import json

from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger
from app.services.llm.base_llm_service import (
    BaseLLMService
)


class GroqLLMService(BaseLLMService):

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    def extract_fields(
        self,
        text: str,
        fields: list
    ):

        prompt = f"""
Extract the following fields from the document text.

Fields to extract:
{', '.join(fields)}

Rules:
- Return ONLY valid JSON
- Do NOT explain
- Do NOT guess
- If value not found, return null
- Format field names as snake_case

Document Text:
{text}

Return JSON object with extracted fields.
        """

        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=500
            )

            content = (
                response.choices[0]
                .message
                .content
            )

            logger.info(f"LLM Response: {content}")

            # Clean up potential markdown formatting
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            result = json.loads(content)
            logger.info("LLM extraction successful")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}")
            return {}
