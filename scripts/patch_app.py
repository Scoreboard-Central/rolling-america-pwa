import re

with open('generated_map.html', 'r') as f:
    new_svg = f.read()

with open('../src/app/app.component.html', 'r') as f:
    app_html = f.read()

# Replace the <svg ... </svg> inside the <div class="relative w-full aspect-[20/14]">
if '<svg viewBox=' in app_html:
    app_html = re.sub(r'<svg viewBox=.*?</svg>', new_svg, app_html, flags=re.DOTALL)
else:
    print("Could not find <svg viewBox=...")
    
with open('../src/app/app.component.html', 'w') as f:
    f.write(app_html)
print("Updated app.component.html")
