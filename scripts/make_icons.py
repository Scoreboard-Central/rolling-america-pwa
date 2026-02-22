import os
import subprocess

IMAGE_PATH = "/Users/blakelamb/.gemini/antigravity/brain/c69cf3e6-83de-46c2-b5a9-b0ae3afa0feb/rolling_america_logo_1771802027407.png"
out_dir = "src/assets/icons"
os.makedirs(out_dir, exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    out_file = os.path.join(out_dir, f"icon-{size}x{size}.png")
    subprocess.run(["sips", "-s", "format", "png", "-z", str(size), str(size), IMAGE_PATH, "--out", out_file])

# Make favicon.ico (let's do 32x32 for ico format)
fav_out = "src/favicon.ico"
subprocess.run(["sips", "-z", "32", "32", "-s", "format", "ico", IMAGE_PATH, "--out", fav_out])
print("Icons generated!")
