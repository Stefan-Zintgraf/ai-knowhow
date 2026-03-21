const dotenv = require('dotenv');

function loadConfig() {
  dotenv.config();

  const errors = [];

  const apiKey = process.env.API_KEY;
  if (!apiKey) {
    errors.push('API_KEY is required');
  } else if (apiKey.length < 32) {
    errors.push('API_KEY must be at least 32 characters');
  }

  const portStr = process.env.PORT;
  let port = 3000;
  if (portStr !== undefined && portStr !== '') {
    port = parseInt(portStr, 10);
    if (isNaN(port) || port < 1 || port > 65535) {
      errors.push('PORT must be a valid integer between 1 and 65535');
    }
  }

  const allowedNumbersStr = process.env.ALLOWED_NUMBERS;
  let allowedNumbers = [];
  if (!allowedNumbersStr || allowedNumbersStr.trim() === '') {
    errors.push('ALLOWED_NUMBERS is required');
  } else {
    allowedNumbers = allowedNumbersStr.split(',').map(n => n.trim());
    const phoneRegex = /^\d{7,15}$/;
    for (const num of allowedNumbers) {
      if (!phoneRegex.test(num)) {
        errors.push(`Invalid phone number in ALLOWED_NUMBERS: "${num}" (must be 7-15 digits only)`);
      }
    }
  }

  const authFolder = process.env.AUTH_FOLDER || 'auth_info_sender';
  const logFile = process.env.LOG_FILE || 'logs/wa-sender';

  let logRetentionDays = 7;
  if (process.env.LOG_RETENTION_DAYS !== undefined && process.env.LOG_RETENTION_DAYS !== '') {
    logRetentionDays = parseInt(process.env.LOG_RETENTION_DAYS, 10);
    if (isNaN(logRetentionDays) || logRetentionDays < 1) {
      errors.push('LOG_RETENTION_DAYS must be a positive integer');
    }
  }

  let rateLimitPerMinute = 10;
  if (process.env.RATE_LIMIT_PER_MINUTE !== undefined && process.env.RATE_LIMIT_PER_MINUTE !== '') {
    rateLimitPerMinute = parseInt(process.env.RATE_LIMIT_PER_MINUTE, 10);
    if (isNaN(rateLimitPerMinute) || rateLimitPerMinute < 1) {
      errors.push('RATE_LIMIT_PER_MINUTE must be a positive integer');
    }
  }

  let rateLimitPerNumberPerHour = 5;
  if (process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR !== undefined && process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR !== '') {
    rateLimitPerNumberPerHour = parseInt(process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR, 10);
    if (isNaN(rateLimitPerNumberPerHour) || rateLimitPerNumberPerHour < 1) {
      errors.push('RATE_LIMIT_PER_NUMBER_PER_HOUR must be a positive integer');
    }
  }

  if (errors.length > 0) {
    for (const err of errors) {
      console.error(`Config error: ${err}`);
    }
    process.exit(1);
  }

  return {
    apiKey,
    port,
    allowedNumbers,
    authFolder,
    logFile,
    logRetentionDays,
    rateLimitPerMinute,
    rateLimitPerNumberPerHour,
  };
}

module.exports = { loadConfig };
