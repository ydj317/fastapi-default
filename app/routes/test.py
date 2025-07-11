from typing import List
import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from dependency_injector.wiring import Provide, inject
from playwright.async_api import async_playwright
from app.celery_worker import my_task
from app.core.settings import settings
from redis.asyncio import Redis
from app.core.containers import Container
from app.tasks.my_task import add
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from pathlib import Path

router = APIRouter()

@router.get("/test/scrape")
async def scrape(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()  # 페이지 전체 HTML 가져오기
        await browser.close()
        return {"html": content}

@router.get("/test/exception")
def rase_exception():
    raise Exception('rase exception!!!')

@router.get("/test/task/add")
def run_add_task(a: int, b: int):
    result = add.delay(a, b)
    return {"task_id": result.id}

@router.get("/test/task/result/{task_id}")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=my_task)

    if result.state == "PENDING":
        return {"status": "PENDING"}

    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}

    elif result.state == "FAILURE":
        return {"status": "FAILURE", "error": str(result.result)}

    else:
        return {"status": result.state}

@router.get("/test/redis")
@inject
async def test_redis(redis: Redis = Depends(Provide[Container.redis])):
    await redis.set("key", "value111")
    val = await redis.get("key")
    return {"key": val}


UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


@router.post("/test/upload-image")
async def upload_image(file: UploadFile = File(...)):

    filename = file.filename
    ext = filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 고유한 파일명 생성 (UUID 기반)
    new_filename = f"{uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / new_filename

    # 파일 저장
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return JSONResponse({
        "filename": new_filename,
        "url": f"/uploads/images/{new_filename}"
    })

@router.post("/test/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        filename = file.filename
        ext = filename.split(".")[-1].lower()

        # 확장자 검사
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {filename}")

        # 고유한 파일 이름 생성
        new_filename = f"{uuid4().hex}.{ext}"
        file_path = UPLOAD_DIR / new_filename

        # 파일 저장
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await f.write(chunk)

        saved_files.append({
            "original_filename": filename,
            "saved_filename": new_filename,
            "url": f"/uploads/images/{new_filename}"
        })

    return JSONResponse(content={"uploaded": saved_files})