# colorproject

Translates a text string into a sequence of coloured squares, strongly inspired by the work of [Christian Faur](https://www.christianfaur.com/).

Each letter of the alphabet is assigned a unique colour distributed evenly across the visible spectrum (violet → red).  Non-alphabetic characters (spaces, punctuation, digits …) are rendered as white squares.

![alphabet](https://github.com/user-attachments/assets/b9dd8a74-6064-4441-ab95-30dd5c8bfb87)
*A → Z encoded as coloured squares*

---

## Requirements

```
pip install -r requirements.txt
```

## Usage

### Command line

```bash
# Encode a string (output saved to output.png by default)
python colorproject.py "Hello World"

# Custom output file, square size and padding
python colorproject.py "Bonjour" -o bonjour.png -s 60 -p 6

# Wrap into multiple rows (e.g. 10 squares per row)
python colorproject.py "The quick brown fox" -r 10 -o fox.png

# Read text from stdin
echo "colorproject" | python colorproject.py -o stdin.png
```

| Option | Default | Description |
|--------|---------|-------------|
| `-o` / `--output` | `output.png` | Output image file |
| `-s` / `--size` | `50` | Square side length in pixels |
| `-p` / `--padding` | `4` | Gap between squares in pixels |
| `-r` / `--row` | `0` | Squares per row (0 = single row) |

### Python API

```python
from colorproject import letter_to_color, text_to_image

# Get the RGB colour for a single letter
print(letter_to_color("A"))   # (127, 0, 255)  — violet
print(letter_to_color("Z"))   # (255, 0, 0)    — red

# Generate and save an image
img = text_to_image("Hello", square_size=50, padding=4)
img.save("hello.png")
```

## Running the tests

```bash
pip install pytest
pytest test_colorproject.py -v
```

## Colour mapping

The 26 letters are spread evenly over the HSV hue wheel, starting at violet (hue 0.75) for **A** and ending at red (hue 0.0) for **Z**:

```
A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
violet → blue → cyan → green → yellow → orange → red
```
