**One-off command** — run a single command with a specific version:
```bash
pyenv shell 3.12
python --version    # 3.12.x
```
This only affects the current shell session.

**Per-project** — sets the version for a directory automatically:
```bash
cd your-project
pyenv local 3.14
python --version    # 3.14.x, only in this folder
```
Creates a `.python-version` file in that directory. Any shell entering it will auto-switch.

**Global default** — changes the default across all shells:
```bash
pyenv global 3.12
```
> Be careful with this one — it overrides `python` everywhere. Your system 3.13 (`python3`) stays untouched regardless.

**Quick reference:**

| Command | Scope |
|---|---|
| `pyenv shell 3.12` | Current shell only |
| `pyenv local 3.14` | Current directory (and subdirs) |
| `pyenv global 3.12` | Everywhere (until changed) |
| `pyenv versions` | List all installed versions |
| `pyenv version` | Show currently active version |

For most cases, `pyenv local` per project is the cleanest approach.
