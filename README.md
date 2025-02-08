# kaizilla
Small project to add descriptions and keywords to images with help of OpenAI LLM. Image itself is not affected anyhow, only EXIF, IPTC and XMP metadata is changed.

Please note that you need to set description in EXIF data first, LLM can not deduce good image description just from image itself. You better to provide some meaningful description to direct model right path.

## Preparation

First of all you need to get OpenAI key to work with LLM. Use it as usual, set OPENAI_API_KEY in terminal like this
```bash
export OPENAI_API_KEY="your_api_key_here"
```

Create virtual environment (if you want) and install packages from requirements.txt
```bash
pip install -r requirements.txt
```

## Execute script
You can just put metadata into image
```bash
python3 kaizilla path_to_your_image.jpg
```

You can get some criticism from LLM about your image if you run script with `-c` or `--criticism` flag
```bash
python3 kaizilla --criticism path_to_your_image.jpg
```

## Badges

[![Super-Linter](https://github.com/Ansud/kaizilla/actions/workflows/superlinter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Ansud/kaizilla)
![GitHub top language](https://img.shields.io/github/languages/top/Ansud/kaizilla)
