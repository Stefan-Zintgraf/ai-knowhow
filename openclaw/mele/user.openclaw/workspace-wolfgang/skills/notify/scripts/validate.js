#!/usr/bin/env node
/**
 * Validate cron job JSON structure before submission
 * Usage: node validate.js '{"name": "test", "schedule": {...}, ...}'
 * Returns: {"valid": true} or {"valid": false, "errors": [...]}
 */

const input = process.argv[2];
if (!input) {
  console.log(JSON.stringify({ valid: false, errors: ['No JSON provided'] }));
  process.exit(1);
}

let job;
try {
  job = JSON.parse(input);
} catch (e) {
  console.log(JSON.stringify({ valid: false, errors: ['Invalid JSON: ' + e.message] }));
  process.exit(1);
}

const errors = [];

// Required top-level fields
if (!job.name) errors.push('Missing required field: name');
if (!job.schedule) errors.push('Missing required field: schedule');
if (!job.payload) errors.push('Missing required field: payload');
if (!job.sessionTarget) errors.push('Missing required field: sessionTarget');

// Validate schedule
if (job.schedule) {
  if (!job.schedule.kind) {
    errors.push('Missing schedule.kind');
  } else if (!['at', 'every', 'cron'].includes(job.schedule.kind)) {
    errors.push('Invalid schedule.kind: must be "at", "every", or "cron"');
  }
  
  if (job.schedule.kind === 'at' && !job.schedule.at) {
    errors.push('schedule.at is required when kind is "at"');
  }
  if (job.schedule.kind === 'every' && !job.schedule.everyMs) {
    errors.push('schedule.everyMs is required when kind is "every"');
  }
  if (job.schedule.kind === 'cron' && !job.schedule.expr) {
    errors.push('schedule.expr is required when kind is "cron"');
  }
}

// Validate payload
if (job.payload) {
  if (!job.payload.kind) {
    errors.push('Missing payload.kind');
  } else if (!['systemEvent', 'agentTurn'].includes(job.payload.kind)) {
    errors.push('Invalid payload.kind: must be "systemEvent" or "agentTurn"');
  }
  
  if (job.payload.kind === 'systemEvent' && !job.payload.text && !job.payload.message) {
    errors.push('payload.text or payload.message is required for systemEvent');
  }
  if (job.payload.kind === 'agentTurn' && !job.payload.message) {
    errors.push('payload.message is required for agentTurn');
  }
  
  // Check for common mistake: sessionTarget inside payload
  if (job.payload.sessionTarget) {
    errors.push('sessionTarget should be at top level, not inside payload');
  }
}

// Validate sessionTarget
if (job.sessionTarget && !['main', 'isolated'].includes(job.sessionTarget)) {
  errors.push('Invalid sessionTarget: must be "main" or "isolated"');
}

// Check payload.kind matches sessionTarget rules
if (job.payload && job.sessionTarget) {
  if (job.sessionTarget === 'main' && job.payload.kind !== 'systemEvent') {
    errors.push('sessionTarget "main" requires payload.kind "systemEvent"');
  }
  if (job.sessionTarget === 'isolated' && job.payload.kind !== 'agentTurn') {
    errors.push('sessionTarget "isolated" requires payload.kind "agentTurn"');
  }
}

const result = {
  valid: errors.length === 0,
  errors: errors
};

console.log(JSON.stringify(result));
