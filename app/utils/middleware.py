import logging
import time
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request


logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5*1024*1024,
    backupCount=5,
    encoding="utf-8"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[file_handler, logging.StreamHandler()]
)


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        start_time = time.perf_counter()
        logger.info(
            f"Начало обработки {request.method} {request.url}"
        )
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            logger.info(
                f"Конец обработки {request.method} {request.url} - "
                f"Статус: {response.status_code} - "
                f"Время: {process_time:.4f} сек"
            )

            return response

        except Exception as exc:
            process_time = time.perf_counter() - start_time
            logger.error(
                f"Ошибка при обработке {request.method} {request.url} - "
                f"Время: {process_time:.4f} сек - "
                f"Ошибка: {str(exc)}"
            )
            raise exc
