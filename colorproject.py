"""
colorproject.py
Translates a text string into a sequence of coloured squares,
strongly inspired by the work of Christian Faur.

Christian Faur's "Crayon" alphabet assigns each of the 26 letters a unique
colour distributed evenly across the visible spectrum (violet → red).
Non-alphabetic characters are represented by a white square.
"""

import colorsys
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Colour alphabet
# ---------------------------------------------------------------------------

def _build_color_map() -> dict[str, tuple[int, int, int]]:
    """
    Build a mapping from each letter (upper and lower case) to an RGB colour.

    The 26 letters are spread evenly over the hue circle, starting at
    violet (hue ≈ 0.75) and advancing toward red, which closely mirrors
    Christian Faur's published colour alphabet.
    """
    color_map: dict[str, tuple[int, int, int]] = {}
    n = 26
    for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        # hue goes from 0.75 (violet) down to 0.0 (red) across 26 steps
        hue = (0.75 - i * 0.75 / (n - 1)) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        rgb = (int(r * 255), int(g * 255), int(b * 255))
        color_map[letter] = rgb
        color_map[letter.lower()] = rgb
    return color_map


COLOR_MAP: dict[str, tuple[int, int, int]] = _build_color_map()

# Colour used for non-alphabetic characters (space, punctuation, digits …)
DEFAULT_COLOR: tuple[int, int, int] = (255, 255, 255)


def letter_to_color(letter: str) -> tuple[int, int, int]:
    """Return the RGB colour assigned to *letter*.

    Non-alphabetic characters return ``DEFAULT_COLOR`` (white).
    """
    return COLOR_MAP.get(letter, DEFAULT_COLOR)


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def text_to_image(
    text: str,
    square_size: int = 50,
    padding: int = 4,
    squares_per_row: int = 0,
) -> Image.Image:
    """Render *text* as a grid of coloured squares and return a PIL Image.

    Parameters
    ----------
    text:
        The input string to encode.
    square_size:
        Side length of each coloured square in pixels (default 50).
    padding:
        Gap between adjacent squares in pixels (default 4).
    squares_per_row:
        How many squares fit in one row.  When 0 (default) all characters
        are placed on a single row.
    """
    if not text:
        raise ValueError("text must not be empty")
    if square_size < 1:
        raise ValueError("square_size must be at least 1")

    n = len(text)
    cols = squares_per_row if squares_per_row > 0 else n
    rows = (n + cols - 1) // cols

    cell = square_size + padding
    width = cols * cell + padding
    height = rows * cell + padding

    img = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)

    for idx, char in enumerate(text):
        row, col = divmod(idx, cols)
        x = padding + col * cell
        y = padding + row * cell
        color = letter_to_color(char)
        draw.rectangle([x, y, x + square_size - 1, y + square_size - 1], fill=color)

    return img


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Translate text into coloured squares (Christian Faur style)."
    )
    parser.add_argument("text", nargs="?", help="Text to encode (or read from stdin).")
    parser.add_argument(
        "-o", "--output", default="output.png", help="Output image file (default: output.png)."
    )
    parser.add_argument(
        "-s", "--size", type=int, default=50, help="Square size in pixels (default: 50)."
    )
    parser.add_argument(
        "-p", "--padding", type=int, default=4, help="Padding between squares in pixels (default: 4)."
    )
    parser.add_argument(
        "-r", "--row", type=int, default=0,
        help="Number of squares per row (default: 0 = single row)."
    )
    args = parser.parse_args()

    text = args.text or sys.stdin.read().strip()
    if not text:
        parser.error("No text provided.")

    img = text_to_image(text, square_size=args.size, padding=args.padding, squares_per_row=args.row)
    img.save(args.output)
    print(f"Saved {len(text)}-character image to '{args.output}' ({img.width}×{img.height} px).")


if __name__ == "__main__":
    main()
