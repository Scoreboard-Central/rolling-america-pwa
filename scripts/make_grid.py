import sys

# Max width is 46 cells. Height is 28.
new_rows = [
    # 00:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME .. .. .. .. .. .. .. ..",
    # 01:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ME ME .. .. .. .. .. .. .. ..",
    # 02: AK floating, top states
    ".. .. AK AK AK AK .. .. WA WA WA WA ID ID ID ID MT MT MT MT ND ND ND ND MN MN MN MN WI WI WI WI NY NY VT VT NH NH ME ME .. .. .. .. .. ..",
    # 03:
    ".. .. AK AK AK AK .. .. WA WA WA WA ID ID ID ID MT MT MT MT ND ND ND ND MN MN MN MN WI WI WI WI NY NY VT VT NH NH ME ME .. .. .. .. .. ..",
    # 04:
    ".. .. AK AK AK AK .. .. OR OR OR OR ID ID ID ID WY WY WY WY SD SD SD SD SD SD SD SD WI WI WI WI NY NY MA MA MA MA ME ME .. .. .. .. .. ..",
    # 05:
    ".. .. AK AK AK AK .. .. OR OR OR OR ID ID ID ID WY WY WY WY SD SD SD SD SD SD SD SD WI WI WI WI NY NY MA MA MA MA ME ME .. .. .. .. .. ..",
    # 06:
    ".. .. .. .. .. .. .. .. OR OR OR OR NV NV NV NV WY WY WY WY NE NE NE NE IL IL IL IL WI WI WI WI NY NY CT CT CT CT RI RI .. .. .. .. .. ..",
    # 07:
    ".. .. .. .. .. .. .. .. OR OR OR OR NV NV NV NV WY WY WY WY NE NE NE NE IL IL IL IL WI WI WI WI NY NY CT CT CT CT RI RI .. .. .. .. .. ..",
    # 08:
    ".. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV AZ AZ AZ AZ NE NE NE NE IN IN IN IN MI MI MI MI NY NY NJ NJ CT CT RI RI .. .. .. .. .. ..",
    # 09:
    ".. .. .. .. .. .. .. .. CA CA CA CA NV NV NV NV AZ AZ AZ AZ NE NE NE NE IN IN IN IN MI MI MI MI NY NY NJ NJ CT CT RI RI .. .. .. .. .. ..",
    # 10: HI floating
    ".. .. HI HI HI HI .. .. CA CA CA CA CA CA AZ AZ AZ AZ CO CO CO CO KS KS IN IN IN IN MI MI MI MI OH OH OH OH PA PA DE DE .. .. .. .. .. ..",
    # 11:
    ".. .. HI HI HI HI .. .. CA CA CA CA CA CA AZ AZ AZ AZ CO CO CO CO KS KS IN IN IN IN MI MI MI MI OH OH OH OH PA PA DE DE .. .. .. .. .. ..",
    # 12: AR needs to be above LA/AL.
    ".. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ NM NM OK OK KS KS MO MO MO MO KY KY KY KY WV WV PA PA PA PA MD MD .. .. .. .. .. .. .. ..",
    # 13:
    ".. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ NM NM OK OK KS KS MO MO MO MO KY KY KY KY WV WV PA PA PA PA MD MD .. .. .. .. .. .. .. ..",
    # 14: AR left of TN, below MO
    ".. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ TX TX OK OK AR AR AR AR MO MO TN TN TN TN TN TN VA VA VA VA VA VA .. .. .. .. .. ..",
    # 15:
    ".. .. .. .. .. .. .. .. CA CA CA CA CA CA AZ AZ AZ AZ TX TX OK OK AR AR AR AR MO MO TN TN TN TN TN TN VA VA VA VA VA VA .. .. .. .. .. ..",
    # 16:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ TX TX TX TX AR AR AR AR LA LA AL AL MS MS MS GA GA NC NC NC NC .. .. .. .. .. .. .. .. .. .. ..",
    # 17:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. AZ AZ TX TX TX TX AR AR AR AR LA LA AL AL MS MS MS GA GA NC NC NC NC .. .. .. .. .. .. .. .. .. .. ..",
    # 18:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR AR AR LA LA AL AL MS MS MS GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. ..",
    # 19:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR AR AR LA LA AL AL MS MS MS GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. ..",
    # 20: 
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA AL AL MS MS MS GA GA GA GA SC SC .. .. .. .. .. .. .. .. .. .. ..",
    # 21:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA AL AL MS MS MS GA GA SC SC SC SC .. .. .. .. .. .. .. .. .. .. ..",
    # 22:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. GA GA FL FL .. .. .. .. .. .. .. .. .. .. ..",
    # 23:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. GA GA FL FL .. .. .. .. .. .. .. .. .. .. ..",
    # 24:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL .. .. .. .. .. .. .. .. .. .. ..",
    # 25:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL .. .. .. .. .. .. .. .. .. .. ..",
    # 26:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..",
    # 27:
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .."
]

W = 46
lines = []
for r in new_rows:
    rt = r.split()
    rt.extend(['..'] * (W - len(rt)))
    lines.append(rt)

with open('grid.txt', 'w') as f:
    for row in lines:
        f.write(" ".join(f"{c:2}" for c in row) + "\n")

print("Grid written to grid.txt")
