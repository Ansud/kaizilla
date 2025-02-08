from pathlib import Path

from .models import CriticismData


def process_image(image_path: Path) -> CriticismData:
    return CriticismData(improvements="improvements", strengths="strengths")
