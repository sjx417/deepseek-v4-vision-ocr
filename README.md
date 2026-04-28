# DeepSeek V4 Vision OCR

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tesseract](https://img.shields.io/badge/OCR-Tesseract%205.x-blue)](https://github.com/tesseract-ocr/tesseract)

> Let DeepSeek V4 "see" images — a Claude Code skill that adds local OCR capability to non-multimodal LLMs.

DeepSeek V4 is powerful, but it can't process images. This skill gives it eyes. When you paste a screenshot, photo, or scanned document into Claude Code, the skill runs Tesseract OCR locally, extracts the text, and feeds it to the model. No vision API, no cloud calls, fully offline.

## Quick start

```bash
# 1. Download the skill
git clone https://github.com/sjx417/deepseek-v4-vision-ocr.git

# 2. Copy to your Claude Code skills directory
cp -r deepseek-v4-vision-ocr/image-ocr ~/.claude/skills/

# 3. Install Tesseract (if not already installed)
# Windows: winget install tesseract-ocr.tesseract
# macOS:   brew install tesseract
# Linux:   sudo apt install tesseract-ocr

# 4. Install Python dependency
pip install pillow

# (Optional) Chinese language support: download chi_sim.traineddata
# from https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
# and place in your Tesseract tessdata directory.

# Done. Restart Claude Code, send an image, and the skill auto-activates.
```

## How it works

```
User sends image  →  Skill intercepts  →  Tesseract OCR (local)  →  Text returned to model
```

The model never "sees" the image — it reads the OCR result. This works with any non-multimodal model (DeepSeek V4, any text-only LLM).

## PSM modes

Different page segmentation modes for different image types:

| PSM | Best for |
|-----|----------|
| 3 | Screenshots, mixed content (default) |
| 4 | Book pages, single-column text |
| 6 | Dense paragraphs |
| 11 | Covers, posters, UI labels |

```bash
python scripts/ocr_image.py screenshot.png           # auto mode (chi_sim+eng)
python scripts/ocr_image.py photo.jpg --lang eng     # English only
python scripts/ocr_image.py book.png --psm 6         # dense text
python scripts/ocr_image.py cover.png --psm 11       # sparse text
```

## Requirements

- Tesseract OCR 5.x
- Python 3.8+
- Pillow

## License

MIT
