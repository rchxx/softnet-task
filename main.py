import uvicorn
from config import AppConfig


if __name__ == "__main__":
    uvicorn.run(
        app="api.app:app", host=AppConfig.host, port=AppConfig.port, reload=True
    )
