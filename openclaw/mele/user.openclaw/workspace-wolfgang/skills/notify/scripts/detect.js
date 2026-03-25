#!/usr/bin/env node
/**
 * Detect if a user message is a scheduling/notification request
 * Usage: node detect.js "send me a good morning email every day at 7am"
 * Returns: {"isNotification": true, "confidence": 0.95}
 */

const message = process.argv[2] || '';
const lowerMsg = message.toLowerCase();

// High-confidence patterns (explicit scheduling intent)
const highPatterns = [
  /\bremind\s+me\b/,
  /\bnotify\s+me\b/,
  /\bping\s+me\b/,
  /\bin\s+\d+\s+(second|minute|hour|day)s?\b/,
  /\bat\s+\d{1,2}(?::\d{2})?\s*(am|pm)?\b/,
  /\bevery\s+(morning|afternoon|evening|day|week|month|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b/,
  /\bschedule\b/,
  /\btomorrow\b/,
  /\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|week|month)\b/,
  /\bsend\s+me\b.*\b(in|at|every|when)\b/,
  /\bsend\s+.*(message|email|mail|notification)\b.*\b(in|at|every|tomorrow|morning|evening)\b/,
  /\b(daily|weekly|monthly|hourly)\b/,
  /\beach\s+(day|week|month|morning|evening)\b/,
];

// Medium-confidence patterns (could be scheduling)
const mediumPatterns = [
  /\b(later|soon|tonight|morning|evening)\b/,
  /\b(set|create)\s+a?\s+(reminder|notification|alert|schedule)\b/,
  /\b(recurring|repeat|repeated)\b/,
];

let confidence = 0;
let matchedPatterns = [];

for (const pattern of highPatterns) {
  if (pattern.test(lowerMsg)) {
    confidence += 0.3;
    matchedPatterns.push(pattern.source);
  }
}

for (const pattern of mediumPatterns) {
  if (pattern.test(lowerMsg)) {
    confidence += 0.15;
    matchedPatterns.push(pattern.source);
  }
}

// Cap at 0.95 to avoid overconfidence
confidence = Math.min(confidence, 0.95);

// Must have at least one high-confidence pattern
const hasHighPattern = highPatterns.some(p => p.test(lowerMsg));

const result = {
  isNotification: hasHighPattern && confidence >= 0.3,
  confidence: confidence,
  matchedPatterns: matchedPatterns
};

console.log(JSON.stringify(result));
