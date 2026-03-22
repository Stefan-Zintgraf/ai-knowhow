const fs = require('fs');
const path = require('path');

/** Events always echoed to stdout when verbose is off (full audit still goes to the log file). */
const STDOUT_QUIET_ALLOW = new Set(['FATAL', 'ERROR', 'SHUTDOWN', 'STARTUP']);

function createLogger(config, options = {}) {
  const verboseStdout = Boolean(options.verbose);
  const logBase = config.logFile;
  const logDir = path.dirname(logBase);
  const logName = path.basename(logBase);

  function getLogFilePath() {
    const now = new Date();
    const dateStr = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0');
    return path.join(logDir, `${logName}-${dateStr}.log`);
  }

  function formatTimestamp() {
    const now = new Date();
    const date = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0');
    const time = String(now.getHours()).padStart(2, '0') + ':' +
      String(now.getMinutes()).padStart(2, '0') + ':' +
      String(now.getSeconds()).padStart(2, '0');
    return `${date} ${time}`;
  }

  function log(event, targetNumber, message) {
    const timestamp = formatTimestamp();
    let line = `[${timestamp}] ${event}`;

    if (targetNumber != null) {
      line += ` ${targetNumber}`;
    }

    if (message != null) {
      // Sanitize: strip newlines/control chars to prevent log injection
      const sanitized = String(message).replace(/[\r\n\x00-\x1f]/g, ' ');
      const truncated = sanitized.substring(0, 200);
      line += ` "${truncated}"`;
    }

    line += '\n';

    fs.mkdirSync(logDir, { recursive: true });

    const filePath = getLogFilePath();
    fs.appendFileSync(filePath, line);

    if (verboseStdout || STDOUT_QUIET_ALLOW.has(event)) {
      process.stdout.write(line);
    }
  }

  function runHousekeeping() {
    try {
      if (!fs.existsSync(logDir)) {
        log('HOUSEKEEPING', null, 'Deleted 0 log files');
        return;
      }

      const files = fs.readdirSync(logDir);
      // Only match files with our configured logName prefix
      const dateRegex = new RegExp(`^${logName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}-(\\d{4}-\\d{2}-\\d{2})\\.log$`);
      const now = new Date();
      let deletedCount = 0;

      for (const file of files) {
        const match = file.match(dateRegex);
        if (!match) continue;

        const fileDate = new Date(match[1] + 'T00:00:00');
        const ageDays = (now - fileDate) / (1000 * 60 * 60 * 24);

        if (ageDays > config.logRetentionDays) {
          try {
            fs.unlinkSync(path.join(logDir, file));
            deletedCount++;
          } catch (err) {
            console.error(`Housekeeping: failed to delete ${file}: ${err.message}`);
          }
        }
      }

      log('HOUSEKEEPING', null, `Deleted ${deletedCount} log files`);
    } catch (err) {
      console.error(`Housekeeping error: ${err.message}`);
    }
  }

  return { log, runHousekeeping };
}

module.exports = { createLogger };
