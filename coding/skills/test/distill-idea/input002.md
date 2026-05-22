Goals for the auth-rework work item:

1. Replace the current session-token storage approach with one that meets the new compliance requirements.
2. Keep existing user sessions valid across the cutover so no one gets force-logged-out.
3. Make the new storage layer observable enough that we can detect token-handling regressions before users do.
4. Leave room for a future second auth factor without committing to a specific mechanism now.
