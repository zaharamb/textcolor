"""
Tests for colorproject.py
"""

import pytest
from PIL import Image
from colorproject import (
    COLOR_MAP,
    DEFAULT_COLOR,
    letter_to_color,
    text_to_image,
)


# ---------------------------------------------------------------------------
# letter_to_color
# ---------------------------------------------------------------------------

class TestLetterToColor:
    def test_uppercase_letter_returns_rgb_tuple(self):
        color = letter_to_color("A")
        assert isinstance(color, tuple)
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)

    def test_lowercase_maps_same_as_uppercase(self):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            assert letter_to_color(ch) == letter_to_color(ch.upper())

    def test_all_26_letters_have_distinct_colors(self):
        colors = [letter_to_color(ch) for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        assert len(set(colors)) == 26, "Each letter should have a unique colour"

    def test_non_alpha_returns_default_color(self):
        for ch in " !0?-\n":
            assert letter_to_color(ch) == DEFAULT_COLOR

    def test_color_map_contains_all_letters(self):
        for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            assert ch in COLOR_MAP


# ---------------------------------------------------------------------------
# text_to_image
# ---------------------------------------------------------------------------

class TestTextToImage:
    def test_returns_pil_image(self):
        img = text_to_image("ABC")
        assert isinstance(img, Image.Image)

    def test_image_is_rgb(self):
        img = text_to_image("Hello")
        assert img.mode == "RGB"

    def test_single_row_width(self):
        square_size = 50
        padding = 4
        text = "ABC"
        img = text_to_image(text, square_size=square_size, padding=padding)
        expected_width = len(text) * (square_size + padding) + padding
        assert img.width == expected_width

    def test_single_row_height(self):
        square_size = 50
        padding = 4
        img = text_to_image("XY", square_size=square_size, padding=padding)
        expected_height = 1 * (square_size + padding) + padding
        assert img.height == expected_height

    def test_multirow_layout(self):
        square_size = 20
        padding = 2
        text = "ABCDEF"
        cols = 3
        img = text_to_image(text, square_size=square_size, padding=padding, squares_per_row=cols)
        cell = square_size + padding
        assert img.width == cols * cell + padding
        assert img.height == 2 * cell + padding  # 6 letters / 3 cols = 2 rows

    def test_pixel_color_matches_letter(self):
        square_size = 10
        padding = 0
        img = text_to_image("A", square_size=square_size, padding=padding)
        # The centre pixel of the first square should match letter_to_color("A")
        px = img.getpixel((square_size // 2, square_size // 2))
        assert px == letter_to_color("A")

    def test_empty_text_raises(self):
        with pytest.raises(ValueError, match="empty"):
            text_to_image("")

    def test_invalid_square_size_raises(self):
        with pytest.raises(ValueError, match="square_size"):
            text_to_image("A", square_size=0)

    def test_space_character_uses_default_color(self):
        square_size = 10
        padding = 0
        img = text_to_image(" ", square_size=square_size, padding=padding)
        px = img.getpixel((square_size // 2, square_size // 2))
        assert px == DEFAULT_COLOR

    def test_custom_square_size(self):
        size = 30
        img = text_to_image("Z", square_size=size, padding=2)
        assert img.width == size + 2 * 2
