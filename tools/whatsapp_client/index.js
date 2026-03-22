const fs = require('fs');
const { loadConfig } = require('./config');
const { createLogger } = require('./logger');
const { createRateLimiter } = require('./rate-limiter');
const { createSendRoute } = require('./routes/send');
const {
  default: makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore,
} = require('@whiskeysockets/baileys');
const express = require('express');
const qrcode = require('qrcode-terminal');

const { version: appVersion } = require('./package.json');

function parseCliArgs(argv) {
  let verbose = false;
  let help = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      help = true;
      continue;
    }
    if (a === '-v' || a === '--verbose') {
      verbose = true;
      const next = argv[i + 1];
      if (next === '1' || next === '2' || next === '3') {
        i += 1;
      }
      continue;
    }
    if (a.startsWith('--verbose=')) {
      const v = a.slice('--verbose='.length).trim();
      verbose = v === '' || v === '1' || v === 'true' || v === 'yes';
      continue;
    }
    if (/^-v\d+$/.test(a)) {
      verbose = true;
      continue;
    }
  }
  return { verbose, help };
}

function printHelp() {
  console.log(`whatsapp_client — HTTP API for sending WhatsApp messages

Usage:
  node index.js [options]

Options:
  -v, --verbose       Print all log lines to stdout (same as -v 1).
  -v 1                Same as --verbose.
  --verbose=1         Same as --verbose.
  -h, --help          Show this help.

Without -v, only essential lines are printed to stdout (errors, startup, shutdown);
routine traffic (SENT, RECONNECT, housekeeping, etc.) is still written to the log file.

Examples:
  node index.js
  node index.js -v
  node index.js --verbose
`);
}

const cli = parseCliArgs(process.argv.slice(2));
if (cli.help) {
  printHelp();
  process.exit(0);
}

const config = loadConfig();
const { log, runHousekeeping } = createLogger(config, { verbose: cli.verbose });
const rateLimiter = createRateLimiter(config);

let sock = null;
let connectionState = null;
let consecutiveFailures = 0;
let server = null;
let isShuttingDown = false;
/** One-shot: clear disk auth and reconnect so a new QR can be scanned (handles stale creds after 405). */
let clearedAuthAfter405 = false;

function getSocket() {
  if (connectionState === 'open' && sock) {
    return sock;
  }
  return null;
}

function clearAuthFolder() {
  try {
    fs.rmSync(config.authFolder, { recursive: true, force: true });
  } catch (_) {
    // ignore
  }
  fs.mkdirSync(config.authFolder, { recursive: true });
}

