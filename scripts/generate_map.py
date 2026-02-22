import json

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..
.. AK AK .. WA ID ID MT ND MN MN WI NY VT VT NH ME ME ..
.. AK AK .. OR ID UT SD SD SD IA WI NY VT VT NH NH .. ..
.. .. .. .. OR NV UT WY NE NE IL WI NY MA MA MA MA .. ..
.. .. .. .. CA NV AZ WY NE NE IN MI NY CT CT CT RI .. ..
.. HI HI .. CA CA AZ CO CO KS IN MI NJ CT OH PA DE .. ..
.. .. .. .. CA CA AZ NM OK KS LA TN MS KY WV PA MD .. ..
.. .. .. .. CA CA AZ TX OK AR MO TN AL AL VA VA NC .. ..
.. .. .. .. .. .. .. TX TX AR AR AR AL AL SC SC GA GA ..
.. .. .. .. .. .. .. TX TX AR AR AR .. .. .. GA GA .. ..
.. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
"""

colors = {
    'AK': 'ra-orange', 'HI': 'ra-orange', 'WA': 'ra-orange', 'OR': 'ra-orange', 'ID': 'ra-orange', 'UT': 'ra-orange', 'AZ': 'ra-orange', 'NV': 'ra-orange', 'CA': 'ra-orange',
    'MT': 'ra-blue', 'ND': 'ra-blue', 'SD': 'ra-blue', 'MN': 'ra-blue', 'IA': 'ra-blue', 'WI': 'ra-blue', 'IL': 'ra-blue', 'IN': 'ra-blue', 'MI': 'ra-blue',
    'WY': 'ra-green', 'NE': 'ra-green', 'KS': 'ra-green', 'CO': 'ra-green', 'NM': 'ra-green', 'OK': 'ra-green', 'TX': 'ra-green',
    'MO': 'ra-yellow', 'AR': 'ra-yellow', 'LA': 'ra-yellow', 'AL': 'ra-yellow', 'TN': 'ra-yellow', 'MS': 'ra-yellow', 'FL': 'ra-yellow', 'KY': 'ra-yellow',
    'DE': 'ra-red', 'MD': 'ra-red', 'PA': 'ra-red', 'OH': 'ra-red', 'WV': 'ra-red', 'VA': 'ra-red', 'NC': 'ra-red', 'SC': 'ra-red', 'GA': 'ra-red',
    'ME': 'ra-purple', 'NH': 'ra-purple', 'VT': 'ra-purple', 'NY': 'ra-purple', 'MA': 'ra-purple', 'RI': 'ra-purple', 'CT': 'ra-purple', 'NJ': 'ra-purple',
}

hex_colors = {
    'ra-orange': '#F4B384', 'ra-blue': '#85BBEA', 'ra-green': '#9ACC99',
    'ra-yellow': '#F4D075', 'ra-red': '#F29C9C', 'ra-purple': '#A4A6D5'
}

lines = [l.strip().split() for l in grid_str.strip().split('\n')]
H = len(lines)
W = max(len(row) for row in lines)

# ensure uniform grid
grid = []
for row in lines:
    grid.append(row + ['..'] * (W - len(row)))

SIZE = 34 # pixels per cell
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*SIZE}" height="{H*SIZE}" viewBox="0 0 {W*SIZE} {H*SIZE}">')

# Find all states
states = set(c for r in grid for c in r if c != '..')
for state in states:
    cells = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == state]
    
    fill_color = hex_colors[colors[state]]
    
    tag = f"""  <g class="cursor-pointer hover:opacity-80 transition-opacity" (click)="openModal('state', '{state}')">"""
    svg.append(tag)
    
    # Draw Fill Rectangles
    for (x, y) in cells:
        svg.append(f'    <rect x="{x*SIZE}" y="{y*SIZE}" width="{SIZE}" height="{SIZE}" fill="{fill_color}" />')
        
    # Draw Outer Borders
    for (x, y) in cells:
        px, py = x*SIZE, y*SIZE
        # Top
        if y == 0 or grid[y-1][x] != state:
            svg.append(f'    <line x1="{px}" y1="{py}" x2="{px+SIZE}" y2="{py}" stroke="#334155" stroke-width="2" />')
        # Bottom
        if y == H-1 or grid[y+1][x] != state:
            svg.append(f'    <line x1="{px}" y1="{py+SIZE}" x2="{px+SIZE}" y2="{py+SIZE}" stroke="#334155" stroke-width="2" />')
        # Left
        if x == 0 or grid[y][x-1] != state:
            svg.append(f'    <line x1="{px}" y1="{py}" x2="{px}" y2="{py+SIZE}" stroke="#334155" stroke-width="2" />')
        # Right
        if x == W-1 or grid[y][x+1] != state:
            svg.append(f'    <line x1="{px+SIZE}" y1="{py}" x2="{px+SIZE}" y2="{py+SIZE}" stroke="#334155" stroke-width="2" />')
            
    # Draw Text
    avg_x = sum(x for x, y in cells) / len(cells)
    avg_y = sum(y for x, y in cells) / len(cells)
    cx = avg_x * SIZE + SIZE/2
    cy = avg_y * SIZE + SIZE/2
    
    tag2 = f"""    <text x="{cx}" y="{cy+2}" text-anchor="middle" dominant-baseline="central" font-size="20" font-weight="900" fill="#1e293b">{{{{ stateData['{state}'] }}}}</text>"""
    circle_tag = f"""    @if (guardedStates['{state}']) {{\n      <circle cx="{cx}" cy="{cy+2}" r="15" fill="none" stroke="#1e293b" stroke-width="2.5" />\n    }}"""
    svg.append(circle_tag)
    svg.append(tag2)
    
    svg.append('  </g>')

svg.append('</svg>')

with open('generated_map.html', 'w') as f:
    f.write("\n".join(svg))

print(f"Generated map with {len(states)} states.")
