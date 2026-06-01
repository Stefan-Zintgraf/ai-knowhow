Update the error handling in the payment processing module. When a payment fails, the current behavior just logs the error. We want to add retry logic with exponential backoff and notify the user via email when all retries are exhausted. Not sure which files handle payment processing or what the current error handling looks like.

The user confirms they want the agent to explore the codebase to score the triage axes.

Exploration results (simulated B10 dispatch):
- Read 1: src/services/payments/index.ts — found PaymentService class
- Read 2: src/services/payments/processor.ts — found processPayment method with try/catch
- Read 3: src/services/payments/retry.ts — file not found, no existing retry logic
- Read 4: src/services/notifications/email.ts — found EmailService
- Read 5: src/services/payments/types.ts — found PaymentError type
- Read 6: BUDGET EXCEEDED — agent attempted to read src/services/payments/config.ts (6th read)
