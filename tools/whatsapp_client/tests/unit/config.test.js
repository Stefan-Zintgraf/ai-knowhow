const { loadConfig } = require('../../config');

// Save original env and prevent process.exit from killing tests
let mockExit;
const originalEnv = process.env;

beforeEach(() => {
  process.env = { ...originalEnv };
  // Clear all config-related env vars
  delete process.env.API_KEY;
  delete process.env.PORT;
  delete process.env.ALLOWED_NUMBERS;
  delete process.env.AUTH_FOLDER;
  delete process.env.LOG_FILE;
  delete process.env.LOG_RETENTION_DAYS;
  delete process.env.RATE_LIMIT_PER_MINUTE;
  delete process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR;

  mockExit = jest.spyOn(process, 'exit').mockImplementation(() => {
    throw new Error('process.exit called');
  });
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterEach(() => {
  process.env = originalEnv;
  jest.restoreAllMocks();
});

function setValidEnv() {
  process.env.API_KEY = 'a'.repeat(32);
  process.env.ALLOWED_NUMBERS = '4915111111111,4915122222222';
}

describe('config.js - loadConfig()', () => {
  test('valid config with all vars set returns correct parsed object', () => {
    process.env.API_KEY = 'x'.repeat(64);
    process.env.PORT = '4000';
    process.env.ALLOWED_NUMBERS = '4915111111111,4915122222222';
    process.env.AUTH_FOLDER = 'my_auth';
    process.env.LOG_FILE = 'logs/custom';
    process.env.LOG_RETENTION_DAYS = '14';
    process.env.RATE_LIMIT_PER_MINUTE = '20';
    process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR = '10';

    const config = loadConfig();

    expect(config.apiKey).toBe('x'.repeat(64));
    expect(config.port).toBe(4000);
    expect(config.allowedNumbers).toEqual(['4915111111111', '4915122222222']);
    expect(config.authFolder).toBe('my_auth');
    expect(config.logFile).toBe('logs/custom');
    expect(config.logRetentionDays).toBe(14);
    expect(config.rateLimitPerMinute).toBe(20);
    expect(config.rateLimitPerNumberPerHour).toBe(10);
  });

  test('missing API_KEY exits with error', () => {
    process.env.ALLOWED_NUMBERS = '4915111111111';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(mockExit).toHaveBeenCalledWith(1);
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('API_KEY'));
  });

  test('API_KEY shorter than 32 chars exits with error', () => {
    process.env.API_KEY = 'short';
    process.env.ALLOWED_NUMBERS = '4915111111111';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(mockExit).toHaveBeenCalledWith(1);
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('API_KEY must be at least 32 characters'));
  });

  test('missing ALLOWED_NUMBERS exits with error', () => {
    process.env.API_KEY = 'a'.repeat(32);

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(mockExit).toHaveBeenCalledWith(1);
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('ALLOWED_NUMBERS'));
  });

  test('empty ALLOWED_NUMBERS exits with error', () => {
    process.env.API_KEY = 'a'.repeat(32);
    process.env.ALLOWED_NUMBERS = '   ';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(mockExit).toHaveBeenCalledWith(1);
  });

  test('ALLOWED_NUMBERS with non-digit entry exits with error', () => {
    process.env.API_KEY = 'a'.repeat(32);
    process.env.ALLOWED_NUMBERS = '49abc1234567';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('49abc1234567'));
  });

  test('ALLOWED_NUMBERS with too-short number exits with error', () => {
    process.env.API_KEY = 'a'.repeat(32);
    process.env.ALLOWED_NUMBERS = '123';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('123'));
  });

  test('invalid PORT (non-numeric) exits with error', () => {
    setValidEnv();
    process.env.PORT = 'abc';

    expect(() => loadConfig()).toThrow('process.exit called');
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('PORT'));
  });

  test('defaults applied when optional vars not set', () => {
    setValidEnv();

    const config = loadConfig();

    expect(config.port).toBe(3000);
    expect(config.authFolder).toBe('auth_info_sender');
    expect(config.logFile).toBe('logs/wa-sender');
    expect(config.logRetentionDays).toBe(7);
    expect(config.rateLimitPerMinute).toBe(10);
    expect(config.rateLimitPerNumberPerHour).toBe(5);
  });

  test('ALLOWED_NUMBERS parsed correctly into array', () => {
    setValidEnv();
    process.env.ALLOWED_NUMBERS = '1112223333,4445556666';

    const config = loadConfig();
    expect(config.allowedNumbers).toEqual(['1112223333', '4445556666']);
  });

  test('ALLOWED_NUMBERS with spaces are trimmed', () => {
    setValidEnv();
    process.env.ALLOWED_NUMBERS = '1112223333, 4445556666 ';

    const config = loadConfig();
    expect(config.allowedNumbers).toEqual(['1112223333', '4445556666']);
  });

  test('rate limit values parsed correctly from env', () => {
    setValidEnv();
    process.env.RATE_LIMIT_PER_MINUTE = '25';
    process.env.RATE_LIMIT_PER_NUMBER_PER_HOUR = '8';

    const config = loadConfig();
    expect(config.rateLimitPerMinute).toBe(25);
    expect(config.rateLimitPerNumberPerHour).toBe(8);
  });
});
