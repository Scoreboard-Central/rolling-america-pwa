import re

with open("src/app/app.component.html", "r") as f:
    html = f.read()

with open("generated_map.html", "r") as f:
    new_svg = f.read().strip()
    # fix quotes right away
    new_svg = new_svg.replace("\\'", "'")

pattern = re.compile(r'<svg.*?</svg>', re.DOTALL)
if pattern.search(html):
    html = pattern.sub(new_svg, html)
    with open("src/app/app.component.html", "w") as f:
        f.write(html)
    print("SVG replaced.")
else:
    print("SVG tag not found in HTML.")
