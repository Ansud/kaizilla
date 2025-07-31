from pathlib import Path

import exiv2

from source.metadata import ImageMetadata


def validate_image_metadata(
    image_path: Path, description_short: str, description_long: str, keywords: list[str]
) -> None:
    image = exiv2.ImageFactory.open(str(image_path))
    image.readMetadata()

    exif = image.exifData()
    iptc = image.iptcData()
    xmp = image.xmpData()

    assert exif[ImageMetadata.EXIF_DESCRIPTION_KEY].toString() == description_short
    assert iptc[ImageMetadata.IPTC_DESCRIPTION_KEY].toString() == description_short
    assert xmp[ImageMetadata.XMP_DESCRIPTION_KEY].toString() == f"{ImageMetadata.XMP_LANGUAGE} {description_short}"
    assert iptc[ImageMetadata.IPTC_LONG_DESCRIPTION_KEY].toString() == description_long
    assert xmp[ImageMetadata.XMP_LONG_DESCRIPTION_KEY].toString() == f"{ImageMetadata.XMP_LANGUAGE} {description_long}"

    keywords_set = set(keywords)
    xmp_keywords = set(xmp[ImageMetadata.XMP_KEYWORDS_KEY].toString().split("; "))
    keywords_key = exiv2.IptcKey(ImageMetadata.IPTC_KEYWORDS_KEY)
    keywords_iptc = {item.toString() for item in iptc.findKey(keywords_key)}

    assert keywords_set == keywords_iptc
    assert keywords_set == xmp_keywords


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


def test_not_saved_with_exception(test_image_with_exif_description: Path) -> None:
    try:
        with ImageMetadata(test_image_with_exif_description) as meta:
            meta.set_description("long description", "short description")
            raise ValueError
    except ValueError:
        pass

    with ImageMetadata(test_image_with_exif_description) as meta:
        assert meta.get_description() == "Test description exif"


def test_saved(test_image_with_exif_description: Path) -> None:
    new_description_long = "long description"
    new_description_short = "short description"
    keywords = ["keyword1", "keyword2"]

    with ImageMetadata(test_image_with_exif_description) as meta:
        meta.set_description(new_description_long, new_description_short)
        meta.set_keywords(keywords)

    validate_image_metadata(test_image_with_exif_description, new_description_short, new_description_long, keywords)
