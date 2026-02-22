from PIL import Image

img = Image.open('/Users/blakelamb/.gemini/antigravity/brain/c69cf3e6-83de-46c2-b5a9-b0ae3afa0feb/media__1771736120277.jpg')
print("Image size:", img.size)
w, h = img.size

# Save cropped sections so they are easier to look at!
img.crop((int(w*0.1), int(h*0.2), int(w*0.4), int(h*0.7))).save('orange_blue.jpg')
img.crop((int(w*0.3), int(h*0.3), int(w*0.6), int(h*0.8))).save('green_yellow.jpg')
img.crop((int(w*0.5), int(h*0.2), int(w*0.9), int(h*0.7))).save('red_purple.jpg')
print("Saved crops")
