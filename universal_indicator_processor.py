import cv2 as cv
import numpy as np
from io_utils import save_image
import typing

#/home/derpy/PycharmProjects/pH_paper_reader/universal_indicator_processor.py
def find_contours(image):
    image = cv.dilate(image, None, iterations=5)
    image = cv.erode(image, None, iterations=5)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv.filter2D(blur, -1, sharpen_kernel)
    save_image(sharpen, "sharpen.png")

    # Threshold and morph close
    thresh = cv.threshold(sharpen, 170, 255, cv.THRESH_BINARY_INV)[1]
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    close = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=2)
    open = cv.morphologyEx(close, cv.MORPH_OPEN, kernel, iterations=2)

    save_image(open, "open.png")

    # Find contours and filter using the threshold area
    cnts = cv.findContours(open, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    median_area = np.median([cv.contourArea(c) for c in cnts])
    cnts = [c for c in cnts if cv.contourArea(c) * 0.8 < median_area < cv.contourArea(c) * 1.2]
    #todo: remove this copy once finished. Not needed in end thing, is here purely for debugging
    contour_image = image.copy()
    cv.drawContours(contour_image, cnts, -1, (255, 255, 0), 2)
    save_image(contour_image, "contours.png")

    if len(cnts) != 64:
        print("Error: Expected 64 contours, found {}".format(len(cnts)))

    # min_area = 4000
    # max_area = 6000
    # image_number = 0
    # for c in cnts:
    #     area = cv.contourArea(c)
    #     print(area)
    #     x, y, w, h = cv.boundingRect(c)
    #     ROI = image[y:y + h, x:x + w]
    #     save_image(ROI, "ROI/{}.png".format(image_number))
    #     cv.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    #     image_number += 1

    return cnts

# returns centroid as a tuple (x, y)
def get_centroids(contour) -> typing.Tuple[int, int]:
    m = cv.moments(contour)
    return int(m['m10'] / m['m00']), int(m['m01'] / m['m00'])

# takes a list of tuples of centroids and contours.
# Sorts them by the centroid
# returns a dictionary for the pH values 0 to 14 with the contours sorted by y position
def sort_centroids(centroid_contour_tuple):
    # we use tup: tup[0] to sort only on the centroid and ignore the contour in the list of tuple
    # tup[0][0] is x coordinate of centroid
    x_sorted = sorted(centroid_contour_tuple, key=lambda tup: tup[0][0])


    temporary_dict = dict()
    for i in range(0, 8):
        temporary_dict[i] = x_sorted[i*4:i*4+4]
    for i in range(8, 15):
        temporary_dict[i] = x_sorted[i*4+4:i*4+8]

    contour_dict = dict()
    for i in range(0, 15):
        tups = temporary_dict[i]
        # sort by y coordinate
        tups.sort(key=lambda tup: tup[0][1])
        cnts = [contour for centroid, contour in tups]
        contour_dict[i] = cnts

    return contour_dict

def canny_process_image(image):
    image = cv.dilate(image, None, iterations=3)
    image = cv.erode(image, None, iterations=3)
    edges = cv.Canny(image, 120, 300)
    save_image(edges, "canny_edges.png")
    return image

def sobel_process_image(image):
    horizontal_sobel = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3)
    vertical_sobel = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=3)

    abs_sobel_horizontal = np.absolute(horizontal_sobel)
    abs_sobel_vertical = np.absolute(vertical_sobel)

    sobel_magnitude = np.sqrt(abs_sobel_horizontal**2 + abs_sobel_vertical**2)
    scaled_sobel = np.uint8(255*sobel_magnitude/np.max(sobel_magnitude))
    save_image(scaled_sobel, "scaled_sobel.png")

    return image