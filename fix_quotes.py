with open("scripts/generate_map.py", "r") as f:
    text = f.read()

# Replace all occurrences of \\' inside the f-objects with \"
text = text.replace("(\\'state\\', \\'{state}\\')", '(\\"state\\", \\"{state}\\")')
text = text.replace("[\\'{state}\\']", '[\\"{state}\\"]')

with open("scripts/generate_map.py", "w") as f:
    f.write(text)
print("Quotes definitely fixed")
