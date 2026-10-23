import cv2
import numpy as np
from PIL import Image

src_path = r'C:\Users\lokes\.gemini\antigravity\brain\caa5acd3-4748-4207-a500-32b7a79c085f\school_bus_isometric_ne_1792734465120.jpg'
out_path = r'C:\tx_dmv\driving_rule_animations_suite\assets\vehicles\school_bus_tx_ne_clean.png'

img = Image.open(src_path).convert('RGB')
arr = np.array(img)
h, w, _ = arr.shape

# Grayscale & brightness
gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

# Find background by flood-filling from borders where gray > 235
# We create a mask for flood fill (h+2, w+2)
flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)

# Binary threshold for initial white background candidate
# Any pixel with gray > 235 and low saturation (difference between max and min channel < 20)
diff = np.max(arr, axis=2).astype(int) - np.min(arr, axis=2).astype(int)
is_white_candidate = (gray > 238) & (diff < 18)

# We want to flood fill from edges to find all exterior background
bg_mask = np.zeros((h, w), dtype=np.uint8)
# Fill from the four corners and border points
border_pts = []
for x in range(0, w, 10):
    border_pts.append((x, 0))
    border_pts.append((x, h - 1))
for y in range(0, h, 10):
    border_pts.append((0, y))
    border_pts.append((w - 1, y))

# Convert candidate to uint8 for cv2
cand_u8 = (is_white_candidate.astype(np.uint8)) * 255
# FloodFill needs connectivity
for px, py in border_pts:
    if cand_u8[py, px] == 255:
        cv2.floodFill(cand_u8, None, (px, py), 128)

# Exterior pure background is where cand_u8 == 128
exterior_pure_bg = (cand_u8 == 128)

# Shadow region: pixels on the ground under the vehicle that are darker than white,
# located in the lower half of the image (y > 450) and outside the main vehicle body
# Let's inspect the shadow
shadow_alpha = np.zeros((h, w), dtype=np.float32)
# Any exterior pixel (or adjacent to pure bg) with gray < 245
for y in range(400, h):
    for x in range(w):
        if gray[y, x] < 248:
            # darkness measure
            darkness = 248.0 - float(gray[y, x])
            if darkness > 2.0:
                shadow_alpha[y, x] = min(darkness * 1.3, 160.0)

# Now, vehicle body is everything that is NOT exterior pure background and NOT ground shadow
# Let's refine vehicle body mask
# Vehicle body is a connected component
# Let's find contours of non-pure-bg
non_bg = (~exterior_pure_bg).astype(np.uint8) * 255
# Morphology close to fill small gaps
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(non_bg, cv2.MORPH_CLOSE, kernel)

# Find largest contour - that's the bus + its immediate shadow
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_cnt = max(contours, key=cv2.contourArea)

# Let's find tire bottom contact points to separate bus body from ground shadow
# In our image, let's find the lowest tire pixels
# The bus tires are black (low gray, e.g. gray < 80)
tire_mask = (gray < 75) & (y_indices := np.arange(h)[:, None] > 550)

# Let's create an RGBA output image
rgba = np.zeros((h, w, 4), dtype=np.uint8)

# For shadow: RGB = (0, 0, 0), A = shadow_alpha
rgba[:, :, 0] = 0
rgba[:, :, 1] = 0
rgba[:, :, 2] = 0
rgba[:, :, 3] = np.clip(shadow_alpha, 0, 180).astype(np.uint8)

# Now place vehicle body on top:
# Where is vehicle body?
# Inside largest contour, and NOT pure white background
body_mask = np.zeros((h, w), dtype=np.uint8)
cv2.drawContours(body_mask, [largest_cnt], -1, 255, -1)

# However, the contour might include ground shadow.
# Ground shadow has high gray (>130) and is at the bottom, OR has very low saturation.
# The bus body is either yellow (diff > 40), or dark black (gray < 85), or tinted glass (gray 70..130), or white roof hatch (inside roof, y < 450)
is_body = np.zeros((h, w), dtype=bool)
for y in range(h):
    for x in range(w):
        if body_mask[y, x] == 255:
            g = float(gray[y, x])
            d = float(diff[y, x])
            if y < 650: # Upper body and roof
                if g < 240 or d > 15: # Not pure white background
                    is_body[y, x] = True
            else: # Lower wheels and bumper area
                # Wheels, bumper, rub rails are dark (g < 90) or yellow body (d > 35)
                if g < 90 or d > 30:
                    is_body[y, x] = True
                elif g < 180 and d > 15:
                    is_body[y, x] = True

# Dilate body slightly to capture antialiased edges
body_u8 = is_body.astype(np.uint8) * 255
# Remove small noise
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(body_u8)
main_label = 0
max_area = 0
for l in range(1, num_labels):
    if stats[l, cv2.CC_STAT_AREA] > max_area:
        max_area = stats[l, cv2.CC_STAT_AREA]
        main_label = l

main_body = (labels == main_label)

# Soft edge antialiasing for body
body_dist = cv2.distanceTransform(main_body.astype(np.uint8), cv2.DIST_L2, 3)
body_alpha = np.clip(body_dist * 255.0, 0, 255).astype(np.uint8)
body_alpha[main_body] = 255

# Apply body over shadow
for c in range(3):
    rgba[:, :, c] = np.where(main_body, arr[:, :, c], rgba[:, :, c])
rgba[:, :, 3] = np.maximum(rgba[:, :, 3], np.where(main_body, 255, 0))

# Clean crop bounding box with padding
# Find non-zero alpha bounding box
alpha_channel = rgba[:, :, 3]
y_nz, x_nz = np.where(alpha_channel > 5)
pad = 10
min_x = max(0, np.min(x_nz) - pad)
max_x = min(w, np.max(x_nz) + pad)
min_y = max(0, np.min(y_nz) - pad)
max_y = min(h, np.max(y_nz) + pad)

cropped = rgba[min_y:max_y, min_x:max_x]
Image.fromarray(cropped).save(out_path)
print(f'Saved extracted bus to {out_path}, size: {cropped.shape[1]}x{cropped.shape[0]}')
