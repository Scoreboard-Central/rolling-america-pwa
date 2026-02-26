import re

with open('generated_map.html', 'r') as f:
    html = f.read()

# Find all groups
groups = re.findall(r'<g.*?(?=<g|</svg)', html, flags=re.DOTALL)

state_coords = {}
max_x, max_y = 0, 0

for g in groups:
    # Find state name
    m_state = re.search(r"stateData\['(.*?)'\]", g)
    if not m_state:
        # fallback to click openModal
        m_state = re.search(r"openModal\('state',\s*'(.*?)'\)", g)
    if not m_state: continue
    state = m_state.group(1)
    
    # Find all rects
    rects = re.findall(r'<rect x="(\d+)" y="(\d+)"', g)
    for rx, ry in rects:
        x, y = int(rx)//34, int(ry)//34
        if y not in state_coords: state_coords[y] = {}
        state_coords[y][x] = state
        max_x = max(max_x, x)
        max_y = max(max_y, y)

grid = []
for y in range(max_y + 1):
    row = []
    for x in range(max_x + 1):
        row.append(state_coords.get(y, {}).get(x, '..'))
    grid.append(row)

# Now apply expansions or manual fixes directly
# Let's just write this to test_grid.txt to verify its integrity
joined = ",\n    ".join('"' + " ".join(row) + '"' for row in grid)

with open('make_map.py', 'r') as f: code = f.read()
new_code = re.sub(r'grid_lines = \[(.*?)\]', f'grid_lines = [\n    {joined}\n]', code, flags=re.DOTALL)
with open('make_map.py', 'w') as f: f.write(new_code)
print("Extracted grid and saved to make_map.py!")
