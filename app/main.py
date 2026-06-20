import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from analyzer import analyze_image_file, analyze_image_url

load_dotenv()

app = FastAPI(title="Image to Text API")

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


class UrlRequest(BaseModel):
    url: str
    language: str = "ko"


@app.get("/")
def root():
    return {"status": "running", "message": "Image to Text API"}


@app.post("/analyze/file")
async def analyze_file(
    file: UploadFile = File(...),
    language: str = Query(default="ko", description="ko 또는 en"),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="JPG, PNG, GIF, WEBP 이미지만 지원합니다")

    image_bytes = await file.read()

    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 5MB 이하여야 합니다")

    result = analyze_image_file(image_bytes, file.content_type, language)

    return JSONResponse(content={
        "filename": file.filename,
        "language": result["language"],
        "description": result["description"],
    })


@app.post("/analyze/url")
def analyze_url(req: UrlRequest):
    if not req.url.startswith("http"):
        raise HTTPException(status_code=400, detail="올바른 URL을 입력해주세요")

    result = analyze_image_url(req.url, req.language)

    return JSONResponse(content={
        "url": req.url,
        "language": result["language"],
        "description": result["description"],
    })
