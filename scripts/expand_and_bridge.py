import re

# Read the validated grid
with open('make_map.py', 'r') as f:
    code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
grid_lines_str = m.group(1)
lines = [l.strip().strip('"').strip("'") for l in grid_lines_str.split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), max(len(row) for row in grid)

# 3x3 Expansion
new_H, new_W = H * 3, W * 3
new_grid = [['..'] * new_W for _ in range(new_H)]

for r in range(H):
    for c in range(len(grid[r])):
        val = grid[r][c]
        if val == '..': continue
        for dr in range(3):
            for dc in range(3):
                new_grid[3*r + dr][3*c + dc] = val

# Bridge diagonals
# If X is at (r,c) and (r+1, c+1) with diagonal connection
for r in range(H - 1):
    for c in range(W - 1):
        try:
            val1 = grid[r][c]
            val2 = grid[r+1][c+1]
            val_tr = grid[r][c+1]
            val_bl = grid[r+1][c]
        except IndexError:
            continue
            
        if val1 == val2 and val1 != '..':
            if val_tr != val1 and val_bl != val1:
                # Bridge X between top-left and bottom-right
                # Top-left block bottom-right corner is (3r+2, 3c+2)
                # Bottom-right block top-left corner is (3r+3, 3c+3)
                # Bridge fills (3r+2, 3c+3) and (3r+3, 3c+2)
                new_grid[3*r+2][3*c+3] = val1
                new_grid[3*r+3][3*c+2] = val1
                
        if val_tr == val_bl and val_tr != '..':
            if val1 != val_tr and val2 != val_tr:
                # Bridge Y between top-right and bottom-left
                # Top-right block bottom-left corner is (3r+2, 3c+3)
                # Bottom-left block top-right corner is (3r+3, 3c+2)
                # Bridge fills (3r+2, 3c+2) and (3r+3, 3c+3)
                new_grid[3*r+2][3*c+2] = val_tr
                new_grid[3*r+3][3*c+3] = val_tr

joined = ",\n    ".join('"' + " ".join(row) + '"' for row in new_grid)
new_code = code[:m.start(1)] + "\n    " + joined + "\n" + code[m.end(1):]

with open('make_map.py', 'w') as f:
    f.write(new_code)

print("Expanded grid to 3x3 and added bridges safely!")
