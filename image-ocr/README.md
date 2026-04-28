# image-ocr

A Claude Code skill that gives non-multimodal models the ability to "see" images via local Tesseract OCR.

## Why

Claude's official models (Opus, Sonnet) have built-in vision. But if you use a third-party model without multimodal support (e.g., deepseek-v4-pro), images are invisible. This skill bridges the gap with local OCR — no API calls, no vision model required.

## How it works

When the user sends an image, the skill runs Tesseract OCR locally, extracts text, and returns it to the model. The model never "sees" the image — it reads the OCR result instead.

## Skill structure

```
image-ocr/
├── SKILL.md              # Skill metadata & usage instructions for Claude
└── scripts/
    └── ocr_image.py      # OCR script (Tesseract CLI wrapper)
```

## Installation

### 1. Install Tesseract OCR engine

```bash
# Windows (winget)
winget install tesseract-ocr.tesseract

# macOS
brew install tesseract

# Linux
sudo apt install tesseract-ocr
```

### 2. Install Python dependency

```bash
pip install pillow
```

### 3. (Optional) Add Chinese language support

Download `chi_sim.traineddata` from [tesseract-ocr/tessdata](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata) and place it in your Tesseract `tessdata` directory.

### 4. Install the skill

```bash
cp -r image-ocr /path/to/your/project/.claude/skills/
```

Or install globally:

```bash
cp -r image-ocr ~/.claude/skills/
```

## Usage

Once installed, the skill activates automatically when you send an image to Claude Code. No manual invocation needed.

You can also call the script directly:

```bash
# Default (Chinese + English, auto page segmentation)
python scripts/ocr_image.py screenshot.png

# English only
python scripts/ocr_image.py photo.jpg --lang eng

# Dense text paragraphs
python scripts/ocr_image.py document.png --psm 6

# Sparse text (covers, posters)
python scripts/ocr_image.py cover.png --psm 11
```

### PSM modes

| PSM | Description | Best for |
|-----|-------------|----------|
| 3 | Fully automatic | General purpose, screenshots |
| 4 | Single column | Book pages with variable text sizes |
| 6 | Uniform block | Dense paragraphs |
| 11 | Sparse text | Covers, posters, UI elements |

## Supported languages

Any [Tesseract language pack](https://github.com/tesseract-ocr/tessdata) can be used. Default supports:

- `eng` — English (included by default)
- `chi_sim` — Chinese Simplified (requires download)

## Requirements

- Tesseract OCR 5.x
- Python 3.8+
- Pillow

## License

MIT
