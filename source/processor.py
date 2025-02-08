import base64
import sys
from io import BytesIO
from pathlib import Path

import exiv2
from PIL import Image

from .llm import generate_metadata_for_image
from .metadata import get_image_description, set_image_description, set_image_keywords
from .models import CriticismData
from .settings import settings


def process_image(image_path: Path) -> CriticismData:
    buffered = BytesIO()
    image_path_str = str(image_path)

    # Get image metadata to process
    image = exiv2.ImageFactory.open(image_path_str)
    image.readMetadata()

    # Image must have description to point LLM to right way
    description = get_image_description(image)

    if description is None:
        print(f"Image {image_path} has no description", file=sys.stderr)  # noqa:T201
        return CriticismData()

    # Create image thumbnail, it is not good idea to send megabytes of data to OpenAI LLM, it is costly
    with Image.open(image_path_str) as image_file:
        image_file.thumbnail(size=(settings.THUMBNAIL_MAX_SIZE_X, settings.THUMBNAIL_MAX_SIZE_Y))
        image_file.save(buffered, "JPEG")
        # Encode image to base64 to allow LLM "see" it
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")

    generated_data = generate_metadata_for_image(encoded, description)

    set_image_description(image, generated_data.description.wiki.en, generated_data.description.stock.en)
    set_image_keywords(image, generated_data.keywords)

    image.writeMetadata()

    return generated_data.criticism
