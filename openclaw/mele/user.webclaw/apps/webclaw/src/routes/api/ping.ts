import { createFileRoute } from '@tanstack/react-router'
import { json } from '@tanstack/react-start'
import { gatewayConnectCheck } from '../../server/gateway'

export const Route = createFileRoute('/api/ping')({
  server: {
    handlers: {
      GET: async () => {
        try {
          await gatewayConnectCheck()
          return json({ ok: true })
        } catch (err) {
          // Always 200 so the client can show ok: false + specific error (e.g. pairing).
          return json({
            ok: false,
            error: err instanceof Error ? err.message : String(err),
          })
        }
      },
    },
  },
})
