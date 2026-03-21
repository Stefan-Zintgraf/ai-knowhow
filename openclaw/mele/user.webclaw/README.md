# WebClaw

![Cover](https://raw.githubusercontent.com/ibelick/webclaw/main/apps/webclaw/public/cover.jpg)

Fast web client for OpenClaw.

**In this monorepo:** this directory is tracked only by [ai-knowhow](https://github.com/Stefan-Zintgraf/ai-knowhow) (upstream WebClaw reference: [ibelick/webclaw](https://github.com/ibelick/webclaw)). Do not run `git init` here; use the repository root for all Git operations.

[webclaw.dev](https://webclaw.dev)

Currently in beta.

## Installation

```bash
npx webclaw
```

The CLI will ask for a project name, env keys, and a port, then create the folder and start WebClaw.

WebClaw env vars: `CLAWDBOT_GATEWAY_URL` + `CLAWDBOT_GATEWAY_TOKEN` (or `CLAWDBOT_GATEWAY_PASSWORD`) — OpenClaw gateway/auth docs: https://docs.openclaw.ai/gateway (env precedence: https://docs.openclaw.ai/help/environment).

## Contributing

Please read the [contributing guide](CONTRIBUTING.md).

## License

See [LICENSE](LICENSE).
