import uvicorn
from api.banners.handlers import banner_router
from fastapi import FastAPI

app = FastAPI(
    title="Сервис баннеров",
    version="1.0.0"
)

#
# def custom_openapi():
#     with open("api.yaml", "r") as file:
#         api_file = yaml.safe_load(file)
#     return api_file
#
#
# app.openapi = custom_openapi

app.include_router(banner_router)

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8003, reload=True)
