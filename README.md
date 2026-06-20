# Image to Text API

이미지를 업로드하면 Claude Vision이 한국어/영어로 분석해주는 API

## 구조

```
이미지 입력 (파일 업로드 또는 URL)
        ↓
Claude Vision (이미지 분석)
        ↓
텍스트 설명 반환 (한국어/영어)
```

## 엔드포인트

- `POST /analyze/file` — 이미지 파일 업로드
- `POST /analyze/url` — 이미지 URL로 분석

## 실행 방법

```bash
cp .env.example .env  # API 키 입력
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001
```
