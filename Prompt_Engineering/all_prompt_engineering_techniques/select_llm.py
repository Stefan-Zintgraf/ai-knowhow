"""
Shared LLM selection for Jupyter notebooks.

Usage in a notebook:
    from select_llm import get_llm

    ollama_model = "llama3.2:1b"  # or None / "" / "none" for OpenAI
    llm = get_llm(ollama_model)
"""
import os

from dotenv import load_dotenv

load_dotenv()


def _get_ollama_base_url():
    """Resolve Ollama base URL from env or Docker fallback. Raises if unavailable."""
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    if not ollama_base_url:
        in_docker = os.path.exists("/.dockerenv") or os.path.exists(
            "/run/.containerenv"
        )
        if in_docker:
            ollama_base_url = "http://host.docker.internal:11434"
        else:
            raise RuntimeError(
                "OLLAMA_BASE_URL is not set and not running inside Docker. "
                "Set OLLAMA_BASE_URL (e.g. http://localhost:11434) or run inside Docker."
            )
    return ollama_base_url.rstrip("/")


def get_supported_ollama_models():
    """
    Return a list of Ollama model names (string array) from the remote Ollama server.

    Queries the Ollama API (OLLAMA_BASE_URL) for available models. Raises if
    Ollama is unreachable or OLLAMA_BASE_URL is not set.
    """
    import httpx

    base_url = _get_ollama_base_url()
    r = httpx.get(f"{base_url}/api/tags", timeout=5.0)
    r.raise_for_status()
    models = r.json().get("models", [])
    return [m["name"] for m in models]


def get_llm(ollama_model=None):
    """
    Return an LLM instance: ChatOllama if ollama_model is set, else ChatOpenAI.
    Returns None if the requested Ollama model is not found. Raises if Ollama is unreachable.

    ollama_model: e.g. "llama3.2:1b", or None / "" / "none" for OpenAI (gpt-4o-mini).
    """
    if ollama_model and str(ollama_model).strip().lower() != "none":
        ollama_base_url = _get_ollama_base_url()
        import httpx

        try:
            r = httpx.get(
                f"{ollama_base_url}/api/tags", timeout=5.0
            )
            r.raise_for_status()
            models = r.json().get("models", [])
            model_names = [m["name"] for m in models]
            if ollama_model not in model_names:
                available = ", ".join(model_names) if model_names else "none"
                print(f"Error: Ollama model '{ollama_model}' not found.")
                print(f"Available models: {available}")
                print(f"Pull the model with: ollama pull {ollama_model}")
                return None
        except httpx.HTTPError as e:
            print(f"Error: Could not reach Ollama at {ollama_base_url}: {e}")
            raise
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(
            model=ollama_model,
            base_url=ollama_base_url,
        )
    else:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model="gpt-4o-mini")
