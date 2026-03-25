const express = require('express');
const crypto = require('crypto');

function createSendRoute(getSocket, config, log, rateLimiter) {
  const router = express.Router();

  router.post('/send', async (req, res) => {
    try {
      // 1. Check API key (constant-time comparison to prevent timing attacks)
      const apiKey = req.headers['x-api-key'];
      if (!apiKey || typeof apiKey !== 'string' ||
          apiKey.length !== config.apiKey.length ||
          !crypto.timingSafeEqual(Buffer.from(apiKey), Buffer.from(config.apiKey))) {
        return res.status(401).json({
          success: false,
          error: 'Unauthorized: invalid or missing API key',
        });
      }

      // 2. Extract and validate fields
      const number = req.body.number != null ? String(req.body.number) : undefined;
      const message = req.body.message;

      if (!number || !message || typeof message !== 'string' || message.length === 0) {
        return res.status(400).json({
          success: false,
          error: 'Missing required fields: number and message',
        });
      }

      // 3. Validate phone number format
      if (!/^\d{7,15}$/.test(number)) {
        return res.status(400).json({
          success: false,
          error: 'Invalid phone number format',
        });
      }

      // 4. Check allowlist
      if (!config.allowedNumbers.includes(number)) {
        log('REJECTED', number, message);
        return res.status(403).json({
          success: false,
          error: 'Forbidden: number not in allowlist',
        });
      }

      // 5. Check rate limit
      const limitResult = rateLimiter.checkLimit(number);
      if (!limitResult.allowed) {
        log('RATE_LIMITED', number, message);
        return res.status(429).json({
          success: false,
          error: limitResult.reason,
        });
      }

      // 6. Check socket connection
      const socket = getSocket();
      if (!socket) {
        return res.status(503).json({
          success: false,
          error: 'WhatsApp connection not ready',
        });
      }

      // 7. Send message
      await socket.sendMessage(number + '@s.whatsapp.net', { text: message });

      // 8. Record rate limit usage only after successful send
      rateLimiter.recordUsage(number);

      // 9. Log and respond
      log('SENT', number, message);
      return res.status(200).json({ success: true });
    } catch (err) {
      // 9. Error handling
      log('ERROR', req.body?.number != null ? String(req.body.number) : null, err.message);
      return res.status(500).json({
        success: false,
        error: 'Internal server error',
      });
    }
  });

  return router;
}

module.exports = { createSendRoute };
