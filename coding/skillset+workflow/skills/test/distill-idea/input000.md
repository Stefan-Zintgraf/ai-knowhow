We need to nail down how AI agents do coding work in this repo — both for greenfield features and for fixes inside the existing codebase. Right now everyone freelances: some sessions sprawl into massive plans, others skip planning entirely on what turn out to be load-bearing changes.

I want a workflow that covers the full path from raw idea to merged code. Alongside it we need guardrails that protect the system's intent so agents don't drift, but those guardrails can't bloat the always-on context — we already burn too many tokens on boilerplate.

Whatever we write down has to actually shape agent behavior. Prose docs that nobody enforces are useless. The workflow also can't be so heavy that planning eats the session before any code lands.

One more thing: small tweaks shouldn't have to ride the whole pipeline. We need a clean way for the full process to collapse to something proportionate, without people silently bypassing it when it gets inconvenient.
