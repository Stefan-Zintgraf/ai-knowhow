const fs = require('fs');
const path = require('path');
const os = require('os');
const { createLogger } = require('../../logger');

let tmpDir;
let config;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'logger-test-'));
  config = {
    logFile: path.join(tmpDir, 'logs', 'wa-sender'),
    logRetentionDays: 7,
  };
  jest.spyOn(process.stdout, 'write').mockImplementation(() => {});
});

afterEach(() => {
  jest.restoreAllMocks();
  fs.rmSync(tmpDir, { recursive: true, force: true });
});

function getTodayDateStr() {
  const now = new Date();
  return now.getFullYear() + '-' +
    String(now.getMonth() + 1).padStart(2, '0') + '-' +
    String(now.getDate()).padStart(2, '0');
}

describe('logger.js - createLogger()', () => {
  test('log line format: [YYYY-MM-DD HH:mm:ss] EVENT number "message"', () => {
    const { log } = createLogger(config);
    log('SENT', '4915111111111', 'Hello world');

    const dateStr = getTodayDateStr();
    const logFile = path.join(tmpDir, 'logs', `wa-sender-${dateStr}.log`);
    const content = fs.readFileSync(logFile, 'utf8');

    expect(content).toMatch(/^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] SENT 4915111111111 "Hello world"\n$/);
  });

  test('message over 200 chars is truncated to 200', () => {
    const { log } = createLogger(config);
    const longMessage = 'x'.repeat(300);
    log('SENT', '4915111111111', longMessage);

    const dateStr = getTodayDateStr();
    const logFile = path.join(tmpDir, 'logs', `wa-sender-${dateStr}.log`);
    const content = fs.readFileSync(logFile, 'utf8');

    // Message in quotes should be exactly 200 chars
    const match = content.match(/"([^"]*)"/);
    expect(match[1]).toHaveLength(200);
  });

  test('event without target number omits number from log line', () => {
    const { log } = createLogger(config);
    log('STARTUP', null, 'Service started, 3 allowed numbers loaded');

    const dateStr = getTodayDateStr();
    const logFile = path.join(tmpDir, 'logs', `wa-sender-${dateStr}.log`);
    const content = fs.readFileSync(logFile, 'utf8');

    expect(content).toMatch(/^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] STARTUP "Service started, 3 allowed numbers loaded"\n$/);
  });

  test('log file created with correct date-stamped name', () => {
    const { log } = createLogger(config);
    log('TEST', null, 'test');

    const dateStr = getTodayDateStr();
    const logFile = path.join(tmpDir, 'logs', `wa-sender-${dateStr}.log`);
    expect(fs.existsSync(logFile)).toBe(true);
  });

  test('log directory auto-created if missing', () => {
    const logDir = path.join(tmpDir, 'logs');
    expect(fs.existsSync(logDir)).toBe(false);

    const { log } = createLogger(config);
    log('TEST', null, 'test');

    expect(fs.existsSync(logDir)).toBe(true);
  });

  test('quiet mode: SENT does not write to stdout; file still updated', () => {
    const { log } = createLogger(config);
    log('SENT', '4915111111111', 'Hi');

    expect(process.stdout.write).not.toHaveBeenCalled();

    const dateStr = getTodayDateStr();
    const logFile = path.join(tmpDir, 'logs', `wa-sender-${dateStr}.log`);
    expect(fs.readFileSync(logFile, 'utf8')).toContain('SENT');
  });

  test('verbose mode: SENT writes to stdout', () => {
    const { log } = createLogger(config, { verbose: true });
    log('SENT', '4915111111111', 'Hi');

    expect(process.stdout.write).toHaveBeenCalled();
  });

  test('quiet mode: STARTUP still writes to stdout', () => {
    const { log } = createLogger(config);
    log('STARTUP', null, 'ready');

    expect(process.stdout.write).toHaveBeenCalled();
  });

  test('housekeeping deletes old log files and keeps recent ones', () => {
    const logDir = path.join(tmpDir, 'logs');
    fs.mkdirSync(logDir, { recursive: true });

    // Create an old log file (20 days ago)
    const oldDate = new Date();
    oldDate.setDate(oldDate.getDate() - 20);
    const oldDateStr = oldDate.getFullYear() + '-' +
      String(oldDate.getMonth() + 1).padStart(2, '0') + '-' +
      String(oldDate.getDate()).padStart(2, '0');
    const oldFile = path.join(logDir, `wa-sender-${oldDateStr}.log`);
    fs.writeFileSync(oldFile, 'old log');

    // Create a recent log file (1 day ago)
    const recentDate = new Date();
    recentDate.setDate(recentDate.getDate() - 1);
    const recentDateStr = recentDate.getFullYear() + '-' +
      String(recentDate.getMonth() + 1).padStart(2, '0') + '-' +
      String(recentDate.getDate()).padStart(2, '0');
    const recentFile = path.join(logDir, `wa-sender-${recentDateStr}.log`);
    fs.writeFileSync(recentFile, 'recent log');

    const { runHousekeeping } = createLogger(config);
    runHousekeeping();

    expect(fs.existsSync(oldFile)).toBe(false);
    expect(fs.existsSync(recentFile)).toBe(true);
  });

  test('housekeeping on empty log directory does not error', () => {
    const logDir = path.join(tmpDir, 'logs');
    fs.mkdirSync(logDir, { recursive: true });

    const { runHousekeeping } = createLogger(config);
    expect(() => runHousekeeping()).not.toThrow();
  });

  test('housekeeping exception during file deletion does not throw', () => {
    const logDir = path.join(tmpDir, 'logs');
    fs.mkdirSync(logDir, { recursive: true });

    // Create an old file then make the directory read-only to simulate deletion error
    const oldDate = new Date();
    oldDate.setDate(oldDate.getDate() - 20);
    const oldDateStr = oldDate.getFullYear() + '-' +
      String(oldDate.getMonth() + 1).padStart(2, '0') + '-' +
      String(oldDate.getDate()).padStart(2, '0');
    fs.writeFileSync(path.join(logDir, `wa-sender-${oldDateStr}.log`), 'old');

    // Mock unlinkSync to throw
    const originalUnlink = fs.unlinkSync;
    jest.spyOn(fs, 'unlinkSync').mockImplementation(() => {
      throw new Error('Permission denied');
    });
    jest.spyOn(console, 'error').mockImplementation(() => {});

    const { runHousekeeping } = createLogger(config);
    expect(() => runHousekeeping()).not.toThrow();

    fs.unlinkSync.mockRestore();
  });

  test('LOG_FILE with hyphens — date extraction works correctly', () => {
    const hyphenConfig = {
      logFile: path.join(tmpDir, 'logs', 'my-wa-sender'),
      logRetentionDays: 7,
    };
    const logDir = path.join(tmpDir, 'logs');
    fs.mkdirSync(logDir, { recursive: true });

    // Create an old file with hyphenated base name
    const oldDate = new Date();
    oldDate.setDate(oldDate.getDate() - 20);
    const oldDateStr = oldDate.getFullYear() + '-' +
      String(oldDate.getMonth() + 1).padStart(2, '0') + '-' +
      String(oldDate.getDate()).padStart(2, '0');
    const oldFile = path.join(logDir, `my-wa-sender-${oldDateStr}.log`);
    fs.writeFileSync(oldFile, 'old');

    // Create a recent file
    const recentDate = new Date();
    recentDate.setDate(recentDate.getDate() - 1);
    const recentDateStr = recentDate.getFullYear() + '-' +
      String(recentDate.getMonth() + 1).padStart(2, '0') + '-' +
      String(recentDate.getDate()).padStart(2, '0');
    const recentFile = path.join(logDir, `my-wa-sender-${recentDateStr}.log`);
    fs.writeFileSync(recentFile, 'recent');

    const { runHousekeeping } = createLogger(hyphenConfig);
    runHousekeeping();

    expect(fs.existsSync(oldFile)).toBe(false);
    expect(fs.existsSync(recentFile)).toBe(true);
  });
});
