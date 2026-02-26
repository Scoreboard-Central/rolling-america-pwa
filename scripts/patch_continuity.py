import re

with open('make_map.py', 'r') as f:
    code = f.read()

m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]

H = len(grid)
W = max(len(row) for row in grid)
for r in range(H):
    grid[r].extend(['..'] * (W - len(grid[r])))

grid[4][27] = 'MA'
grid[5][25] = 'NJ'
grid[5][26] = 'NY'
grid[6][22] = 'OH'
grid[7][17] = 'MO'
grid[8][18] = 'MO'
grid[8][20] = 'KY'
grid[8][23] = 'WV'
grid[10][21] = 'TN'
grid[10][25] = 'VA'

joined = ",\n    ".join('"' + " ".join(r) + '"' for r in grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]

with open('make_map.py', 'w') as f:
    f.write(new_code)
print("Patched make_map.py!")
