with open('generated_map.html', 'r') as f:
    svg_content = f.read()

with open('src/app/app.component.html', 'r') as f:
    html_content = f.read()

start_tag = '<svg xmlns="http://www.w3.org/2000/svg"'
start_idx = html_content.find(start_tag)
if start_idx == -1:
    print("Error: Could not find start tag!")
    exit(1)

end_tag = '</svg>'
end_idx = html_content.find(end_tag, start_idx) + len(end_tag)

svg_content = svg_content.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" class="w-full h-full max-h-full"')

new_html = html_content[:start_idx] + svg_content.strip() + html_content[end_idx:]

with open('src/app/app.component.html', 'w') as f:
    f.write(new_html)
print("Injected successfully!")
