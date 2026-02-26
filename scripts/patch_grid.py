import sys

with open('make_map.py', 'r') as f: code = f.read()
import re
m = re.search(r'grid_lines = \[(.*?)\]', code, flags=re.DOTALL)
lines = [l.strip().strip('"').strip("'") for l in m.group(1).split(',\n')]
grid = [l.split() for l in lines]
H, W = len(grid), max(len(r) for r in grid)
for i in range(H): grid[i].extend(['..']*(W-len(grid[i])))

def break_link(s1, s2):
    # Find all orthogonal touches between s1 and s2
    touches = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == s1:
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < H and 0 <= nx < W and grid[ny][nx] == s2:
                        touches.append((y, x, ny, nx)) # from s1 to s2
    
    return touches

print("Touches IL-MI:", break_link("IL", "MI"))
print("Touches MD-WV:", break_link("MD", "WV"))
print("Touches MT-WA:", break_link("MT", "WA"))
print("Touches UT-NM:", break_link("UT", "NM"))

