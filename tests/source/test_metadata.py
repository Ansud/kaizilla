from pathlib import Path

from source.metadata import ImageMetadata


def test_get_description_not_present(test_image: Path) -> None:
    result = ImageMetadata(test_image).get_description()
    assert result is None


def test_get_description_exif(test_image_with_exif_description: Path) -> None:
    result = ImageMetadata(test_image_with_exif_description).get_description()
    assert result == "Test description exif"


def test_get_description_iptc(test_image_with_iptc_description: Path) -> None:
    result = ImageMetadata(test_image_with_iptc_description).get_description()
    assert result == "Test description iptc"


def test_get_description_xmp(test_image_with_xmp_description: Path) -> None:
    result = ImageMetadata(test_image_with_xmp_description).get_description()
    assert result == 'lang="x-default" Test description xmp'
