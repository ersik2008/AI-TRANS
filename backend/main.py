from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import asyncio
from pathlib import Path
from datetime import datetime
import logging

# ──────────────────────────────────────────────────────────────
# Логирование — чтобы видеть ВСЁ, что происходит в фоне
# ──────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-translate")

# ──────────────────────────────────────────────────────────────
# Импорты твоих сервисов
# ──────────────────────────────────────────────────────────────
from services.job_manager import JobManager
from services.media_processor import MediaProcessor

app = FastAPI(
    title="AI-Translate API",
    description="Media recognition and translation API",
    version="1.0.0"
)

# CORS — разрешаем всё (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Директория для загрузок
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Инициализация сервисов
job_manager = JobManager()
media_processor = MediaProcessor()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ──────────────────────────────────────────────────────────────
# ГЛАВНЫЙ ЭНДПОИНТ — теперь 100% не блокирует сервер
# ──────────────────────────────────────────────────────────────
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    target_language: str = Form(...),
    background_tasks: BackgroundTasks  # ← Это важно!
):
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="Файл не загружен")

        job_id = str(uuid.uuid4())
        job_dir = UPLOAD_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        file_path = job_dir / file.filename

        # Сохраняем файл
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"Файл сохранён: {file_path}")

        # Создаём задачу
        job_manager.create_job(
            job_id=job_id,
            file_path=str(file_path),
            target_language=target_language,
            original_filename=file.filename
        )

        # Запускаем обработку в фоне через BackgroundTasks (надёжнее, чем asyncio.create_task)
        background_tasks.add_task(
            safe_process_job,
            job_id,
            str(file_path),
            target_language
        )

        return {
            "job_id": job_id,
            "status": "queued",
            "message": "Файл принят в обработку"
        }

    except Exception as e:
        logger.error(f"Ошибка при загрузке: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────────
# Обёртка с try/except — чтобы задача НЕ УБИЛА весь сервер
# ──────────────────────────────────────────────────────────────
async def safe_process_job(job_id: str, file_path: str, target_lang: str):
    try:
        logger.info(f"Начинаем обработку job_id={job_id}")
        job_manager.set_processing(job_id)

        # Здесь вся тяжёлая работа
        await media_processor.process(job_id, file_path, target_lang)

        # Если дошло сюда — всё ок
        job_manager.set_completed(job_id)
        logger.info(f"Успешно завершено job_id={job_id}")

    except Exception as e:
        error_msg = f"Ошибка обработки: {str(e)}"
        logger.error(f"{error_msg} | job_id={job_id}")
        job_manager.set_failed(job_id, error_msg)


# ──────────────────────────────────────────────────────────────
# Остальные эндпоинты
# ──────────────────────────────────────────────────────────────
@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return job


@app.get("/api/jobs")
async def list_jobs():
    return {"jobs": job_manager.list_jobs()}


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    job_manager.delete_job(job_id)
    return {"message": "Задача удалена"}


# ──────────────────────────────────────────────────────────────
# Запуск (для разработки)
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)