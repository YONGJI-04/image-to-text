import anthropic
import base64
import os


def analyze_image_file(image_bytes: bytes, media_type: str, language: str = "ko") -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    image_data = base64.standard_b64encode(image_bytes).decode("utf-8")

    lang_instruction = "한국어로 답변해주세요." if language == "ko" else "Please answer in English."

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"""이 이미지를 분석해서 다음 항목으로 나눠서 설명해주세요:

1. **전체 설명**: 이미지 전반적인 내용 (2-3문장)
2. **주요 요소**: 이미지에서 눈에 띄는 것들 (목록)
3. **분위기/스타일**: 색감, 톤, 전반적인 느낌
4. **키워드**: 이미지를 나타내는 핵심 단어 5개

{lang_instruction}""",
                    },
                ],
            }
        ],
    )

    return {
        "description": message.content[0].text,
        "language": language,
    }


def analyze_image_url(url: str, language: str = "ko") -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    lang_instruction = "한국어로 답변해주세요." if language == "ko" else "Please answer in English."

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": url,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"""이 이미지를 분석해서 다음 항목으로 나눠서 설명해주세요:

1. **전체 설명**: 이미지 전반적인 내용 (2-3문장)
2. **주요 요소**: 이미지에서 눈에 띄는 것들 (목록)
3. **분위기/스타일**: 색감, 톤, 전반적인 느낌
4. **키워드**: 이미지를 나타내는 핵심 단어 5개

{lang_instruction}""",
                    },
                ],
            }
        ],
    )

    return {
        "description": message.content[0].text,
        "language": language,
    }
