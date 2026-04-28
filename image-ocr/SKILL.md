---
name: image-ocr
description: Use this skill whenever the user sends an image and you cannot see it directly (e.g., you are running on a non-multimodal model like deepseek-v4-pro). This skill runs Tesseract OCR locally to extract text from images. Use when: the user pastes/sends an image, asks to "read" or "recognize" an image, or asks what's in a picture/screenshot. Also use when the user asks for OCR or text extraction from any image file.
---

# Image OCR

## When

The current model cannot process images directly. When the user sends an image, this skill extracts text from it using local Tesseract OCR.

## How

Run `scripts/ocr_image.py <image_path>` with appropriate language and PSM settings:

- Default: `chi_sim+eng` with PSM 3 (auto page segmentation)
- For screenshots with dense text: PSM 6
- For sparse text (book covers, signs): PSM 11
- English only: `--lang eng`
- Chinese only: `--lang chi_sim`

## PSM modes

| PSM | Description | Best for |
|-----|-------------|----------|
| 3 | Fully automatic | General purpose, most screenshots |
| 4 | Single column of text | Book pages with variable text sizes |
| 6 | Uniform block of text | Dense paragraphs |
| 11 | Sparse text | Covers, posters, UI elements |

## Script location

`scripts/ocr_image.py` — takes image path, outputs UTF-8 text to stdout.

## Notes

- Chinese output may display as garbled text in the bash terminal. Write to a file (`stdout` -> `/tmp/ocr_result.txt`) and read it instead.
- Tesseract is installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Available languages: `chi_sim`, `eng`, `osd`
