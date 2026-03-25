import { MessageStatus } from './message-status'

type GatewayStatusMessageProps = {
  state: 'checking' | 'error'
  error?: string | null
  onRetry?: () => void
  className?: string
}

export function GatewayStatusMessage({
  state,
  error,
  onRetry,
  className,
}: GatewayStatusMessageProps) {
  const isChecking = state === 'checking'
  const err = (error ?? '').toLowerCase()
  const isPairing =
    !isChecking &&
    (err.includes('pairing') ||
      err.includes('device') ||
      err.includes('approve'))
  const title = isChecking
    ? 'Checking gateway connection...'
    : isPairing
      ? 'Gateway pairing required'
      : 'OpenClaw gateway is unreachable'
  const description = isChecking
    ? 'This dashboard needs access to the OpenClaw gateway configured by your server environment variables.'
    : ''
  return (
    <MessageStatus
      title={title}
      description={
        isChecking ? (
          description
        ) : isPairing ? (
          <>
            This machine&apos;s WebClaw device identity is not approved on the
            gateway yet. On the gateway host run:{' '}
            <span className="font-mono">openclaw devices approve &lt;device-id&gt;</span>{' '}
            (see server logs for the device id), or copy an approved{' '}
            <span className="font-mono">.device-keys.json</span> from another
            setup.
          </>
        ) : (
          <>
            We could not reach the gateway from the dashboard server. Start the
            gateway and confirm your server environment has{' '}
            <span className="font-mono">CLAWDBOT_GATEWAY_URL</span> plus{' '}
            <span className="font-mono">CLAWDBOT_GATEWAY_TOKEN</span> (or{' '}
            <span className="font-mono">CLAWDBOT_GATEWAY_PASSWORD</span>).
          </>
        )
      }
      detail={isChecking ? null : error}
      actionLabel={isChecking ? undefined : 'Retry'}
      onAction={isChecking ? undefined : onRetry}
      className={className}
    />
  )
}
