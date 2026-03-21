const { createRateLimiter } = require('../../rate-limiter');

describe('rate-limiter.js - createRateLimiter()', () => {
  test('under global limit returns allowed: true', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 5, rateLimitPerNumberPerHour: 10 });
    const result = limiter.checkLimit('4915111111111');
    expect(result).toEqual({ allowed: true });
  });

  test('exceeds global limit returns allowed: false', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 3, rateLimitPerNumberPerHour: 100 });

    limiter.recordUsage('1111111');
    limiter.recordUsage('2222222');
    limiter.recordUsage('3333333');
    const result = limiter.checkLimit('4444444');

    expect(result.allowed).toBe(false);
    expect(result.reason).toContain('Global rate limit exceeded');
    expect(result.reason).toContain('3/min');
  });

  test('under per-number limit returns allowed: true', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 100, rateLimitPerNumberPerHour: 3 });

    limiter.recordUsage('1111111');
    limiter.recordUsage('1111111');
    const result = limiter.checkLimit('1111111');

    expect(result).toEqual({ allowed: true });
  });

  test('exceeds per-number limit returns allowed: false', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 100, rateLimitPerNumberPerHour: 2 });

    limiter.recordUsage('1111111');
    limiter.recordUsage('1111111');
    const result = limiter.checkLimit('1111111');

    expect(result.allowed).toBe(false);
    expect(result.reason).toContain('Per-number rate limit exceeded');
    expect(result.reason).toContain('1111111');
    expect(result.reason).toContain('2/hr');
  });

  test('different numbers have independent per-number counters', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 100, rateLimitPerNumberPerHour: 2 });

    limiter.recordUsage('1111111');
    limiter.recordUsage('1111111');

    // Different number should still be allowed
    const result = limiter.checkLimit('2222222');
    expect(result).toEqual({ allowed: true });
  });

  test('old timestamps are pruned (expired entries do not count)', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 2, rateLimitPerNumberPerHour: 100 });

    const realNow = Date.now;
    let currentTime = realNow();

    jest.spyOn(Date, 'now').mockImplementation(() => currentTime);

    limiter.recordUsage('1111111');
    limiter.recordUsage('1111111');

    // Should be blocked now
    expect(limiter.checkLimit('1111111').allowed).toBe(false);

    // Advance time by 61 seconds
    currentTime += 61 * 1000;

    // Should be allowed again (old timestamps pruned)
    const result = limiter.checkLimit('1111111');
    expect(result.allowed).toBe(true);

    Date.now.mockRestore();
  });

  test('checkLimit does not record usage (read-only check)', () => {
    const limiter = createRateLimiter({ rateLimitPerMinute: 2, rateLimitPerNumberPerHour: 100 });

    // checkLimit alone should never exhaust the limit
    limiter.checkLimit('1111111');
    limiter.checkLimit('1111111');
    limiter.checkLimit('1111111');
    limiter.checkLimit('1111111');

    // Should still be allowed since checkLimit doesn't record
    expect(limiter.checkLimit('1111111').allowed).toBe(true);
  });
});
