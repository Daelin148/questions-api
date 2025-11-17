from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.utils.events import apply_migrations
from app.utils.middleware import register_middleware

app = FastAPI(
    title=settings.app_name,
    lifespan=apply_migrations
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*']
)

register_middleware(app)

app.include_router(api_router, prefix='/api/v1')


@app.get('/')
async def main():
    return 'Тестовое задание в Хайталент'
