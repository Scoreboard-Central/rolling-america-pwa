grid_lines = [
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME ..",
    ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH MA MA",
    ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI NY NY NY NY MA CT MA MA MA RI",
    ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN IN OH PA PA NY NJ CT CT CT RI RI",
    ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA DE NJ DE DE .. ..",
    ".. .. .. .. .. .. .. CA CA NV NV UT UT CO CO CO KS KS MO IL KY OH OH WV PA PA MD MD DE DE .. ..",
    ".. .. HI HI HI .. .. CA CA AZ NV UT UT CO CO CO KS KS KS MO MO KY KY KY WV WV MD MD MD .. .. ..",
    ".. .. HI HI HI .. .. CA CA AZ AZ AZ NM NM NM OK OK OK MO MO KY KY VA VA VA VA MD MD .. .. .. ..",
    ".. .. .. .. .. .. .. CA CA AZ AZ AZ AZ NM NM TX TX OK OK AR TN MO TN TN TN NC VA NC NC NC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX AR AR MS MS AL GA GA GA SC SC SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. TX TX TX TX LA LA MS MS AL AL GA GA GA GA SC .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. LA LA LA LA LA MS MS AL AL AL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL FL .. .. ..",
    ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. FL FL FL .. .. .. .."
]

lines = [l.split() for l in grid_lines]
# MI touches OH?
def t_horiz(a,b):
    for y in range(len(lines)):
        for x in range(len(lines[y])-1):
            if set([lines[y][x], lines[y][x+1]]) == {a, b}:
                return True
    return False

def t_vert(a,b):
    for y in range(len(lines)-1):
        for x in range(len(lines[y])):
            if set([lines[y][x], lines[y+1][x]]) == {a, b}:
                return True
    return False

def touches(a,b):
    return t_horiz(a,b) or t_vert(a,b)

# PA needs NY, NJ
print(f"PA touches NJ: {touches('PA', 'NJ')}")
print(f"PA touches NY: {touches('PA', 'NY')}")
# NY needs PA, NJ, VT, MA, CT (touches 3)
print(f"NY touches PA: {touches('NY', 'PA')}")
print(f"NY touches NJ: {touches('NY', 'NJ')}")
print(f"NY touches VT: {touches('NY', 'VT')}")
print(f"NY touches MA: {touches('NY', 'MA')}")
print(f"NY touches CT: {touches('NY', 'CT')}")

# MI needs OH
print(f"MI touches OH: {touches('MI', 'OH')}")
# OH needs MI
print(f"OH touches MI: {touches('OH', 'MI')}")

# IN needs KY
print(f"IN touches KY: {touches('IN', 'KY')}")
# KY needs IN
print(f"KY touches IN: {touches('KY', 'IN')}")
