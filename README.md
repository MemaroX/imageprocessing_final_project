# Image Processing Application

This is a simple Python application built using Tkinter for GUI and OpenCV for image processing. It allows users to load an image, apply various filters, and save the processed image.

## Features

- **Load an image** in various formats (JPG, PNG, BMP).
- **Apply a range of filters** to the loaded image:
  - Low Pass Filter
  - High-Pass Filter
  - Mean Filter
  - Median Filter
  - Roberts Edge Detector
  - Prewitt Edge Detector
  - Sobel Edge Detector
  - Erosion
  - Dilation
  - Opening
  - Closing
  - Hough Circle Transform
  - Region Split and Merge
  - Thresholding
- **Save the processed image** with a default filename format: `{filter image} of {original name}.{format}`.

## Installation

1. **Clone this repository** to your local machine:

   ```bash
   git clone https://github.com/MemaroX/imageprocessing_final_project.git

2. **Install the required Python packages:

   ```bash
   pip install -r requirements.txt

3. **Clone this repository** to your local machine:

   ```bash
   python main.py

** Usage
Load Image: Click on the "Load Image" button to select an image file from your computer.
Apply Filter: Choose a filter from the list of available filters.
Adjust Parameters: If applicable, adjust the parameters using the slider.
Apply: Click on the "Apply" button to apply the selected filter.
Save Image: After applying the filter, click on the "Save Image" button to save the processed image.
Requirements
Python 3.6 or higher
OpenCV
Tkinter
NumPy
Contributing
Contributions are welcome! Feel free to open issues and pull requests

