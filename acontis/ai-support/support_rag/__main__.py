"""`python -m support_rag` — runs uvicorn."""

import uvicorn

from support_rag.config import load_config


def main() -> None:
    config = load_config()
    host, port_s = config.service.bind.rsplit(":", 1)
    uvicorn.run("support_rag.app:app", host=host, port=int(port_s), workers=1)


if __name__ == "__main__":
    main()
