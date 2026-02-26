import json

grid_str = """
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. VT VT VT NH NH NH ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. VT VT VT NH NH NH ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. VT VT VT NH NH NH ME ME ME ME ME ME .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. WA WA WA WA WA WA WA WA ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. NY NY NY NY VT VT VT NH NH NH .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. WA WA WA WA WA WA WA WA ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. NY NY NY NY VT VT VT NH NH NH .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. WA WA WA WA WA WA WA WA ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN WI WI WI WI WI MI MI MI MI MI MI .. .. .. .. .. .. .. .. NY NY NY NY VT VT VT NH NH NH .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. WA WA WA WA WA WA WA WA ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN WI WI WI WI WI MI MI MI MI MI MI .. .. .. .. .. .. .. .. NY NY NY NY MA MA MA MA MA MA MA MA MA .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. WA WA WA WA WA WA WA WA ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN WI WI WI WI WI MI MI MI MI MI MI .. .. .. .. .. .. .. .. NY NY NY NY MA MA MA MA MA MA MA MA MA .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AK AK AK AK AK AK .. .. .. OR OR OR OR OR OR OR OR ID ID ID MT MT MT MT MT MT MT MT MT MT MT ND ND ND ND ND ND ND ND ND MN MN MN MN MN WI WI WI WI WI .. .. MI MI MI MI .. .. .. .. NY NY NY NY NY NY NY NY MA MA MA MA MA MA MA MA MA .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. OR OR OR OR OR OR OR OR ID ID ID MT MT MT MT MT MT MT MT MT MT MT SD SD SD SD SD SD SD SD SD MN MN MN MN MN WI WI WI WI WI .. .. MI MI MI MI .. .. .. .. NY NY NY NY NY NY NY NY CT CT CT CT CT CT RI RI RI .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. OR OR OR OR OR OR OR OR ID ID ID MT MT MT MT MT MT MT MT MT MT MT SD SD SD SD SD SD SD SD SD MN MN MN MN MN WI WI WI WI WI .. .. MI MI MI MI .. .. .. .. NY NY NY NY NY NY NY NY CT CT CT CT CT CT RI RI RI .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. OR OR OR OR OR OR OR OR ID ID ID ID ID ID WY WY WY WY WY WY WY WY SD SD SD SD SD SD SD SD SD IA IA IA IA IA WI WI WI WI WI .. .. MI MI MI MI .. .. .. .. NY NY NY NY NY NY NY NY CT CT CT CT CT CT RI RI RI .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. OR OR OR OR OR OR OR OR ID ID ID ID ID ID WY WY WY WY WY WY WY WY SD SD SD SD SD SD SD SD SD IA IA IA IA IA IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA NJ NJ NJ NJ NJ NJ .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. OR OR OR OR OR OR OR OR ID ID ID ID ID ID WY WY WY WY WY WY WY WY SD SD SD SD SD SD SD SD SD IA IA IA IA IA IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA NJ NJ NJ NJ NJ NJ .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT WY WY WY WY WY WY WY WY NE NE NE NE NE NE NE NE NE IA IA IA IA IA IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA NJ NJ NJ NJ NJ NJ .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT WY WY WY WY WY WY WY WY NE NE NE NE NE NE NE NE NE IA IA IA IA IA IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA DE DE DE DE DE DE .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT WY WY WY WY WY WY WY WY NE NE NE NE NE NE NE NE NE IA IA IA IA IA IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA DE DE DE DE DE DE .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO NE NE NE NE NE NE NE MO MO MO MO MO IL IL IL IL IL IN IN IN IN OH OH OH OH PA PA PA PA PA PA PA PA DE DE DE DE DE DE .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO NE NE NE NE NE NE NE MO MO MO MO MO IL IL IL IL IL KY KY KY KY KY WV WV WV WV WV WV VA VA VA MD MD MD MD MD MD .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO KS KS KS KS KS KS KS MO MO MO MO MO IL IL IL IL IL KY KY KY KY KY WV WV WV WV WV WV VA VA VA MD MD MD MD MD MD .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO KS KS KS KS KS KS KS MO MO MO MO MO IL IL IL IL IL KY KY KY KY KY WV WV WV WV WV WV VA VA VA MD MD MD MD MD MD .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO KS KS KS KS KS KS KS MO MO MO MO MO KY KY KY KY KY KY KY KY KY KY VA VA VA VA VA VA VA VA VA VA VA VA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. HI HI HI HI HI HI .. .. .. CA CA CA CA NV NV NV NV NV NV UT UT UT UT UT UT CO CO CO CO CO CO CO CO KS KS KS KS KS KS KS MO MO MO MO MO KY KY KY KY KY KY KY KY KY KY VA VA VA VA VA VA VA VA VA VA VA VA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. HI HI HI HI HI HI .. .. .. CA CA CA CA CA CA CA CA AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM OK OK OK OK OK OK OK OK OK MO MO MO MO MO KY KY KY KY KY KY KY KY KY KY VA VA VA VA VA VA VA VA VA VA VA VA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. HI HI HI HI HI HI .. .. .. .. CA CA CA CA CA CA CA AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM OK OK OK OK OK OK OK OK OK MO MO MO MO MO TN TN TN TN TN TN TN TN TN TN TN TN NC NC NC NC NC NC NC NC NC NC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM OK OK OK OK OK OK OK OK OK AR AR AR AR AR TN TN TN TN TN TN TN TN TN TN TN TN NC NC NC NC NC NC NC NC NC NC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. CA CA CA CA CA AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX OK OK OK OK OK AR AR AR AR AR TN TN TN TN TN TN TN TN TN TN TN TN NC NC NC NC NC NC NC NC NC NC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX OK OK OK OK OK AR AR AR AR AR MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX OK OK OK OK OK AR AR AR AR AR MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX OK OK OK OK OK AR AR AR AR AR MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX TX TX TX TX TX TX TX AR AR AR MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ AZ AZ AZ AZ AZ AZ NM NM NM NM NM NM TX TX TX TX TX TX TX TX TX TX TX LA LA LA MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX TX TX TX TX TX LA LA LA MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX TX TX TX TX TX LA LA LA MS MS MS MS MS AL AL AL AL GA GA GA GA GA GA .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX TX TX TX TX TX LA LA LA MS MS MS MS MS AL AL FL FL FL FL FL FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX TX TX TX TX TX LA LA LA LA LA LA MS MS AL AL FL FL FL FL FL FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX LA LA LA LA LA LA MS MS AL AL FL FL FL FL FL FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX LA LA LA LA LA LA .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX TX TX TX TX LA LA LA LA LA LA .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX TX .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
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

SIZE = 12 # pixels per cell
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*SIZE}" height="{H*SIZE}" viewBox="0 0 {W*SIZE} {H*SIZE}">')

# Find all states
states = set(c for r in grid for c in r if c != '..')
for state in states:
    cells = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == state]
    
    fill_color = hex_colors[colors[state]]
    tag = f"""  <g class="state-{state} cursor-pointer hover:opacity-80 transition-opacity" (click)="openModal('state', '{state}')">"""
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
    custom_centers = {
        'ID': (35.5, 15),
        'FL': (71.5, 38),
        'VA': (76.5, 25),
        'CA': (26.5, 21)
    }
    
    if state in custom_centers:
        cx_grid, cy_grid = custom_centers[state]
    else:
        cx_grid = sum(x for x, y in cells) / len(cells)
        cy_grid = sum(y for x, y in cells) / len(cells)
        
    cx = cx_grid * SIZE + SIZE/2
    cy = cy_grid * SIZE + SIZE/2
    
    tag2 = f"""    <text x="{cx}" y="{cy+2}" text-anchor="middle" dominant-baseline="central" font-size="20" font-weight="900" fill="#1e293b">{{{{ stateData['{state}'] }}}}</text>"""
    circle_tag = f"""    @if (guardedStates['{state}']) {{\n      <circle cx="{cx}" cy="{cy+2}" r="15" fill="none" stroke="#1e293b" stroke-width="2.5" />\n    }}"""
    svg.append(circle_tag)
    svg.append(tag2)
    
    svg.append('  </g>')

svg.append('</svg>')

with open('generated_map.html', 'w') as f:
    f.write("\n".join(svg))

print(f"Generated map with {len(states)} states.")
