import itertools
from pathlib import Path

import exiv2
import pytest
from PIL import Image

from source.metadata import ImageMetadata

# mypy: allow-untyped-decorators

# Generate unique integers for run
autoincr = itertools.count().__next__


@pytest.fixture()
def response_fixture() -> dict[str, object]:
    response = {
        "reasoning": {"quality": ["I thought a bit."], "image_description_keywords": ["Some more thinking."]},
        "description": {
            "wiki": {"en": "This is good photo", "ru": "Хорошая фотография"},
            "stock": {"en": "This is photo", "ru": "Это фото"},
        },
        "keywords": ["1", "2", "3"],
        "criticism": {"improvements": "Do not do bad things", "strengths": "Do good things"},
    }

    return response


@pytest.fixture
def test_image(tmp_path: Path) -> Path:
    im = Image.frombytes("L", (10, 10), b"\x00" * 10 * 10)
    image_path = tmp_path / f"test_image_{autoincr()}.jpg"
    im.save(image_path)

    return image_path


@pytest.fixture
def test_image_with_exif_description(test_image: Path) -> Path:
    image = exiv2.ImageFactory.open(str(test_image))

    exif_data = image.exifData()
    exif_data[ImageMetadata.EXIF_DESCRIPTION_KEY] = "Test description exif"
    image.setExifData(exif_data)

    image.writeMetadata()
    return test_image


@pytest.fixture
def test_image_with_iptc_description(test_image: Path) -> Path:
    image = exiv2.ImageFactory.open(str(test_image))

    iptc_data = image.iptcData()
    iptc_data[ImageMetadata.IPTC_DESCRIPTION_KEY] = "Test description iptc"
    image.setIptcData(iptc_data)

    image.writeMetadata()
    return test_image


@pytest.fixture
def test_image_with_xmp_description(test_image: Path) -> Path:
    image = exiv2.ImageFactory.open(str(test_image))

    xmp_data = image.xmpData()
    xmp_data[ImageMetadata.XMP_DESCRIPTION_KEY] = "Test description xmp"
    image.setXmpData(xmp_data)

    image.writeMetadata()
    return test_image
