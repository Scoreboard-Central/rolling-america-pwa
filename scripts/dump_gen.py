import re
with open('generate_map.py', 'r') as f:
    code = f.read()
grid_str = re.search(r'grid_str = """(.*?)"""', code, flags=re.DOTALL).group(1).strip()
lines = [l.strip().split() for l in grid_str.split('\n')]
W = max(len(l) for l in lines)
grid = [r + ['..'] * (W - len(r)) for r in lines]

print("      " + "".join(f"{i % 10}" for i in range(W)))
for i, r in enumerate(grid):
    print(f"R{i:02d}: " + "".join(c[0] if c!='..' else '.' for c in r))

print("\nMO cells:", [(i, c) for i, r in enumerate(grid) for c, val in enumerate(r) if val == 'MO'])
print("NY cells:", [(i, c) for i, r in enumerate(grid) for c, val in enumerate(r) if val == 'NY'])
print("MA cells:", [(i, c) for i, r in enumerate(grid) for c, val in enumerate(r) if val == 'MA'])
