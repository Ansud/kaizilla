import argparse
import sys
from pathlib import Path

from source import process_image


def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(
        description="Generate image description and keywords and put it into image metadata"
    )
    parser.add_argument("image_file", type=str, help="Image file to process [JPG]")
    parser.add_argument(
        "-d", "--description", type=str, help="Image initial description, if not provided, will be taken from metadata"
    )
    # TODO: Select criticism language
    parser.add_argument(
        "-c", "--criticism", action=argparse.BooleanOptionalAction, help="Display criticism about image"
    )

    arguments = parser.parse_args(args)

    image_file_path = Path(arguments.image_file)

    if not image_file_path.exists():
        print(f"File not found: {image_file_path}", file=sys.stderr)  # noqa:T201
        sys.exit(-1)

    try:
        criticism = process_image(arguments.image_file, arguments.description)
    except ValueError:
        sys.exit(-2)

    if arguments.criticism:
        print(f"Improvements: {criticism.improvements}")  # noqa:T201
        print(f"Strengths: {criticism.strengths}")  # noqa:T201


if __name__ == "__main__":
    main(sys.argv[1:])
