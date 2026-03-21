const express = require('express');
const request = require('supertest');
const { createSendRoute } = require('../../routes/send');
const { createRateLimiter } = require('../../rate-limiter');

const TEST_API_KEY = 'a'.repeat(32);
const TEST_NUMBER = '4915111111111';

function createTestApp(options = {}) {
  const config = {
    apiKey: TEST_API_KEY,
    allowedNumbers: [TEST_NUMBER, '4915122222222'],
    ...options.configOverrides,
  };

  const mockSocket = options.socket !== undefined ? options.socket : {
    sendMessage: jest.fn().mockResolvedValue({}),
  };

  const getSocket = options.getSocket || (() => mockSocket);
  const logFn = options.log || jest.fn();
  const rateLimiter = options.rateLimiter || createRateLimiter({
    rateLimitPerMinute: 100,
    rateLimitPerNumberPerHour: 100,
  });

  const app = express();
  app.use(express.json());
  app.use(createSendRoute(getSocket, config, logFn, rateLimiter));

  return { app, mockSocket, logFn, rateLimiter };
}

describe('POST /send - integration tests', () => {
  test('valid request with correct API key + allowed number → 200', async () => {
    const { app, mockSocket } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER, message: 'Hello' });

    expect(res.status).toBe(200);
    expect(res.body).toEqual({ success: true });
    expect(mockSocket.sendMessage).toHaveBeenCalledWith(
      `${TEST_NUMBER}@s.whatsapp.net`,
      { text: 'Hello' }
    );
  });

  test('wrong API key → 401', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', 'wrong-key')
      .send({ number: TEST_NUMBER, message: 'Hello' });

    expect(res.status).toBe(401);
    expect(res.body).toEqual({
      success: false,
      error: 'Unauthorized: invalid or missing API key',
    });
  });

  test('missing API key header → 401', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .send({ number: TEST_NUMBER, message: 'Hello' });

    expect(res.status).toBe(401);
    expect(res.body.success).toBe(false);
    expect(res.body.error).toContain('Unauthorized');
  });

  test('missing number field → 400', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ message: 'Hello' });

    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      success: false,
      error: 'Missing required fields: number and message',
    });
  });

  test('missing message field → 400', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER });

    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      success: false,
      error: 'Missing required fields: number and message',
    });
  });

  test('empty body → 400', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({});

    expect(res.status).toBe(400);
  });

  test('number as integer (not string) → still works (coerced)', async () => {
    const { app, mockSocket } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: 4915111111111, message: 'Hello' });

    expect(res.status).toBe(200);
    expect(res.body).toEqual({ success: true });
    expect(mockSocket.sendMessage).toHaveBeenCalledWith(
      `${TEST_NUMBER}@s.whatsapp.net`,
      { text: 'Hello' }
    );
  });

  test('invalid phone number format → 400', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: 'hello', message: 'Hello' });

    expect(res.status).toBe(400);
    expect(res.body).toEqual({
      success: false,
      error: 'Invalid phone number format',
    });
  });

  test('invalid phone number with special chars → 400', async () => {
    const { app } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: '49+151111', message: 'Hello' });

    expect(res.status).toBe(400);
    expect(res.body.error).toBe('Invalid phone number format');
  });

  test('number not in allowlist → 403 + REJECTED logged', async () => {
    const { app, logFn } = createTestApp();

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: '4915199999999', message: 'Hello' });

    expect(res.status).toBe(403);
    expect(res.body).toEqual({
      success: false,
      error: 'Forbidden: number not in allowlist',
    });
    expect(logFn).toHaveBeenCalledWith('REJECTED', '4915199999999', 'Hello');
  });

  test('rate limit exceeded → 429 + RATE_LIMITED logged', async () => {
    const rateLimiter = createRateLimiter({
      rateLimitPerMinute: 1,
      rateLimitPerNumberPerHour: 100,
    });
    const logFn = jest.fn();
    const { app } = createTestApp({ rateLimiter, log: logFn });

    // First request succeeds
    await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER, message: 'First' });

    // Second request should be rate limited
    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER, message: 'Second' });

    expect(res.status).toBe(429);
    expect(res.body.success).toBe(false);
    expect(res.body.error).toContain('rate limit');
    expect(logFn).toHaveBeenCalledWith('RATE_LIMITED', TEST_NUMBER, 'Second');
  });

  test('socket is null (not connected) → 503', async () => {
    const { app } = createTestApp({ getSocket: () => null });

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER, message: 'Hello' });

    expect(res.status).toBe(503);
    expect(res.body).toEqual({
      success: false,
      error: 'WhatsApp connection not ready',
    });
  });

  test('socket.sendMessage throws error → 500', async () => {
    const mockSocket = {
      sendMessage: jest.fn().mockRejectedValue(new Error('Network error')),
    };
    const { app } = createTestApp({ socket: mockSocket });

    const res = await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: TEST_NUMBER, message: 'Hello' });

    expect(res.status).toBe(500);
    expect(res.body).toEqual({
      success: false,
      error: 'Internal server error',
    });
  });

  test('verify sendMessage called with correct JID format', async () => {
    const { app, mockSocket } = createTestApp();

    await request(app)
      .post('/send')
      .set('x-api-key', TEST_API_KEY)
      .send({ number: '4915122222222', message: 'Test' });

    expect(mockSocket.sendMessage).toHaveBeenCalledWith(
      '4915122222222@s.whatsapp.net',
      { text: 'Test' }
    );
  });

  test('all responses are JSON with { success, error? } shape', async () => {
    const { app } = createTestApp();

    // Test various error responses
    const responses = [
      await request(app).post('/send').send({}), // no api key
      await request(app).post('/send').set('x-api-key', TEST_API_KEY).send({}), // missing fields
    ];

    for (const res of responses) {
      expect(res.headers['content-type']).toMatch(/json/);
      expect(typeof res.body.success).toBe('boolean');
      if (!res.body.success) {
        expect(typeof res.body.error).toBe('string');
      }
    }
  });
});
