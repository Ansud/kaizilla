from pathlib import Path
from typing import Any
from unittest.mock import ANY, patch

from kaizilla import main
from source.models import ResponseData


@patch("source.processor.generate_metadata_for_image")
def test_parameters_description_passed(
    mock_generate_meta: Any, test_image_with_exif_description: Path, response_fixture_typed: ResponseData
) -> None:
    mock_generate_meta.return_value = response_fixture_typed
    file_path = str(test_image_with_exif_description)

    description_parameters = "This passed via parameters"

    main([file_path, "-d", description_parameters])
    mock_generate_meta.assert_called_once_with(ANY, description_parameters)


@patch("source.processor.generate_metadata_for_image")
def test_parameters_description_not_passed(
    mock_generate_meta: Any,
    test_image_with_exif_description: Path,
    exif_description: str,
    response_fixture_typed: ResponseData,
) -> None:
    mock_generate_meta.return_value = response_fixture_typed
    file_path = str(test_image_with_exif_description)

    main([file_path])
    mock_generate_meta.assert_called_once_with(ANY, exif_description)