async function connectToWhatsApp() {
  fs.mkdirSync(config.authFolder, { recursive: true });

  const { state, saveCreds } = await useMultiFileAuthState(config.authFolder);

  const noopLogger = {
    info() {},
    error() {},
    warn() {},
    debug() {},
    trace() {},
    child() { return this; },
  };

  const { version } = await fetchLatestBaileysVersion();

  // Clean up old socket event listeners before creating new one (F2)
  if (sock) {
    try { sock.ev.removeAllListeners(); } catch (_) {}
  }

  sock = makeWASocket({
    auth: {
      creds: state.creds,
      keys: makeCacheableSignalKeyStore(state.keys, noopLogger),
    },
    version,
    logger: noopLogger,
    printQRInTerminal: false,
    browser: ['whatsapp_client', 'http-api', appVersion],
    syncFullHistory: false,
    markOnlineOnConnect: false,
  });

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      log('STARTUP', null, 'Scan the QR code below with WhatsApp to pair:');
      qrcode.generate(qr, { small: true });
    }

    if (connection !== undefined) {
      connectionState = connection;
    }

    if (connection === 'close') {
      // Don't reconnect during shutdown (F3)
      if (isShuttingDown) return;

      const statusCode = lastDisconnect?.error?.output?.statusCode;

      if (statusCode === DisconnectReason.loggedOut) {
        log('FATAL', null, 'Session logged out remotely. Delete auth folder and re-pair.');
        return;
      }

      // 405 is not in DisconnectReason — it is a raw HTTP-style status code from WhatsApp
      // indicating the session credentials were rejected (observed in production)
      if (statusCode === 405) {
        const location = lastDisconnect?.error?.data?.location || 'unknown';
        if (!clearedAuthAfter405) {
          clearedAuthAfter405 = true;
          log(
            'RECONNECT',
            null,
            `Session rejected (405, location: ${location}). Clearing stored auth once and reconnecting — scan the new QR if shown. If this repeats, check IP rate limits or account restrictions.`,
          );
          try {
            sock?.end?.();
          } catch (_) {}
          sock = null;
          connectionState = null;
          clearAuthFolder();
          setImmediate(() => {
            connectToWhatsApp().catch((err) => {
              log('ERROR', null, `Reconnect after 405 auth clear failed: ${err.message}`);
            });
          });
          return;
        }
        log(
          'FATAL',
          null,
          `Session rejected by WhatsApp (code 405, location: ${location}) after auth reset. Delete auth folder manually and re-pair. If this persists, the cause may be IP rate-limiting or account restrictions.`,
        );
        return;
      }

      consecutiveFailures++;
      if (consecutiveFailures > 10) {
        log('FATAL', null, `${consecutiveFailures} consecutive reconnection failures. Exiting.`);
        process.exit(1);
      }

      log('RECONNECT', null, `Connection closed (code: ${statusCode}). Reconnecting in 5s... (attempt ${consecutiveFailures})`);
      // Wrap reconnect in try/catch to prevent unhandled rejections (F4)
      setTimeout(() => {
        connectToWhatsApp().catch((err) => {
          log('ERROR', null, `Reconnection failed: ${err.message}`);
          consecutiveFailures++;
          if (consecutiveFailures > 10) {
            log('FATAL', null, `${consecutiveFailures} consecutive reconnection failures. Exiting.`);
            process.exit(1);
          }
          // Retry again after delay
          if (!isShuttingDown) {
            setTimeout(() => {
              connectToWhatsApp().catch(() => {});
            }, 5000);
          }
        });
      }, 5000);
    }

    if (connection === 'open') {
      consecutiveFailures = 0;
      log('STARTUP', null, 'WhatsApp connection established');
    }
  });

  // Wrap saveCreds to prevent unhandled errors (F9)
  sock.ev.on('creds.update', async () => {
    try {
      await saveCreds();
    } catch (err) {
      console.error(`Failed to save credentials: ${err.message}`);
    }
  });
}

// Express setup
const app = express();
app.use(express.json({ limit: '16kb' }));
app.use(createSendRoute(getSocket, config, log, rateLimiter));

// Start
async function main() {
  await connectToWhatsApp();

  server = app.listen(config.port, '127.0.0.1', () => {
    log('STARTUP', null, `Server listening on 127.0.0.1:${config.port}, ${config.allowedNumbers.length} allowed numbers loaded`);
  });

  // Initial housekeeping + daily interval
  runHousekeeping();
  setInterval(runHousekeeping, 24 * 60 * 60 * 1000);
}

// Graceful shutdown
function shutdown(signal) {
  if (isShuttingDown) return; // Prevent double shutdown
  isShuttingDown = true;

  log('SHUTDOWN', null, `Received ${signal}, shutting down`);

  if (sock) {
    try { sock.ev.removeAllListeners(); } catch (_) {}
    try { sock.end(); } catch (_) {}
  }

  if (server) {
    server.close(() => {
      process.exit(0);
    });
    // Force exit after 5s if server.close hangs
    setTimeout(() => process.exit(0), 5000);
  } else {
    process.exit(0);
  }
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Catch unhandled errors to prevent silent crashes (F8)
process.on('unhandledRejection', (reason) => {
  log('ERROR', null, `Unhandled rejection: ${reason}`);
});

process.on('uncaughtException', (err) => {
  log('FATAL', null, `Uncaught exception: ${err.message}`);
  process.exit(1);
});

main().catch((err) => {
  log('FATAL', null, `Startup error: ${err.message}`);
  process.exit(1);
});
