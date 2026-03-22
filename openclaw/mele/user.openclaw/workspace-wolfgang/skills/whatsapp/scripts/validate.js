#!/usr/bin/env node
/**
 * Validate WhatsApp send payload before exec (lightweight).
 * Usage: node validate.js '{"number":"4917...","message":"Hi","mode":"immediate"}'
 */

const input = process.argv[2];
if (!input) {
  console.log(JSON.stringify({ valid: false, errors: ["No JSON provided"] }));
  process.exit(1);
}

let o;
try {
  o = JSON.parse(input);
} catch (e) {
  console.log(JSON.stringify({ valid: false, errors: ["Invalid JSON: " + e.message] }));
  process.exit(1);
}

const errors = [];

if (!o.number || typeof o.number !== "string") {
  errors.push('Missing or invalid "number" (string, digits only, no +)');
} else {
  const digits = o.number.replace(/\s/g, "");
  if (!/^\d{8,15}$/.test(digits)) {
    errors.push('"number" must be 8–15 digits (no + in JSON)');
  }
}

if (!o.message || typeof o.message !== "string" || !o.message.trim()) {
  errors.push('Missing or empty "message"');
}

const mode = o.mode || "immediate";
if (!["immediate", "delayed", "recurring"].includes(mode)) {
  errors.push('Invalid "mode": use immediate | delayed | recurring');
}

if (mode === "delayed") {
  if (o.delaySeconds != null && (typeof o.delaySeconds !== "number" || o.delaySeconds < 0)) {
    errors.push('"delaySeconds" must be a non-negative number when set');
  }
  if (o.atIso != null && typeof o.atIso !== "string") {
    errors.push('"atIso" must be a string when set');
  }
  if (o.delaySeconds == null && o.atIso == null) {
    errors.push('For delayed mode, set delaySeconds and/or atIso');
  }
}

console.log(JSON.stringify({ valid: errors.length === 0, errors }));
