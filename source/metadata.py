from pathlib import Path
from typing import ClassVar, cast

import exiv2


class ImageMetadata:
    EXIF_DESCRIPTION_KEY: ClassVar[str] = "Exif.Image.ImageDescription"
    IPTC_DESCRIPTION_KEY: ClassVar[str] = "Iptc.Application2.ObjectName"
    XMP_DESCRIPTION_KEY: ClassVar[str] = "Xmp.dc.description"
    IPTC_LONG_DESCRIPTION_KEY: ClassVar[str] = "Iptc.Application2.Caption"
    XMP_LONG_DESCRIPTION_KEY: ClassVar[str] = "Xmp.dc.title"

    IPTC_KEYWORDS_KEY: ClassVar[str] = "Iptc.Application2.Keywords"
    XMP_KEYWORDS_KEY: ClassVar[str] = "Xmp.dc.subject"

    XMP_LANGUAGE: ClassVar[str] = 'lang="x-default"'

    def __init__(self, image_path: Path) -> None:
        self.image = exiv2.ImageFactory.open(str(image_path))
        self.image.readMetadata()

    def get_description(self) -> str | None:
        def _get_description(data: exiv2.IptcData | exiv2.ExifData | exiv2.XmpData, key: str) -> str | None:
            try:
                # exiv2 data has no 'get' method, so we need to use the key directly and catch exceptions
                description = data[key]
                return cast(str, description.toString())
            except KeyError:
                return None

        description = (
            _get_description(self.image.exifData(), self.EXIF_DESCRIPTION_KEY)
            or _get_description(self.image.iptcData(), self.IPTC_DESCRIPTION_KEY)
            or _get_description(self.image.xmpData(), self.XMP_DESCRIPTION_KEY)
        )

        # Catch empty strings too
        if not description:
            return None

        return description

    def set_description(self, long_description: str, short_description: str) -> None:
        exif_data = self.image.exifData()
        iptc_data = self.image.iptcData()
        xmp_data = self.image.xmpData()

        exif_data[self.EXIF_DESCRIPTION_KEY] = short_description
        iptc_data[self.IPTC_DESCRIPTION_KEY] = short_description[:64]
        iptc_data[self.IPTC_LONG_DESCRIPTION_KEY] = long_description[:2000]
        xmp_data[self.XMP_DESCRIPTION_KEY] = f"{self.XMP_LANGUAGE} {short_description}"
        xmp_data[self.XMP_LONG_DESCRIPTION_KEY] = f"{self.XMP_LANGUAGE} {long_description}"

        self.image.setExifData(exif_data)
        self.image.setIptcData(iptc_data)
        self.image.setXmpData(xmp_data)

    def set_keywords(self, keywords: list[str]) -> None:
        iptc_data = self.image.iptcData()
        xmp_data = self.image.xmpData()

        try:
            # Delete all existing keywords, this key can be in metadata multiple times, so do it until no more left
            while True:
                del iptc_data[self.IPTC_KEYWORDS_KEY]
        except KeyError:
            pass

        try:
            del xmp_data[self.XMP_KEYWORDS_KEY]
        except KeyError:
            pass

        # A bit weird exiv2 API to add multiple keys, why there is no add with list?
        key = exiv2.IptcKey(self.IPTC_KEYWORDS_KEY)

        for k in keywords:
            value = exiv2.StringValue()
            value.read(k)
            iptc_data.add(key, value)

        # This key should have semicolon separated keywords
        xmp_data[self.XMP_KEYWORDS_KEY] = "; ".join(keywords)

        self.image.setIptcData(iptc_data)
        self.image.setXmpData(xmp_data)

    def sync(self) -> None:
        self.image.writeMetadata()
