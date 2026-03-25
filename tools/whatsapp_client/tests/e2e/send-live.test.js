const http = require('http');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

// Load test environment
const envTestPath = path.join(__dirname, '../../.env.test');
const envPath = path.join(__dirname, '../../.env');

if (fs.existsSync(envTestPath)) {
  dotenv.config({ path: envTestPath });
} else if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
}

const API_KEY = process.env.API_KEY;
const PORT = process.env.PORT || 3000;
const TEST_NUMBER = process.env.E2E_TEST_NUMBER || (process.env.ALLOWED_NUMBERS || '').split(',')[0]?.trim();
const BASE_URL = `http://127.0.0.1:${PORT}`;

function makeRequest(body, headers = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request(`${BASE_URL}/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        ...headers,
      },
    }, (res) => {
      let responseData = '';
      res.on('data', (chunk) => { responseData += chunk; });
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          body: JSON.parse(responseData),
        });
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function isServiceRunning() {
  return new Promise((resolve) => {
    const req = http.request(`${BASE_URL}/send`, { method: 'POST' }, (res) => {
      res.resume();
      resolve(true);
    });
    req.on('error', () => resolve(false));
    req.end();
  });
}

describe('E2E: POST /send against live service', () => {
  let serviceAvailable = false;

  beforeAll(async () => {
    serviceAvailable = await isServiceRunning();
    if (!serviceAvailable) {
      console.warn('Service not running — skipping E2E tests');
    }
  });

  test('send real message to allowed number → 200', async () => {
    if (!serviceAvailable) return;
    if (!TEST_NUMBER) {
      console.warn('No test number configured — skipping');
      return;
    }

    const timestamp = new Date().toISOString();
    const res = await makeRequest({
      number: TEST_NUMBER,
      message: `E2E test message at ${timestamp}`,
    });

    expect(res.status).toBe(200);
    expect(res.body).toEqual({ success: true });
  });

  test('verify SENT entry appears in today\'s log file', async () => {
    if (!serviceAvailable) return;
    if (!TEST_NUMBER) return;

    const logFile = process.env.LOG_FILE || 'logs/wa-sender';
    const logDir = path.dirname(path.join(__dirname, '../../', logFile));
    const logName = path.basename(logFile);

    const now = new Date();
    const dateStr = now.getFullYear() + '-' +
      String(now.getMonth() + 1).padStart(2, '0') + '-' +
      String(now.getDate()).padStart(2, '0');
    const todayLog = path.join(logDir, `${logName}-${dateStr}.log`);

    if (!fs.existsSync(todayLog)) {
      console.warn('Log file not found — skipping log verification');
      return;
    }

    const content = fs.readFileSync(todayLog, 'utf8');
    expect(content).toContain('SENT');
    expect(content).toContain(TEST_NUMBER);
  });

  test('send to non-allowed number → 403', async () => {
    if (!serviceAvailable) return;

    const res = await makeRequest({
      number: '1234567890',
      message: 'This should be rejected',
    });

    expect(res.status).toBe(403);
    expect(res.body.success).toBe(false);
  });
});
