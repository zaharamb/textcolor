from pathlib import Path
import random

# head : meta
# html : everything visible

text = input("Enter text to translate: ")

print("\nWhich translation method would you prefer?\n"
        "1: Colour dictionary (e.g. all ‘e’s will be green)\n"
        "2: Pure random (e.g. there will be green, red, etc. ‘e’s)")
while True:
    method = input("Your choice (1 or 2): ")
    if method in ("1", "2"):
        break
print(f"You selected method {method}.")

print("\nWhich style would you prefer?\n"
        "1: Plain\n"
        "2: Linear gradient")
while True:
    style = input("Your choice (1 or 2): ")
    if style in ("1", "2"):
        break
print(f"You selected style {style}.\n")

squares_html = ""

# for method 1 only "color dictionary"
letters_colors = {}

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgb({r},{g},{b})"

def clamp(value):
    return max(0, min(255, value))

def random_gradient():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    r2 = clamp(r + random.choice([-70, 70]))
    g2 = clamp(g + random.choice([-70, 70]))
    b2 = clamp(b + random.choice([-70, 70]))

    angle = random.randint(0, 360)

    return f"linear-gradient({angle}deg, rgb({r},{g},{b}), rgb({r2},{g2},{b2}))"

for character in text:
    if character == " ":
        squares_html += '<div class="square" style="background:rgb(254,254,254)"></div>'
    elif method == "1":
        # If the letter doesn't have a color yet
        # (best to do it that way rather than having 26 lines, one for each 26 letters)
        if character not in letters_colors:
            if style == "1":
                letters_colors[character] = random_color()
            else:
                letters_colors[character] = random_gradient()

        squares_html += f'<div class="square" style="background:{letters_colors[character]}"></div>'

    elif method == "2":
        if style == "1":
            squares_html += f'<div class="square" style="background:{random_color()};"></div>'
        else:
            squares_html += f'<div class="square" style="background:{random_gradient()};"></div>'


html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>colorproject</title>

  <style>
    .square {{
    width: 20px;
    height: 20px;
    flex: 0 0 20px; /* flex-grow, flex-shrink, flex-basis: base must be 20px */
    display: block;
    /* background-image:linear-gradient(135deg, red, blue); */
    }}

    .container {{
    display: flex; /* Not relevant to put it in the .square class: because we want to assign the layout of the squares between them, not the squares themselves */
    flex-wrap: wrap; /* allow line breaks */
    row-gap: 3px;
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
