# DeepAgents + Ollama + No‑Key Web Search (DuckDuckGo)

This document contains **the full, unsummarized setup and guidance** for
using:

-   **DeepAgents**
-   **Ollama (local models)**
-   **No‑API‑key web search (DuckDuckGo)**
-   Models: **llama3.1, Mistral, tinyllama**

Nothing is omitted or summarized.

------------------------------------------------------------------------

## Core Idea

Local models **do not access the internet directly**.

Instead:

1.  The LLM decides when it needs fresh information
2.  It calls a **tool** (e.g. `web_search`, `fetch_url`)
3.  Your Python code executes the HTTP request
4.  The result is sent back to the model
5.  The model reasons over the retrieved content

This is **tool calling / agent orchestration**, not browsing.

------------------------------------------------------------------------

## Why DeepAgents

DeepAgents is a LangGraph-based agent framework that provides:

-   Planning and task decomposition
-   Persistent state (threads)
-   Built-in support for subagents
-   Tool orchestration without boilerplate

It is well-suited for: - Web research - Long-running tasks - Multi-step
reasoning - Avoiding context bloat

------------------------------------------------------------------------

## Important Note About Web Search

DeepAgents ships with built-in tools like `web_search`, but:

-   These **default to Tavily**
-   Tavily **requires an API key**
-   Without `TAVILY_API_KEY`, built-in web search is disabled

Therefore, for **no-key operation**, we must provide **custom tools**.

------------------------------------------------------------------------

## Requirements

-   Python 3.10+
-   Ollama running locally
-   At least one tool-capable model
-   No external API keys

------------------------------------------------------------------------

## Install Dependencies (No API Keys)

``` bash
pip install -U   deepagents   langchain-ollama   langchain-community   duckduckgo-search   requests   beautifulsoup4
```

------------------------------------------------------------------------

## Custom No‑Key Tools

### DuckDuckGo Web Search Tool

``` python
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

ddg = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo (no API key required)."""
    return ddg.invoke(query)
```

### URL Fetch + Text Extraction Tool

``` python
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

@tool
def fetch_url(url: str, max_chars: int = 8000) -> str:
    """Fetch a webpage and return readable text."""
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    return text[:max_chars]
```

------------------------------------------------------------------------

## DeepAgents + Ollama Agent Setup

``` python
from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

agent = create_deep_agent(
    model=llm,
    tools=[web_search, fetch_url],
    system_prompt=(
        "You have web_search and fetch_url tools. "
        "For any factual or time-sensitive question, "
        "you MUST search the web, open relevant sources, "
        "and answer with sources."
    ),
)
```

### Running the Agent

``` python
result = agent.invoke(
    {
        "messages": [
            (
                "user",
                "Find recent changes in Ollama tool-calling support and summarize with sources."
            )
        ]
    },
    config={"configurable": {"thread_id": "demo"}},
)

print(result["messages"][-1].content)
```

------------------------------------------------------------------------

## Model‑Specific Behavior and Recommendations

### llama3.1

-   Best overall choice for agents
-   Most reliable tool calling
-   Follows system prompts well
-   Handles multi-step reasoning cleanly

Recommended: - `temperature = 0` - Use as **main agent**

------------------------------------------------------------------------

### Mistral

-   Generally good tool calling
-   More likely to answer "from memory" if not pushed
-   Benefits from stronger instructions

Recommended system prompt additions: - "You MUST use web_search for
factual or time-sensitive queries" - "Do not answer until at least one
source is opened"

------------------------------------------------------------------------

### tinyllama

-   Weak at tool calling
-   Poor at planning and multi-step reasoning
-   Easily ignores tools

Best use: - As a **worker model** - Summarize fetched text - Compress
long documents

Not recommended as: - Main DeepAgent - Planner - Research agent

------------------------------------------------------------------------

## Recommended Multi‑Model Pattern

### High‑Reliability Setup

-   **Main agent**: llama3.1 or Mistral
    -   Decides when to search
    -   Calls `web_search`
    -   Chooses URLs
    -   Calls `fetch_url`
-   **Optional summarizer**: tinyllama
    -   Receives fetched page text
    -   Produces short summaries
    -   Reduces context size

This pattern is: - Faster - Cheaper - More reliable

------------------------------------------------------------------------

## Common Failure Modes

-   Model never calls tools → hallucinated answers
-   Model answers before searching
-   Long webpages overflow context
-   Weak models ignore instructions

Mitigations: - Strong system prompts - Truncate fetched content - Use
llama3.1 for planning - Use tinyllama only for summarization

------------------------------------------------------------------------

## Optional Enhancements

-   Add a research subagent
-   Add citation enforcement
-   Cache search results
-   Replace DuckDuckGo with SearXNG
-   Add domain allowlists
-   Persist memory across runs

------------------------------------------------------------------------

## Summary (Conceptual, Not Condensed)

-   Ollama runs local models only
-   Internet access happens via tools
-   DeepAgents orchestrates tools
-   DuckDuckGo enables no-key search
-   llama3.1 is best for agents
-   Mistral works with stronger prompts
-   tinyllama is best as a worker

------------------------------------------------------------------------

End of document.
