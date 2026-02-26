import re
with open('make_map.py', 'r') as f: code = f.read()
grid_lines_str = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL).group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

for r in range(len(grid)):
    s = ""
    for c in range(len(grid[r])):
        s += f"{grid[r][c]:>3}"
    print(f"R{r:02d}: {s}")

