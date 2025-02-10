# kaizilla

Kaizilla is a small utility that enhances image metadata by adding descriptions and keywords using OpenAI's LLM. The image itself remains unchanged; only EXIF, IPTC, and XMP metadata are modified.

## Features

- Automatically generates and inserts meaningful descriptions and keywords into image metadata.
- Supports EXIF, IPTC, and XMP metadata formats.
- Optional critique mode to analyze the provided image
- Simple command-line usage.

## How It Works

Kaizilla does **not** generate descriptions purely from the image itself. You must provide an initial description in the EXIF metadata, which the LLM then refines and enhances with keywords. Providing meaningful input helps the model generate better results.

## Installation

### 1. Set Up OpenAI API Key

To use Kaizilla, you need an OpenAI API key. Set it in your terminal:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

You can also specify the OpenAI model to use by setting the `OPENAI_MODEL` environment variable. By default, Kaizilla uses `gpt-4o-mini`:

```bash
export OPENAI_MODEL="your_preferred_model"
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended) and install required packages:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Adding Metadata to an Image

Run the script to insert metadata into an image:

```bash
python3 kaizilla path_to_your_image.jpg
```

### Critique Mode

Enable critique mode to get feedback on the description:

```bash
python3 kaizilla.py --criticism path_to_your_image.jpg
```

You will receive a critique of the description, including suggestions for improvement. For example (output may vary):

**Improvements**: To enhance the photo's appeal, consider adjusting the contrast and vibrance to make the colors pop more. Including more foreground elements could also enhance depth.

**Strengths**: The serene composition and effective use of the winding path create a captivating visual journey. The lighting, emblematic of the golden hour, beautifully complements the natural environment.

## Supported Formats

Kaizilla supports JPEG image format and **may be** other formats that support EXIF, IPTC, and XMP metadata. However, metadata support may vary depending on the format and editing tools used.

## Command-Line Options

- `-c`, `--criticism` – Enables critique mode for analyzing the provided description.
- `-h`, `--help` – Displays usage instructions.

## License

Kaizilla is released under the GPL-3.0 license. See the [LICENSE](LICENSE) file for more information.

## Badges

[![Super-Linter](https://github.com/Ansud/kaizilla/actions/workflows/superlinter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit.com/main.svg)](https://results.pre-commit.ci/latest/github/Ansud/kaizilla/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Ansud/kaizilla)
![GitHub top language](https://img.shields.io/github/languages/top/Ansud/kaizilla)
[![Coverage Status](https://coveralls.io/repos/github/Ansud/kaizilla/badge.svg)](https://coveralls.io/github/Ansud/kaizilla)
