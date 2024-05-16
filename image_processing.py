import cv2
import numpy as np
from tkinter import Tk, Frame, Label, Scale, Button
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessing:

    def __init__(self):
        self.kernel_size = 5  # Default kernel size

    def apply_low_pass_filter(self,image):
        kernel_size = self.kernel_size if self.kernel_size % 2 == 1 else self.kernel_size + 1
        lp_img = cv2.GaussianBlur(image,(kernel_size,kernel_size),0)
        return lp_img
    def apply_hpf(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Ensure the kernel size is odd
        kernel_size = self.kernel_size if self.kernel_size % 2 == 1 else self.kernel_size + 1
        blurred_image = cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)
        hpf_image = cv2.subtract(gray_image, blurred_image)
        return hpf_image

    def apply_mean_filter(self, image):
        mean_image = cv2.blur(image, (self.kernel_size, self.kernel_size))
        return mean_image

    def apply_median_filter(self, image):
        kernel_size = self.kernel_size if self.kernel_size % 2 == 1 else self.kernel_size + 1
        median_image = cv2.medianBlur(image, self.kernel_size)
        return median_image

    def apply_roberts_edge_detector(self, image):
        kernel_x = np.array([[1, 0], [0, -1]])
        kernel_y = np.array([[0, 1], [-1, 0]])
        image_x = cv2.filter2D(image, -1, kernel_x)
        image_y = cv2.filter2D(image, -1, kernel_y)
        roberts_image = cv2.addWeighted(image_x, 0.5, image_y, 0.5, 0)
        return roberts_image

    def apply_prewitt_edge_detector(self, image):
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        image_x = cv2.filter2D(image, -1, kernel_x)
        image_y = cv2.filter2D(image, -1, kernel_y)
        prewitt_image = cv2.addWeighted(image_x, 0.5, image_y, 0.5, 0)
        return prewitt_image

    def apply_sobel_edge_detector(self, image):
        kernel_size = min(max(self.kernel_size, 3), 31) if self.kernel_size % 2 == 1 else min(max(self.kernel_size + 1, 3), 31)
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
        sobel_image = cv2.magnitude(sobel_x, sobel_y)
        return sobel_image

    def apply_erosion(self, image):
        kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)
        erosion_image = cv2.erode(image, kernel, iterations=1)
        return erosion_image

    def apply_dilation(self, image):
        kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)
        dilation_image = cv2.dilate(image, kernel, iterations=1)
        return dilation_image

    def apply_open(self, image):
        kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)
        open_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return open_image

    def apply_close(self, image):
        kernel = np.ones((self.kernel_size, self.kernel_size), np.uint8)
        close_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return close_image

    def apply_hough_circle_transform(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
        return image
    def apply_thresholding(self, image, threshold_value):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        _, thresholded_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
        return thresholded_image
    

    def apply_region_split_and_merge(self, image):

    # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the homogeneity criterion
        def homogeneous(region):
        # This is a placeholder. You'll need to define your own criterion.
        # For example, you might check if the standard deviation of the region is below a certain threshold.
            return np.std(region) < 10

    # Define the split function
        def split(region):
        # Split the region into four equal parts
            h, w = region.shape
            return region[:h//2, :w//2], region[:h//2, w//2:], region[h//2:, :w//2], region[h//2:, w//2:]

    # Define the merge function
        def merge(regions):
        # Merge four regions into one
            top = np.hstack(regions[:2])
            bottom = np.hstack(regions[2:])
            return np.vstack([top, bottom])

    # Apply region split and merge to the image
        segmented_image = self.region_split_and_merge(gray_image, homogeneous, split, merge)

        return segmented_image

    def region_split_and_merge(self, region, homogeneous, split, merge):
    # If the region is homogeneous, return it as is
        if homogeneous(region) or min(region.shape) < 2:
            return region
    # Otherwise, split the region, recursively apply region split and merge to the sub-regions, and merge the results
        else:
            return merge([self.region_split_and_merge(sub_region, homogeneous, split, merge) for sub_region in split(region)])
