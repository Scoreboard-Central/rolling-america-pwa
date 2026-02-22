import cv2
import numpy as np

img = cv2.imread('/Users/blakelamb/.gemini/antigravity/brain/c69cf3e6-83de-46c2-b5a9-b0ae3afa0feb/media__1771736120277.jpg')
print("Image shape:", img.shape)

# Just save chunks
h, w = img.shape[:2]
cv2.imwrite('chunk_orange_blue.jpg', img[h//4:h*3//4, w//8:w//2])
cv2.imwrite('chunk_green_yellow.jpg', img[h//4:h, w//3:w*2//3])
cv2.imwrite('chunk_red_purple.jpg', img[h//4:h*3//4, w//2:w])
