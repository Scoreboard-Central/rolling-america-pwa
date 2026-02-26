import re

with open('generated_map.html', 'r') as f:
    new_svg = f.read()

with open('../src/app/app.component.html', 'r') as f:
    html = f.read()

# Replace the <svg> block
html = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg".*?</svg>', new_svg, html, flags=re.DOTALL)

with open('../src/app/app.component.html', 'w') as f:
    f.write(html)
print("Replaced SVG!")
