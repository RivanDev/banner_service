import uvicorn
import yaml
from fastapi import FastAPI

from application.api.banners.handlers import banner_router, user_banner_router


def custom_openapi():
    with open("/app/application/api.yaml", "r") as file:
        api_file = yaml.safe_load(file)
    return api_file


def create_app() -> FastAPI:
    app = FastAPI(title="Сервис баннеров", version="1.0.0", debug=True)
    app.include_router(user_banner_router, prefix="/user_banner")
    app.include_router(banner_router, prefix="/banner")
    # app.openapi = custom_openapi
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
