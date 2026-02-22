// Gmail hook transform: unlock full agent instructions for trusted senders.
// Untrusted senders keep the default secure behavior (tools disabled, security wrapping on).

const TRUSTED_SENDERS = [
  "s.zintgraf@acontis.com",
  "stefan@zintgraf.de",
];

function extractEmail(from) {
  if (!from || typeof from !== "string") return "";
  // Handle "Name <email>" format
  const match = from.match(/<([^>]+)>/);
  return (match ? match[1] : from).trim().toLowerCase();
}

export default function transform(ctx) {
  const messages = ctx.payload.messages;
  if (!Array.isArray(messages) || messages.length === 0) {
    return {};
  }

  const from = messages[0]?.from;
  const email = extractEmail(from);

  if (TRUSTED_SENDERS.includes(email)) {
    // Trusted sender: enable tools + remove security wrapping + deliver to WhatsApp
    return { deliver: true, allowUnsafeExternalContent: true, channel: "whatsapp", to: "+491777960262" };
  }

  // Untrusted sender: keep defaults (tools disabled, security wrapping on)
  return {};
}
