import re

with open('../src/app/app.component.html', 'r') as f:
    content = f.read()

with open('generated_map.html', 'r') as f:
    new_svg = f.read()

# Replace the <svg> block
pattern = r'<svg xmlns="http://www.w3.org/2000/svg" class="w-full h-full max-h-full"[^>]*>.*?</svg>'
# The SVG in the file has class="w-full h-full max-h-full" which my generated SVG might not have...
# Let's adjust new_svg to have the same class
new_svg = new_svg.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" class="w-full h-full max-h-full"')

out = re.sub(pattern, new_svg, content, flags=re.DOTALL)

with open('../src/app/app.component.html', 'w') as f:
    f.write(out)

print("SVG replaced successfully.")
