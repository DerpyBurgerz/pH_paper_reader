import cv2
import oHere’s the issue and the fix.
What the logs mean:
- OpenCV’s GUI (HighGUI) is using a Qt backend. Your environment lacks the Wayland/X11 platform plugin and fonts, so any cv2.imshow/waitKey call triggers those Qt errors.

Long-term solution:
- Remove OpenCV GUI usage and run headless. Save images to disk instead of opening windows. This avoids Qt entirely and runs reliably everywhere.

I’ll refactor your one-file program into an organized, multi-file structure while keeping it minimal:
- io_utils.py: safe image read/save helpers
- processor.py: image processing logic
- main.py: entry point; no GUI, just saves outputs

Below is the updated main.py (you asked for the fixed code to be appended; the rest are new files you can add alongside).s

# ai generated stuff to help with input/output

def load_image(path):
    """Safely loads an image from the given path."""
    if not os.path.exists(path):
        print(f"Error: File {path} not found.")
        return None
    return cv2.imread(path)

def save_image(image, path):
    """Safely saves an image to the given path."""
    success = cv2.imwrite(path, image)
    if success:
        print(f"Image saved to {path}")
    else:
        print(f"Error: Could not save image to {path}")
    return success
