"""
Shared LLM selection for Jupyter notebooks.

Usage in a notebook:
    from select_llm import get_llm, OLLAMA_WIN_PORT, OLLAMA_MAC_PORT

    ollama_model = "llama3.2:1b"  # or None / "" / "none" for OpenAI
    llm = get_llm(ollama_model)  # prefers MAC (GPU)
    llm = get_llm(ollama_model, force_port=OLLAMA_WIN_PORT)  # force Windows
"""
import contextlib
import io
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

# Ports: Mac (VRAM/GPU) = 12434, Windows (no GPU) = 11434
OLLAMA_MAC_PORT = 12434
OLLAMA_WIN_PORT = 11434


def _ollama_host():
    """Return host for Ollama (localhost or host.docker.internal)."""
    in_docker = os.path.exists("/.dockerenv") or os.path.exists(
        "/run/.containerenv"
    )
    return "http://host.docker.internal" if in_docker else "http://localhost"


def _ollama_candidate_urls():
    """Return (mac_url, win_url) for current environment (Docker or host)."""
    host = _ollama_host()
    return (
        f"{host}:{OLLAMA_MAC_PORT}",
        f"{host}:{OLLAMA_WIN_PORT}",
    )


def _port_label(port):
    """Return human-readable label for known ports."""
    if port == OLLAMA_MAC_PORT:
        return "MAC"
    if port == OLLAMA_WIN_PORT:
        return "Windows"
    return f"port {port}"


def _fetch_ollama_models(base_url, timeout=5.0):
    """Return (reachable, model_names). model_names is [] if unreachable."""
    try:
        r = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=timeout)
        r.raise_for_status()
        models = r.json().get("models", [])
        return True, [m["name"] for m in models]
    except (httpx.HTTPError, Exception):
        return False, []


def _get_ollama_base_url(ollama_model=None, force_port=None):
    """
    Resolve Ollama base URL: from force_port, env, or by trying MAC first then Windows.
    When auto-detecting, prefers MAC (GPU/VRAM) over Windows. Always prints
    which backend is used when MAC or Windows is selected.

    force_port: If set (e.g. 11434 for Windows), use that port instead of auto-detect.
    """
    if force_port is not None:
        url = f"{_ollama_host()}:{force_port}"
        reachable, names = _fetch_ollama_models(url)
        if not reachable:
            raise RuntimeError(
                f"Ollama is not reachable at {url}. "
                "Ensure Ollama is running on the specified port."
            )
        if ollama_model and ollama_model not in names:
            raise ValueError(
                f"Ollama model '{ollama_model}' not found at {url}. "
                f"Pull the model with: ollama pull {ollama_model}"
            )
        print(f"Using Ollama on {_port_label(force_port)} (port {force_port}).")
        return url.rstrip("/")

    explicit = os.getenv("OLLAMA_BASE_URL", "").strip()
    if explicit:
        return explicit.rstrip("/")

    mac_url, win_url = _ollama_candidate_urls()
    # Prefer MAC (has VRAM) over Windows (no GPU)
    any_reachable = False
    for url, label, port in [
        (mac_url, "MAC", OLLAMA_MAC_PORT),
        (win_url, "Windows", OLLAMA_WIN_PORT),
    ]:
        reachable, names = _fetch_ollama_models(url)
        if reachable:
            any_reachable = True
        if reachable and (not ollama_model or ollama_model in names):
            print(f"Using Ollama on {label} (port {port}).")
            return url.rstrip("/")

    if any_reachable and ollama_model:
        raise ValueError(
            f"Ollama model '{ollama_model}' not found on MAC or Windows. "
            f"Pull the model with: ollama pull {ollama_model}"
        )
    raise RuntimeError(
        "Ollama is not reachable on MAC or Windows. "
        "Set OLLAMA_BASE_URL (e.g. http://localhost:11434) or use force_port=11434."
    )


def get_supported_ollama_models():
    """
    Return a list of Ollama model names (string array) from the remote Ollama server.

    Queries the Ollama API (OLLAMA_BASE_URL) for available models. Raises if
    Ollama is unreachable or OLLAMA_BASE_URL is not set.
    """
    base_url = _get_ollama_base_url()
    r = httpx.get(f"{base_url}/api/tags", timeout=5.0)
    r.raise_for_status()
    models = r.json().get("models", [])
    return [m["name"] for m in models]


def get_llm(ollama_model=None, force_port=None):
    """
    Return an LLM instance: ChatOllama if ollama_model is set, else ChatOpenAI.
    Prefers MAC (GPU/VRAM) over Windows when the model is available on both.
    Returns None if the requested Ollama model is not found. Raises if Ollama is unreachable.

    ollama_model: e.g. "llama3.2:1b", or None / "" / "none" for OpenAI (gpt-4o-mini).
    force_port: If set (e.g. 11434 for Windows), use that port instead of auto-detect.
    """
    if ollama_model and str(ollama_model).strip().lower() != "none":
        try:
            ollama_base_url = _get_ollama_base_url(ollama_model, force_port)
        except ValueError as e:
            print(f"Error: {e}")
            return None
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(
            model=ollama_model,
            base_url=ollama_base_url,
        )
    else:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model="gpt-4o-mini")


TEST_MODELS = [
    "tinyllama:latest",
    "llama3.2:1b",
    "deepseek-r1:14b",
    "qwen2.5-coder:14b",
    "deepseek-r1:7b",
    "qwen2.5-coder:7b",
    "mistral:latest",
]


def test_model_availability(models=None):
    """
    Check availability of models on MAC and Windows Ollama backends using get_llm.
    Prints which device each model was found on.
    """
    if models is None:
        models = TEST_MODELS
    # Check reachability: try first model on both ports
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            mac_ok = win_ok = False
            try:
                get_llm(models[0], force_port=OLLAMA_MAC_PORT)
                mac_ok = True
            except RuntimeError:
                pass
            try:
                get_llm(models[0], force_port=OLLAMA_WIN_PORT)
                win_ok = True
            except RuntimeError:
                pass
    if not mac_ok and not win_ok:
        print("Ollama is not reachable on MAC or Windows.")
        return
    print("Model availability:")
    for model in models:
        on_mac = False
        on_win = False
        with io.StringIO() as buf:
            with contextlib.redirect_stdout(buf):
                try:
                    if get_llm(model, force_port=OLLAMA_MAC_PORT) is not None:
                        on_mac = True
                except RuntimeError:
                    pass
                try:
                    if get_llm(model, force_port=OLLAMA_WIN_PORT) is not None:
                        on_win = True
                except RuntimeError:
                    pass
        if on_mac and on_win:
            print(f"  {model}: MAC, Windows")
        elif on_mac:
            print(f"  {model}: MAC")
        elif on_win:
            print(f"  {model}: Windows")
        else:
            print(f"  {model}: not found")


if __name__ == "__main__":
    test_model_availability()
