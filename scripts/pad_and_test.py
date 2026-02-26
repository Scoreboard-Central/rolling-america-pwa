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

    import re
    with open('make_map.py', 'r') as f: code = f.read()
    joined = ",\n    ".join('"' + " ".join(r) + '"' for r in fixed)
    new_code = re.sub(r'grid_lines = \[(.*?)\]', f'grid_lines = [\n    {joined}\n]', code, flags=re.DOTALL)
    with open('make_map.py', 'w') as f: f.write(new_code)

run()
