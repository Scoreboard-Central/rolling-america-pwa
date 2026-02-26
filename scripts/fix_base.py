import re

def run():
    grid_lines = [
        ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
        ".. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ME ME ..",
        ".. .. AK AK AK .. .. WA WA WA MT MT MT ND ND MN MN WI WI MI MI MI .. .. .. VT VT NH NH ME ME ..",
        ".. .. AK AK AK .. .. WA WA WA ID MT MT SD SD MN MN WI WI MI MI MI NY NY NY NY VT VT NH NH MA MA",
        ".. .. AK AK AK .. .. OR OR OR ID ID WY SD SD SD IA WI IL IL MI MI MI NY NY NY MA CT MA MA MA RI",
        ".. .. .. .. .. .. .. OR OR OR NV ID WY WY WY NE IA IA IL IL IN IN OH OH PA PA NJ NY CT CT CT RI",
        ".. .. .. .. .. .. .. CA CA NV NV UT WY WY CO NE NE MO IL IN OH OH PA PA PA PA DE DE DE DE .. ..",
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

    max_w = max(len(l.split()) for l in grid_lines)
    fixed = []
    for l in grid_lines:
        words = l.split()
        words.extend(['..'] * (max_w - len(words)))
        fixed.append(words)

    fixed[6][20] = 'IN'
    fixed[6][19] = 'IL'
    
    # Fix GA touching TN. 
    # R10 has TN at 21, 23, 24, 25.
    # R11 has MS MS AL GA GA GA.
    # Col 21: AR. 22: AR. 23: MS. 24: MS. 25: AL. 26: GA.
    # TN is at R10[25]. AL is at R11[25]. GA is at R11[26].
    # So TN doesn't touch GA.
    # Let's make GA touch TN by putting GA at R11[25] and AL at R11[24]. MS at 22, 23.
    # R11: AR(20) AR(21) MS(22) MS(23) AL(24) GA(25) GA(26) GA(27)
    fixed[11][20] = 'AR'
    fixed[11][21] = 'AR'
    fixed[11][22] = 'MS'
    fixed[11][23] = 'MS'
    fixed[11][24] = 'AL'
    fixed[11][25] = 'GA'
    
    # Fix missing IA, NM, ME errors
    # Wait, the error was because they "aren't connected". 
    # Check test_map_rules.py to see why it says they aren't connected!
    
    with open('make_map.py', 'w') as f:
        joined = ",\n    ".join('"' + " ".join(r) + '"' for r in fixed)
        f.write(f'grid_lines = [\n    {joined}\n]')
        
run()
