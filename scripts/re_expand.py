import re
import heapq

with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), max(len(r) for r in grid)
for i in range(H):
    grid[i].extend(['..'] * (W - len(grid[i])))

new_H, new_W = H * 3, W * 3
new_grid = [['..'] * new_W for _ in range(new_H)]

for r in range(H):
    for c in range(W):
        val = grid[r][c]
        if val == '..': continue
        for dr in range(3):
            for dc in range(3):
                new_grid[3*r + dr][3*c + dc] = val

# Safe Bridge logic for direct adjacent diagonals
for r in range(H - 1):
    for c in range(W - 1):
        val1 = grid[r][c]
        val2 = grid[r+1][c+1]
        val_tr = grid[r][c+1]
        val_bl = grid[r+1][c]
            
        if val1 == val2 and val1 != '..':
            if val_tr != val1 and val_bl != val1:
                new_grid[3*r+2][3*c+3] = val1
                new_grid[3*r+3][3*c+2] = val1
                
        if val_tr == val_bl and val_tr != '..':
            if val1 != val_tr and val2 != val_tr:
                new_grid[3*r+2][3*c+2] = val_tr
                new_grid[3*r+3][3*c+3] = val_tr

grid_str = "\n".join(" ".join(row) for row in new_grid)

# Inject to generate_map.py
with open('generate_map.py', 'r') as f:
    gen_code = f.read()

new_gen_code = re.sub(r'grid_str = """[\s\S]*?"""', f'grid_str = """\n{grid_str}\n"""', gen_code)
new_gen_code = new_gen_code.replace("SIZE = 34", "SIZE = 12")
with open('generate_map.py', 'w') as f:
    f.write(new_gen_code)

print("Expansion complete! Ready to generate.")
