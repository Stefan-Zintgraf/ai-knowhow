We're rebuilding the customer-facing notification center. Users keep missing important account events because the current bell-icon dropdown in the top-right of the dashboard is too cramped.

The new thing needs to surface account-critical events reliably so users notice them in time to act. It should let people triage at a glance — distinguish noise from things that need a response. And we need durable state so a notification a user already handled doesn't keep nagging them across devices.

For implementation: use the existing React <NotificationDrawer> component as the base, wire it to the /api/v2/events endpoint, and persist read-state in the Postgres user_notification_state table. Should ship in roughly two sprints.

Explicitly out of scope: mobile push notifications. The mobile team owns that channel and will tackle it separately next quarter.
