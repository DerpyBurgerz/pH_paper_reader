import cv2
import os

# ai generated stuff to help with input/output

def load_image(path):
    """Safely loads an image from the given path."""
    if not os.path.exists(path):
        print(f"Error: File {path} not found.")
        return None
    return cv2.imread(path)

def save_image(image, path):
    """Safely saves an image to the given path."""
    path = "images/" + path
    success = cv2.imwrite(path, image)
    if success:
        print(f"Image saved to {path}")
    else:
        print(f"Error: Could not save image to {path}")
    return success
