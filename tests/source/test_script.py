from pathlib import Path
from typing import Any
from unittest.mock import patch

from kaizilla import main
from source.models import ResponseData

from .test_metadata import validate_image_metadata


@patch("source.processor.generate_metadata_for_image")
def test_parameters_description_passed(
    mock_generate_meta: Any, test_image_with_exif_description: Path, response_fixture_messy_typed: ResponseData
) -> None:
    mock_generate_meta.return_value = response_fixture_messy_typed
    file_path = str(test_image_with_exif_description)

    main([file_path, "-c"])

    mock_generate_meta.assert_called_once()

    validate_image_metadata(
        image_path=test_image_with_exif_description,
        description_long=response_fixture_messy_typed.description.wiki.en,
        description_short=response_fixture_messy_typed.description.stock.en,
        keywords=["keyword with spaces", "strip it", "1", "2", "3"],
    )
