from pathlib import Path
import random

# head : meta
# html : everything visible

text = input("Enter text to translate:")
squares_html = ""
letters_colors = {}

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgb({r},{g},{b})"

for character in text:
    if character == " ":
        squares_html += '<div class="space"></div>'
    else:
        # If the letter doesn't have a color yet
        # (best to do it that way rather than having 26 lines, one for each 26 letters)
        if character not in letters_colors:
            letters_colors[character] = random_color()

        squares_html += f'<div class="square" style="background:{letters_colors[character]}"></div>'


html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Ma page</title>

  <style>
    .square {{
    width: 20px;
    height: 20px;
    /* background: black; */
    margin-right: 0px;
    }}

    .space {{
    width: 20px; /* same size as .square */
    height: 20px;
    }}

    .container {{
    display: flex; /* Not relevant to put it in the .square class: because we want to assign the layout of the squares between them, not the squares themselves */
    }}
  </style>

</head>
<body>
  <div class="container">
    {squares_html}
  </div>


</body>
</html>
"""

p = Path("colorproject.html")
p.write_text(html, encoding="utf-8")
if p.exists():
    print("OK: colorproject.html created")
else:
    print("Error")
