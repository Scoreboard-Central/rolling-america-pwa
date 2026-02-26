import sys

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

lines = [l.strip().split() for l in grid_str.strip().split('\n') if l.strip()]
W = max(len(row) for row in lines)
for row in lines:
    row.extend(['..'] * (W - len(row)))

new_lines = []
for row in lines:
    new_row = []
    for cell in row:
        new_row.extend([cell, cell])
    new_lines.append(" ".join(new_row))
    new_lines.append(" ".join(new_row))

with open('doubled_grid.txt', 'w') as f:
    f.write("\n".join(new_lines))
