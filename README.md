# Image to Text

이미지를 업로드하면 Claude Vision이 한국어/영어로 상세 분석해주는 API

## 아키텍처

```
이미지 입력 (파일 업로드 또는 URL)
        ↓
Claude Vision (claude-sonnet-4-6)
        ↓
전체 설명 / 주요 요소 / 분위기 / 키워드 반환
```

## 분석 항목

1. **전체 설명** - 이미지 전반적인 내용 (2-3문장)
2. **주요 요소** - 이미지에서 눈에 띄는 것들
3. **분위기/스타일** - 색감, 톤, 전반적인 느낌
4. **키워드** - 핵심 단어 5개

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 서버 상태 확인 |
| POST | `/analyze/file` | 이미지 파일 업로드 분석 |
| POST | `/analyze/url` | 이미지 URL로 분석 |
| GET | `/docs` | Swagger UI |

## 요청 예시

```bash
# 파일 업로드
curl -X POST http://localhost:8000/analyze/file \
  -F "file=@image.jpg" \
  -F "language=ko"

# URL
curl -X POST http://localhost:8000/analyze/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.jpg", "language": "ko"}'
```

## 지원 형식

- JPG, PNG, GIF, WEBP
- 최대 파일 크기: 5MB
- 언어: `ko` (한국어), `en` (영어)

## 실행 방법

```bash
cp .env.example .env
pip install -r requirements.txt
cd app && uvicorn main:app --host 0.0.0.0 --port 8001
```

## 환경 변수

```
ANTHROPIC_API_KEY=   # Anthropic Claude API 키
```
