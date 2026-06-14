from io_utils import load_image, save_image
from universal_indicator_processor import *
import cv2 as cv
import typing


def run():
    input_path = "neutral.jpeg"

    # Load image
    image = load_image(input_path)
    if image is None:
        print("Error: Could not load image.")
        return

    processed_image = canny_process_image(image)
    sobel_process_image(image)
    cnts = find_contours(image)
    #todo! https://medium.com/@siromermer/extracting-chess-square-coordinates-dynamically-with-opencv-image-processing-methods-76b933f0f64e
    # step 9 in that link
    # can be used to fill undetected squares
    centroids = list(zip([get_centroids(c) for c in cnts], cnts))
    sorted_contours = sort_centroids(centroids)

    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    pH_hue_dict = dict()
    for i in range(0, 15):
        pH_hue_dict[i] = [get_hue(hsv, cnt) for cnt in sorted_contours[i]]

    print()

if __name__ == "__main__":
    run()