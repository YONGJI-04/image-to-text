import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv
from analyzer import analyze_image_file, analyze_image_url

load_dotenv()

app = FastAPI(title="Image to Text API", description="Claude Vision으로 이미지를 텍스트로 변환", version="1.1.0")

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

class UrlRequest(BaseModel):
    url: str
    language: Literal["ko", "en"] = "ko"
    detail: Literal["brief", "normal", "detailed"] = "normal"

@app.get("/")
def root():
    return {"status": "running", "message": "Image to Text API - Claude Vision"}

@app.post("/analyze/file")
async def analyze_file(
    file: UploadFile = File(...),
    language: Literal["ko", "en"] = Query("ko"),
    detail: Literal["brief", "normal", "detailed"] = Query("normal"),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다 (JPG, PNG, GIF, WEBP)")
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="파일 크기는 5MB 이하여야 합니다")
    result = analyze_image_file(contents, file.content_type, language, detail)
    return {"filename": file.filename, "language": language, **result}

@app.post("/analyze/url")
def analyze_url(req: UrlRequest):
    try:
        result = analyze_image_url(req.url, req.language, req.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"url": req.url, "language": req.language, **result}

@app.get("/detail-levels")
def get_detail_levels():
    return {"levels": ["brief", "normal", "detailed"], "default": "normal"}
