# Ollama Know-How

## Table of Contents

- [Basic Ollama Setup (CLI-Based)](#basic-ollama-setup-cli-based)
  - [1. Install Ollama](#1-install-ollama)
  - [2. Pull a Model](#2-pull-a-model)
  - [3. Start the Server](#3-start-the-server)
- [Using Ollama in LangChain (Replace OpenAI Model Usage)](#using-ollama-in-langchain-replace-openai-model-usage)
  - [Option A: Use `ChatOllama` (Native Ollama)](#option-a-use-chatollama-native-ollama)
  - [Option B: Keep `ChatOpenAI` and Point It at Ollama](#option-b-keep-chatopenai-and-point-it-at-ollama)
  - [Summary](#summary)

---

## Basic Ollama Setup (CLI-Based)

*Adapted from [AnythingLLM-LocalLLM-Tutorial](../anythingllm/BasicArchitecture/AnythingLLM-LocalLLM-Tutorial.md).*

If you prefer a lighter-weight solution than LM Studio:

### 1. Install Ollama

**Windows (PowerShell):**

```powershell
# Download from https://ollama.com and run the installer
# Or use winget:
winget install Ollama.Ollama
```

**Linux / macOS:**  
Download from [https://ollama.com](https://ollama.com) and follow the installer for your platform.

### 2. Pull a Model

```bash
# Best for code review on CPU
ollama pull qwen2.5-coder:7b

# Alternative: smaller model for lower RAM
ollama pull qwen2.5-coder:3b

# Alternative: DeepSeek Coder
ollama pull deepseek-coder-v2:lite
```

### 3. Start the Server

Ollama runs automatically as a service. The API is available at:

- **Local:** `http://localhost:11434`
- **Remote:** `http://<host>:11434` when Ollama runs on another machine (ensure the host is reachable and, if needed, that Ollama is bound to `0.0.0.0` or the desired interface).

---

## Using Ollama in LangChain (Replace OpenAI Model Usage)

If your code currently uses the OpenAI API (e.g. `ChatOpenAI` with an API key) in LangChain, you can switch to Ollama **without changing the rest of your chain**. Two options:

### Option A: Use `ChatOllama` (Native Ollama)

Use LangChain’s Ollama chat model. No API key; point `base_url` at your Ollama server (local or remote).

**Install:**

```bash
pip install langchain-community
```

**Example (local Ollama):**

```python
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(
    model="qwen2.5-coder:7b",  # same name as in `ollama list`
    base_url="http://localhost:11434",
)
response = llm.invoke("Explain prompt engineering in one sentence.")
print(response.content)
```

**Example (Ollama on another machine):**

```python
llm = ChatOllama(
    model="qwen2.5-coder:7b",
    base_url="http://192.168.1.100:11434",  # replace with your Ollama host
)
```

Then use `llm` anywhere you would use a LangChain LLM (e.g. `llm.invoke(...)`, chains, agents). No `OPENAI_API_KEY` needed.

---

### Option B: Keep `ChatOpenAI` and Point It at Ollama

Ollama exposes an **OpenAI-compatible** API under `/v1`. You can keep using `ChatOpenAI` and only change the base URL and model name.

**Example (local Ollama):**

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen2.5-coder:7b",           # use the Ollama model name
    base_url="http://localhost:11434/v1",
    api_key="ollama",                   # placeholder; Ollama does not validate it
)
response = llm.invoke("Explain prompt engineering in one sentence.")
print(response.content)
```

**Example (Ollama on another machine):**

```python
llm = ChatOpenAI(
    model="qwen2.5-coder:7b",
    base_url="http://192.168.1.100:11434/v1",  # replace with your Ollama host
    api_key="ollama",
)
```

**Replacing the setup in a notebook (e.g. intro prompt-engineering lesson):**

- **Before (OpenAI):**  
  `os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')` and `llm = ChatOpenAI(model="gpt-4o-mini")`.

- **After (Ollama, Option B):**  
  Omit or ignore `OPENAI_API_KEY`, and use:

  ```python
  llm = ChatOpenAI(
      model="qwen2.5-coder:7b",
      base_url="http://localhost:11434/v1",   # or your remote Ollama URL
      api_key="ollama",
  )
  ```

All other code (prompts, `invoke`, chains) stays the same.

---

### Summary

| Aspect              | Option A: `ChatOllama`     | Option B: `ChatOpenAI` + base_url   |
|---------------------|----------------------------|-------------------------------------|
| Package             | `langchain-community`      | `langchain-openai` (already in use) |
| API key             | Not needed                 | Any placeholder (e.g. `"ollama"`)   |
| Base URL            | `http://host:11434`        | `http://host:11434/v1`              |
| Model name          | Same as `ollama list`      | Same as `ollama list`               |
| Best when           | You prefer native Ollama   | You want minimal code change        |

For remote Ollama, use the other machine’s host (or IP) in `base_url` and ensure the server is reachable on port `11434`.
