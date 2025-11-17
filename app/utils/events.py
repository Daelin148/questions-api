import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI


@asynccontextmanager
async def apply_migrations(app: FastAPI):
    print("Применяем миграции...")
    try:
        app_dir = Path(__file__).parent.parent
        subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=str(app_dir)
        )
    except Exception as e:
        print(f"Ошибка при применении миграций: {e}")
    print("Миграции применены")
    yield
