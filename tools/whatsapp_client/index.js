const fs = require('fs');
const { loadConfig } = require('./config');
const { createLogger } = require('./logger');
const { createRateLimiter } = require('./rate-limiter');
const { createSendRoute } = require('./routes/send');
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const express = require('express');

const config = loadConfig();
const { log, runHousekeeping } = createLogger(config);
const rateLimiter = createRateLimiter(config);

let sock = null;
let connectionState = null;
let consecutiveFailures = 0;
let server = null;
let isShuttingDown = false;

function getSocket() {
  if (connectionState === 'open' && sock) {
    return sock;
  }
  return null;
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

  // Clean up old socket event listeners before creating new one (F2)
  if (sock) {
    try { sock.ev.removeAllListeners(); } catch (_) {}
  }

  sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
    logger: noopLogger,
  });

  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect } = update;

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
