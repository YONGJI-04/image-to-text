# Image to Text

이미지를 업로드하면 **Claude Vision**이 전체 설명, 주요 요소, 분위기, 키워드를 한국어/영어로 분석해주는 API

---

## 프로젝트 개요

이미지 한 장을 업로드하면 Claude Vision이 이미지를 깊이 있게 분석하여 구조화된 텍스트로 반환합니다. Text to Image 파이프라인의 역방향 프로세스로, 시각 정보를 언어로 변환하는 기능을 구현합니다.

---

## 아키텍처

```
이미지 입력 (파일 업로드 또는 URL)
            ↓
    Base64 인코딩 처리
            ↓
    [ Claude Vision API ]
    claude-sonnet-4-6
    이미지 멀티모달 분석
            ↓
    전체 설명 / 주요 요소 / 분위기 / 키워드 반환
```

---

## 사용 기술 스택

| 기술 | 역할 |
|------|------|
| **Claude Vision** (claude-sonnet-4-6) | 이미지 멀티모달 분석 |
| **FastAPI** | REST API 서버 |
| **Pillow** | 이미지 처리 |

---

## 분석 항목

| 항목 | 설명 |
|------|------|
| **전체 설명** | 이미지 전반적인 내용 (2-3문장) |
| **주요 요소** | 이미지에서 눈에 띄는 요소 목록 |
| **분위기/스타일** | 색감, 톤, 전반적인 느낌 |
| **키워드** | 이미지를 나타내는 핵심 단어 5개 |

---

## 디렉토리 구조

```
image-to-text/
├── app/
│   ├── main.py       # FastAPI 서버 및 엔드포인트
│   └── analyzer.py   # Claude Vision 이미지 분석 모듈
├── requirements.txt
├── .env.example
└── README.md
```

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 서버 상태 확인 |
| `POST` | `/analyze/file` | 이미지 파일 업로드 분석 |
| `POST` | `/analyze/url` | 이미지 URL로 분석 |
| `GET` | `/docs` | Swagger UI |

---

## 요청 / 응답 예시

### 파일 업로드

```bash
curl -X POST "http://localhost:8000/analyze/file?language=ko" \
  -F "file=@image.jpg"
```

### URL 분석

```bash
curl -X POST http://localhost:8000/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/photo.jpg", "language": "ko"}'
```

**응답:**

```json
{
  "filename": "image.jpg",
  "language": "ko",
  "description": "## 1. 전체 설명\n사이버펑크 스타일의 미래 도시 야경입니다...\n\n## 2. 주요 요소\n- 네온사인\n- 고층 빌딩\n...\n\n## 3. 분위기/스타일\n| 항목 | 내용 |\n|------|------|\n| 주조색 | 청록, 네온 레드 |\n\n## 4. 키워드\n`사이버펑크` `야경` `미래도시` `네온` `AI아트`"
}
```

---

## 지원 형식

- **파일 형식**: JPG, PNG, GIF, WEBP
- **최대 크기**: 5MB
- **언어**: `ko` (한국어), `en` (영어)

---

## 실행 방법

```bash
cp .env.example .env
# .env에 ANTHROPIC_API_KEY 입력

pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8001
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 |
