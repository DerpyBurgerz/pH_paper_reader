import cv2

def process_image(image):
    # Example: convert to grayscale or apply some filter
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray
