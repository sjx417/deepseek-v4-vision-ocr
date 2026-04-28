"""OCR image to text using Tesseract CLI. Usage: python ocr_image.py <image_path> [--lang chi_sim+eng]"""
import os
import shutil
import sys
import subprocess
from pathlib import Path


def _find_tesseract():
    # 1. Explicit env var
    if "TESSERACT_CMD" in os.environ:
        p = os.environ["TESSERACT_CMD"]
        if os.path.isfile(p):
            return p

    # 2. Look in PATH
    found = shutil.which("tesseract")
    if found:
        return found

    # 3. Common install locations
    candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
        "/opt/homebrew/bin/tesseract",
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p

    return "tesseract"  # fallback, let subprocess fail with clear error


TESSERACT = _find_tesseract()


def ocr(image_path: str, lang: str = "chi_sim+eng", psm: int = 6) -> str:
    """Run Tesseract OCR on an image and return recognized text."""
    result = subprocess.run(
        [TESSERACT, image_path, "stdout", "-l", lang, "--psm", str(psm)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def available_langs():
    result = subprocess.run(
        [TESSERACT, "--list-langs"],
        capture_output=True, text=True, encoding="utf-8"
    )
    # Tesseract lists langs as: "List of available languages ... (N):\nlang1\nlang2"
    lines = result.stdout.strip().split("\n")
    return [l for l in lines[1:] if l and not l.startswith("List")]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_image.py <image_path> [--lang chi_sim+eng] [--psm 6]")
        sys.exit(1)

    path = sys.argv[1]
    if not Path(path).exists():
        print(f"File not found: {path}")
        sys.exit(1)

    langs = available_langs()
    if "chi_sim" in langs:
        default_lang = "chi_sim+eng"
    else:
        default_lang = langs[0] if langs else "eng"

    lang = default_lang
    psm = 6
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--lang" and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
        elif args[i].startswith("--lang="):
            lang = args[i].split("=", 1)[1]
            i += 1
        elif args[i] == "--psm" and i + 1 < len(args):
            psm = int(args[i + 1])
            i += 2
        elif args[i].startswith("--psm="):
            psm = int(args[i].split("=", 1)[1])
            i += 1
        else:
            i += 1

    try:
        result = ocr(path, lang, psm)
        print(result)
    except Exception as e:
        print(f"OCR failed: {e}", file=sys.stderr)
        sys.exit(1)
