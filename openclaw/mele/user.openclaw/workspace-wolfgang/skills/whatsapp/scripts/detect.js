#!/usr/bin/env node
/**
 * Detect if a user message is a WhatsApp send/remind/notify request.
 * Usage: node detect.js "remind me on WhatsApp in 5 minutes"
 * Returns: {"isWhatsAppIntent": true, "confidence": 0.9}
 */

const message = process.argv[2] || "";
const lowerMsg = message.toLowerCase();

// Must mention WhatsApp (or clear abbreviation in WA context)
const channelMarkers =
  /\bwhatsapp\b/.test(lowerMsg) ||
  /\bwa\b/.test(lowerMsg) ||
  /\bwhatsapp\s*:/.test(lowerMsg);

const intentPatterns = [
  /\b(remind|notify|ping|send|message|text|schreib)\b/,
  /\bin\s+\d+\s+(second|minute|hour|day)s?\b/,
  /\bat\s+\d{1,2}(?::\d{2})?\s*(am|pm)?\b/,
  /\b(tomorrow|every|daily|weekly|schedule)\b/,
  /\b\+?\d[\d\s\-]{6,}\d\b/, // phone-ish
];

let confidence = 0;
const matchedPatterns = [];

if (channelMarkers) {
  confidence += 0.5;
  matchedPatterns.push("channel:whatsapp_or_wa");
}

for (const pattern of intentPatterns) {
  if (pattern.test(lowerMsg)) {
    confidence += 0.2;
    matchedPatterns.push(pattern.source);
  }
}

confidence = Math.min(confidence, 0.95);
confidence = Math.round(confidence * 100) / 100;

const isWhatsAppIntent = channelMarkers && confidence >= 0.5;

console.log(
  JSON.stringify({
    isWhatsAppIntent,
    confidence,
    matchedPatterns,
  }),
);
