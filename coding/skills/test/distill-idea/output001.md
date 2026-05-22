# Goals

1. Surface account-critical events reliably so users notice them in time to act.
2. Enable at-a-glance triage so users can distinguish noise from events needing response.
3. Persist per-user handled-state durably so resolved notifications do not re-nag across devices.
4. Non-goal: Deliver mobile push notifications — owned by the mobile team on a separate track.

Stripped detail: base on existing React `<NotificationDrawer>` component
Stripped detail: wire to `/api/v2/events` endpoint
Stripped detail: persist read-state in Postgres `user_notification_state` table
Stripped detail: ship in roughly two sprints
