import base64
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

from .llm import generate_metadata_for_image
from .metadata import ImageMetadata
from .models import CriticismData
from .settings import settings


def do_process_image(image_path: Path, meta: ImageMetadata, description_in: str | None) -> CriticismData:
    # Image must have description to point LLM to right way
    description = description_in or meta.get_description()

    if description is None:
        print(f"Image {image_path} has no description", file=sys.stderr)  # noqa:T201
        raise ValueError(f"Image {image_path} has no description")

    # Create image thumbnail, it is not good idea to send megabytes of data to OpenAI LLM, it is costly
    with Image.open(str(image_path)) as image_file:
        buffered = BytesIO()

        image_file.thumbnail(size=(settings.THUMBNAIL_MAX_SIZE_X, settings.THUMBNAIL_MAX_SIZE_Y))
        image_file.save(buffered, "JPEG")
        # Encode image to base64 to allow LLM "see" it
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")

    generated_data = generate_metadata_for_image(encoded, description)

    meta.set_description(generated_data.description.wiki.en, generated_data.description.stock.en)
    meta.set_keywords(generated_data.keywords)

    return generated_data.criticism


def process_image(image_path: Path, description_in: str | None) -> CriticismData:
    # Get image metadata to process
    with ImageMetadata(image_path) as image_meta:
        return do_process_image(image_path, image_meta, description_in)
