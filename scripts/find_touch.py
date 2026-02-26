import sys
import re

with open('make_map.py', 'r') as f: code = f.read()
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), max(len(r) for r in grid)
for i in range(H): grid[i].extend(['..']*(W-len(grid[i])))

def t(s1, s2):
    for y in range(H):
        for x in range(W):
            if grid[y][x] == s1:
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] == s2:
                        print(f"{s1} at {y},{x} touches {s2} at {ny},{nx}")

t("NY", "DE")
t("CT", "DE")
t("NJ", "CT")
