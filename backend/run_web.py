import os

import uvicorn

from src.interfaces.web.app import create_fastapi_app, run


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    web_adapter = os.getenv("WEB_ADAPTER", "fastapi").strip().lower()
    if web_adapter == "stdlib":
        run(host=host, port=port)
    else:
        uvicorn.run(create_fastapi_app(), host=host, port=port)