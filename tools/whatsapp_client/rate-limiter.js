function createRateLimiter(config) {
  const globalTimestamps = [];
  const perNumberTimestamps = {};

  function checkLimit(number) {
    const now = Date.now();
    const oneMinuteAgo = now - 60 * 1000;
    const oneHourAgo = now - 60 * 60 * 1000;

    // Prune and check global limit
    while (globalTimestamps.length > 0 && globalTimestamps[0] < oneMinuteAgo) {
      globalTimestamps.shift();
    }

    if (globalTimestamps.length >= config.rateLimitPerMinute) {
      return {
        allowed: false,
        reason: `Global rate limit exceeded (max ${config.rateLimitPerMinute}/min)`,
      };
    }

    // Prune and check per-number limit
    if (!perNumberTimestamps[number]) {
      perNumberTimestamps[number] = [];
    }

    const numberTs = perNumberTimestamps[number];
    while (numberTs.length > 0 && numberTs[0] < oneHourAgo) {
      numberTs.shift();
    }

    if (numberTs.length >= config.rateLimitPerNumberPerHour) {
      return {
        allowed: false,
        reason: `Per-number rate limit exceeded for ${number} (max ${config.rateLimitPerNumberPerHour}/hr)`,
      };
    }

    return { allowed: true };
  }

  function recordUsage(number) {
    const now = Date.now();
    globalTimestamps.push(now);

    if (!perNumberTimestamps[number]) {
      perNumberTimestamps[number] = [];
    }
    perNumberTimestamps[number].push(now);
  }

  return { checkLimit, recordUsage };
}

module.exports = { createRateLimiter };
