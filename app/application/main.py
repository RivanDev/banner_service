from application.api.banners.handlers import banner_router
from fastapi import FastAPI

#
# def custom_openapi():
#     with open("api.yaml", "r") as file:
#         api_file = yaml.safe_load(file)
#     return api_file
#
#


def create_app() -> FastAPI:
    app = FastAPI(title="Сервис баннеров", version="1.0.0", debug=True)
    app.include_router(banner_router, prefix="/banner")
    # app.openapi = custom_openapi
    return app
