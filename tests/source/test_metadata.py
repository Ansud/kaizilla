from pathlib import Path

from source.metadata import ImageMetadata


def test_get_description_not_present(test_image: Path) -> None:
    with ImageMetadata(test_image) as meta:
        assert meta.get_description() is None


def test_get_description_exif(test_image_with_exif_description: Path) -> None:
    with ImageMetadata(test_image_with_exif_description) as meta:
        assert meta.get_description() == "Test description exif"


def test_get_description_iptc(test_image_with_iptc_description: Path) -> None:
    with ImageMetadata(test_image_with_iptc_description) as meta:
        assert meta.get_description() == "Test description iptc"


def test_get_description_xmp(test_image_with_xmp_description: Path) -> None:
    with ImageMetadata(test_image_with_xmp_description) as meta:
        assert meta.get_description() == 'lang="x-default" Test description xmp'
