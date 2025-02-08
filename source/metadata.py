from typing import cast

import exiv2

EXIF_DESCRIPTION_KEY = "Exif.Image.ImageDescription"
IPTC_DESCRIPTION_KEY = "Iptc.Application2.ObjectName"
XMP_DESCRIPTION_KEY = "Xmp.dc.description"
IPTC_LONG_DESCRIPTION_KEY = "Iptc.Application2.Caption"
XMP_LONG_DESCRIPTION_KEY = "Xmp.dc.title"

IPTC_KEYWORDS_KEY = "Iptc.Application2.Keywords"
XMP_KEYWORDS_KEY = "Xmp.dc.subject"

XMP_LANGUAGE = 'lang="x-default"'


def get_image_description(image: exiv2.Image) -> str | None:
    def _get_description(data: exiv2.IptcData | exiv2.ExifData | exiv2.XmpData, key: str) -> str | None:
        try:
            # exiv2 data has no 'get' method, so we need to use the key directly and catch exceptions
            description = data[key]
            return cast(str, description.toString())
        except KeyError:
            return None

    description = (
        _get_description(image.exifData(), EXIF_DESCRIPTION_KEY)
        or _get_description(image.iptcData(), IPTC_DESCRIPTION_KEY)
        or _get_description(image.xmpData(), XMP_DESCRIPTION_KEY)
    )

    return description


def set_image_description(image: exiv2.Image, long_description: str, short_description: str) -> None:
    exif_data = image.exifData()
    iptc_data = image.iptcData()
    xmp_data = image.xmpData()

    exif_data[EXIF_DESCRIPTION_KEY] = short_description
    iptc_data[IPTC_DESCRIPTION_KEY] = short_description[:64]
    iptc_data[IPTC_LONG_DESCRIPTION_KEY] = long_description[:2000]
    xmp_data[XMP_DESCRIPTION_KEY] = f"{XMP_LANGUAGE} {short_description}"
    xmp_data[XMP_LONG_DESCRIPTION_KEY] = f"{XMP_LANGUAGE} {long_description}"

    image.setExifData(exif_data)
    image.setIptcData(iptc_data)
    image.setXmpData(xmp_data)


def set_image_keywords(image: exiv2.Image, keywords: list[str]) -> None:
    iptc_data = image.iptcData()
    xmp_data = image.xmpData()

    try:
        # Delete all existing keywords, this key can be in metadata multiple times, so do it until no more left
        while True:
            del iptc_data[IPTC_KEYWORDS_KEY]
    except KeyError:
        pass

    try:
        del xmp_data[XMP_KEYWORDS_KEY]
    except KeyError:
        pass

    # A bit weird exiv2 API to add multiple keys, why there is no add with list?
    key = exiv2.IptcKey(IPTC_KEYWORDS_KEY)

    for k in keywords:
        value = exiv2.StringValue()
        value.read(k)
        iptc_data.add(key, value)

    # This key should have semicolon separated keywords
    xmp_data[XMP_KEYWORDS_KEY] = "; ".join(keywords)

    image.setIptcData(iptc_data)
    image.setXmpData(xmp_data)
