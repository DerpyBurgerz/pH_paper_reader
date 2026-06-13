import cv2
import numpy as np
from io_utils import save_image


def red_mask(image) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2 masks basks because red goes around the 180 part of the hue circle thingy
    lower_red_1 = np.array([0, 30, 30])
    upper_red_1 = np.array([40, 255, 255])

    lower_red_2 = np.array([170, 70, 50])
    upper_red_2 = np.array([180, 255, 255])

    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    # combine the masks into one mask
    mask = cv2.bitwise_or(mask_1, mask_2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # now we have white shapes where the red was
    return mask


def is_valid_rectangle(contour, img_shape, min_area_ratio=0.01, max_aspect_ratio=3.0):
    # Approximate contour
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    if len(approx) != 4:
        return False

    # Area filter
    area = cv2.contourArea(contour)
    img_area = img_shape[0] * img_shape[1]
    if area < min_area_ratio * img_area:
        return False

    # Aspect ratio (width/height) of the bounding rectangle
    rect = cv2.minAreaRect(contour)
    w, h = rect[1]
    if w == 0 or h == 0:
        return False
    aspect = max(w, h) / min(w, h)
    if aspect > max_aspect_ratio:
        return False

    # Optional: check convexity
    if not cv2.isContourConvex(approx):
        return False

    return True, rect  # rect gives center, size, angle

def process_image(image):
    output = image.copy()
    masked_image = red_mask(image)
    save_image(masked_image, "masked_image.png")
    contours, _ = cv2.findContours(masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        valid, rect = is_valid_rectangle(contour, image.shape)

    return output