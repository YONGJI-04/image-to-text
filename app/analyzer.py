import os
import base64
import httpx
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

DETAIL_PROMPTS = {
    "brief": "이미지를 간략하게 1-2문장으로 설명해주세요.",
    "normal": """이미지를 분석하여 다음 항목을 마크다운 형식으로 작성해주세요:
## 1. 전체 설명
(2-3문장으로 이미지를 묘사)
## 2. 주요 요소
(이미지에서 눈에 띄는 요소를 bullet point로)
## 3. 분위기/스타일
(색감, 톤, 전반적인 느낌을 표로 정리)
## 4. 키워드
(이미지를 나타내는 핵심 단어 5개를 백틱으로 표시)""",
    "detailed": """이미지를 심층 분석하여 다음 항목을 마크다운 형식으로 작성해주세요:
## 1. 전체 설명
(4-5문장으로 이미지를 상세 묘사)
## 2. 구성 요소 분석
(전경/중경/배경으로 나누어 각 요소 설명)
## 3. 색채 분석
(주요 색상, 색온도, 채도, 명도 분석)
## 4. 분위기 & 감정
(이미지가 전달하는 감정과 분위기)
## 5. 기술적 특징
(카메라 앵글, 조명, 구도, 렌즈 효과 등)
## 6. 키워드
(이미지를 나타내는 핵심 단어 10개를 백틱으로 표시)"""
}

def analyze_image_file(image_bytes: bytes, media_type: str, language: str = "ko", detail: str = "normal") -> dict:
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    lang_instruction = "한국어로 답변해주세요." if language == "ko" else "Please answer in English."
    prompt_text = DETAIL_PROMPTS.get(detail, DETAIL_PROMPTS["normal"])
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}},
                {"type": "text", "text": f"{lang_instruction}\n\n{prompt_text}"}
            ]
        }]
    )
    return {"description": message.content[0].text, "detail": detail}

def analyze_image_url(url: str, language: str = "ko", detail: str = "normal") -> dict:
    with httpx.Client(timeout=30) as http:
        resp = http.get(url)
        resp.raise_for_status()
    content_type = resp.headers.get("content-type", "image/jpeg")
    media_type = content_type.split(";")[0].strip()
    return analyze_image_file(resp.content, media_type, language, detail)
