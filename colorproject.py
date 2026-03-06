from pathlib import Path
import random

# head : meta
# html : everything visible

text = input("Program is case-sensitive and treats accented letters (such as é, è, etc.) as different characters.\n"
            "Enter text to translate: ")

def clamp(value):
    return max(0, min(255, value))

def closest_ref_letter_and_dist(x: str, ref_map: dict[str, tuple[int,int,int]]) -> tuple[str, int]:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    if not x in alphabet:
        return None, None

    ix = alphabet.index(x)

    best_letter = None
    best_dist = 10**9 # maximum

    for rl in ref_map.keys(): # key -> letter in ref_map, associated with a tuple RGB
        d = abs(ix - alphabet.index(rl))
        if d < best_dist:
            best_dist = d
            best_letter = rl
            if d == 0:  # exact match (best match) => not need to continue
                break

    return best_letter, best_dist

def color_from_ref_distance(x: str, ref_map: dict[str, tuple[int,int,int]], style: str) -> str:
    rl, d = closest_ref_letter_and_dist(x, ref_map)

    # not a letter
    if rl is None:
        return f"rgb(0,0,0)"

    base = ref_map[rl]
    inv = (255 - ref_map[rl][0], 255 - ref_map[rl][1], 255 - ref_map[rl][2])
    t = d / 25  # between 0..1 -- d between 0 & 25 => 0..25 / 25 (25 = max distance between 2 letters)
    
    # linear interpolation (lerp)
    r = round(base[0] + (inv[0] - base[0]) * t)
    g = round(base[1] + (inv[1] - base[1]) * t)
    b = round(base[2] + (inv[2] - base[2]) * t)

    if style == "1":
        return f"rgb({r}, {g}, {b})"
    else:
        r2 = clamp(r + random.choice([-40, 40]))
        g2 = clamp(g + random.choice([-40, 40]))
        b2 = clamp(b + random.choice([-40, 40]))
        angle = random.randint(0, 360)

        return f"linear-gradient({angle}deg, rgb({r},{g},{b}), rgb({r2},{g2},{b2}))"


print("\nWhich translation method would you prefer?\n"
        "1: Colour dictionary (e.g. all ‘e’s will be green)\n"
        "2: Pure random (e.g. there will be green, red, etc. ‘e’s)\n"
        "3: Reference name (the closer a letter is to a letter in the reference name, the closer its colour will be to the colour associated with that name)")
while True:
    method = input("Your choice (1, 2, 3): ")
    if method in ("1", "2", "3"):
        letters_colors = {} # methods 1, 3
        if method == "3":
            # TODO : control des char
            ref_name = input("Enter the name: ")
            ref_map = {}
            # TODO : value between 0 et 255
            ref_color_r = int(input("Enter the red value of color (RGB) associated with the name: "))
            ref_color_g = int(input("Enter the green value: "))
            ref_color_b = int(input("Enter the blue value: "))

            for c in ref_name:
                ref_map[c] = ( clamp(ref_color_r + random.randint(-20, 20)), clamp(ref_color_g + random.randint(-20, 20)), clamp(ref_color_b + random.randint(-20, 20)) )
                letters_colors[c] = f"rgb({ref_map[c][0]}, {ref_map[c][1]}, {ref_map[c][2]})"

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

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgb({r},{g},{b})"

def random_gradient():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    r2 = clamp(r + random.choice([-70, 70]))
    g2 = clamp(g + random.choice([-70, 70]))
    b2 = clamp(b + random.choice([-70, 70]))

    angle = random.randint(0, 360)

    return f"linear-gradient({angle}deg, rgb({r},{g},{b}), rgb({r2},{g2},{b2}))"

# def normalize_letter(c: str) -> str:

for character in text:
    character = character.lower()
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
    
    elif method == "3":

        if character not in letters_colors:    
            letters_colors[character] = color_from_ref_distance(character, ref_map, style)

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
