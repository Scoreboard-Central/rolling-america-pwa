import sys

W, H = 50, 28
grid = [['..' for _ in range(W)] for _ in range(H)]

def draw_rect(state, x, y, w, h):
    for i in range(h):
        for j in range(w):
            if 0 <= y+i < H and 0 <= x+j < W:
                grid[y+i][x+j] = state

# Define states by x, y, width, height roughly. We can adjust overlapping ones via draw order.
# Orange
# AK is floating
draw_rect('AK', 2, 2, 4, 4)
draw_rect('HI', 2, 14, 4, 2)
draw_rect('WA', 8, 4, 6, 4)
draw_rect('OR', 8, 8, 6, 4)
draw_rect('CA', 8, 12, 4, 10)
draw_rect('NV', 12, 12, 4, 6)
draw_rect('ID', 14, 4, 4, 8)
draw_rect('UT', 16, 12, 4, 6)
draw_rect('AZ', 14, 18, 6, 6)

# Blue
draw_rect('MT', 18, 4, 6, 4)
draw_rect('ND', 24, 4, 4, 4)
draw_rect('SD', 24, 8, 6, 4)
draw_rect('MN', 28, 4, 4, 6)
draw_rect('IA', 28, 10, 4, 4)
draw_rect('WI', 32, 4, 4, 6)
draw_rect('IL', 32, 10, 4, 6)
draw_rect('MI', 36, 4, 4, 6) # MI is split? let's just make it block
draw_rect('IN', 36, 10, 2, 6)

# Green
draw_rect('WY', 18, 8, 6, 4)
draw_rect('CO', 20, 12, 6, 4)
draw_rect('NM', 20, 16, 6, 6)
draw_rect('NE', 24, 12, 6, 4)
draw_rect('KS', 26, 16, 6, 4)
draw_rect('OK', 24, 20, 8, 4)
draw_rect('TX', 22, 24, 10, 4) 

# Yellow
draw_rect('MO', 32, 16, 4, 4)
draw_rect('AR', 30, 20, 4, 4)
draw_rect('LA', 30, 24, 4, 4)
draw_rect('KY', 36, 16, 4, 4)
draw_rect('TN', 34, 20, 8, 2)
draw_rect('MS', 34, 22, 4, 4)
draw_rect('AL', 38, 22, 4, 4)
draw_rect('FL', 42, 26, 6, 2) 

# Red
draw_rect('OH', 38, 12, 4, 4)
draw_rect('WV', 40, 16, 4, 2)
draw_rect('VA', 42, 18, 4, 4)
draw_rect('PA', 42, 12, 4, 4)
draw_rect('MD', 44, 16, 4, 2)
draw_rect('DE', 46, 14, 2, 2)
draw_rect('NC', 44, 22, 4, 2)
draw_rect('SC', 44, 24, 4, 2)
draw_rect('GA', 42, 22, 2, 6) # GA intersects with others, will refine later

# Purple
draw_rect('NY', 40, 6, 4, 6)
draw_rect('NJ', 44, 12, 2, 2)
draw_rect('VT', 44, 6, 2, 2)
draw_rect('NH', 46, 6, 2, 2)
draw_rect('ME', 46, 2, 4, 4)
draw_rect('MA', 44, 8, 6, 2)
draw_rect('CT', 44, 10, 4, 2)
draw_rect('RI', 48, 10, 2, 2)

import os
with open('generated_grid.txt', 'w') as f:
    for row in grid:
        f.write(" ".join(row) + "\n")

import test_map_rules
test_map_rules.grid_str = "\n".join(" ".join(row) for row in grid)
test_map_rules.colors = test_map_rules.colors # Keep colors
test_map_rules.W = W
test_map_rules.H = H
lines = [l.strip().split() for l in test_map_rules.grid_str.strip().split('\n') if l.strip()]
test_map_rules.grid = []
for row in lines:
    test_map_rules.grid.append(row + ['..'] * (W - len(row)))
# re-init neighbors
test_map_rules.neighbors = {}
test_map_rules.states = set(c for r in test_map_rules.grid for c in r if c != '..')
for s in test_map_rules.states:
    test_map_rules.neighbors[s] = set()

for y in range(H):
    for x in range(W):
        c = test_map_rules.grid[y][x]
        if c == '..': continue
        
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < H and 0 <= nx < W:
                nc = test_map_rules.grid[ny][nx]
                if nc != '..' and nc != c:
                    test_map_rules.neighbors[c].add(nc)
                    
test_map_rules.check()

