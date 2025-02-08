from openai import OpenAI

from .models import ResponseData
from .prompt import IMAGE_DESCRIPTION_PROMPT
from .settings import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_metadata_for_image(image_data: str, description: str) -> ResponseData:
    response = openai_client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": [{"type": "text", "text": IMAGE_DESCRIPTION_PROMPT}]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": description},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                ],
            },
        ],
        max_tokens=1500,
    )

    if response.choices[0].message.content is None:
        raise NotImplementedError("Invalid response from OpenAI API")

    # TODO: Ask for retries if the response is not valid JSON
    return ResponseData.model_validate_json(response.choices[0].message.content)
