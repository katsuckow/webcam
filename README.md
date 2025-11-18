# webcam.py — Document alignment and OCR demo

This repository contains a small demo script `webcam.py` that captures frames from a webcam, attempts to detect and perspective-correct a document region, and prepares the image for OCR using Tesseract (via `pytesseract`). The script shows a live video window and allows you to inspect the aligned/corrected document when you press ESC.

**Contents**
- `webcam.py`: main script that captures video, finds document contour, applies perspective transform and shows the aligned result.

**Prerequisites**
- Python 3.7+ (tested with recent Python 3.x versions)
- Install required Python packages:

```powershell
pip install opencv-python numpy pytesseract
```

- Install Tesseract OCR for your platform:
  - Windows: install from https://github.com/tesseract-ocr/tesseract/releases and note the installation path (default: `C:\Program Files\Tesseract-OCR\tesseract.exe`).

**Configuration**
- The script sets `pytesseract.pytesseract.tesseract_cmd` to a hard-coded Windows path:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
```

If your Tesseract executable is located elsewhere, update that line in `webcam.py` to point to the correct path (and include the `.exe` if needed).

**Usage**

1. Connect a webcam and make sure it is available (default camera index 0).
2. From the folder containing `webcam.py`, run:

```powershell
python webcam.py
```

3. A live window named `video` will open. The script captures frames and attempts to detect the largest contour (the document).
4. Press `ESC` (key code 27) to stop the live capture — the script will then show the aligned image in a window named `Aligned` and wait for a key press.

**How it works (quick overview)**
- The `align(document, rotated)` function in `webcam.py`:
  - Converts the captured image to grayscale and thresholds it.
  - Finds contours, sorts by area, and approximates the polygon for the largest contour.
  - Computes a perspective transform (homography) from the detected quadrilateral to a rectangular output and warps the document image.
  - Returns the annotated copy and the aligned (warped/thresholded) result.

- The main loop reads frames, crops a center region, calls `align()` and displays live video. After pressing ESC the aligned result is shown for inspection.

**Tweaks and tips**
- If the script fails to detect a good contour, it falls back to an adaptive threshold branch; you may want to tune threshold values or the contour approximation epsilon (currently `0.1 * perimeter`).
- The script currently assumes a 90-degree rotation (`cv.ROTATE_90_CLOCKWISE`) for display — adjust rotation or cropping logic to fit your camera orientation and document size.
- To use a different camera index, change `cv.VideoCapture(0)` to another index (for example `1`).

**Troubleshooting**
- If you get errors about Tesseract not found, verify the `tesseract_cmd` path and that Tesseract is installed. You can run `tesseract --version` in a terminal to confirm.
- If the camera doesn't open, verify the correct camera index and that no other app is using the camera.
- If the aligned output looks distorted, try adjusting the polygon approximation parameter or print the detected corner coordinates for debugging.

**Notes**
- This script is a demo and is not production-ready. It has minimal error handling and uses fixed parameters that may need tuning for different cameras or documents.
- Feel free to fork and adapt: improvements could include better contour filtering, user-controlled capture, saving aligned images, and direct OCR invocation via `pytesseract.image_to_string()` on the aligned frame.

**License & attribution**
- No license is specified. If you want to use or publish this code, consider adding a `LICENSE` file to the repository.

--
Created from the contents of `webcam.py` to document usage, dependencies and quick tips.
# Camera Reader Project

## Overview
This project contains Python scripts for capturing webcam video and performing optical character recognition (OCR) on video frames in real-time.

## Files

### CameraReader1.py
A real-time OCR application that captures webcam video and extracts text from each frame using Tesseract OCR.

**Features:**
- Real-time webcam capture
- Image preprocessing (grayscale conversion, median blur, adaptive thresholding)
- OCR text extraction using Tesseract
- Live display of processed frames with detected text overlay

**Key Functions:**
- Converts frames to grayscale for better OCR accuracy
- Applies median blur to reduce noise
- Uses adaptive Gaussian thresholding for optimal text detection in varying lighting conditions
- Extracts text data and metadata from frames
- Displays processed frames with detected text

**Controls:**
- Press `q` to quit the application

### webcam.py
A document alignment and perspective correction tool for webcam video.

**Features:**
- Real-time webcam capture with 90° rotation
- Document detection and edge finding
- Automatic perspective correction
- Contour detection and analysis
- Document alignment using homography transformation

**Key Functions:**
- `align(x, rotated)`: Processes a frame to detect document boundaries and apply perspective correction
  - Converts to grayscale
  - Applies thresholding
  - Finds contours and identifies the largest (document)
  - Detects corner points
  - Applies perspective transformation to straighten document
  - Fallback error handling with adaptive thresholding

**Controls:**
- Press `ESC` (key 27) to stop capture and display aligned document

### CameraReader.py
*(File present but not yet documented)*

## Requirements

### Python Packages
```bash
pip install opencv-python
pip install numpy
pip install pytesseract
```

### System Dependencies
- **Tesseract OCR**: Must be installed on your system
  - Windows: Download from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
  - Default installation path: `C:/Program Files/Tesseract-OCR/tesseract`
  - Update the path in the code if installed elsewhere

## Configuration

### Tesseract Path
If Tesseract is installed in a different location, update this line in the scripts:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
```

### OCR Configuration (CameraReader1.py)
The OCR is configured with:
- `--oem 3`: OCR Engine Mode 3 (Default, based on what is available)
- `--psm 6`: Page Segmentation Mode 6 (Assume a single uniform block of text)
- Language: English (`eng`)

Adjust these parameters in the `custom_config` variable for different document types.

### Threshold Parameters
**CameraReader1.py:**
- Median blur kernel: 1
- Adaptive threshold block size: 21
- Adaptive threshold constant: 12

**webcam.py:**
- Binary threshold: 170-250
- Adaptive threshold block size: 21
- Adaptive threshold constant: 10

## Usage

### Running CameraReader1.py
```bash
python CameraReader1.py
```
- The webcam will activate
- Each frame is processed for OCR
- Detected text is printed to console and displayed on frame
- Press `q` to exit

### Running webcam.py
```bash
python webcam.py
```
- The webcam will activate with a 90° rotation
- Place a document in view
- The system will detect and align the document
- Press `ESC` to see the final aligned result

## Troubleshooting

### OpenCV GUI Error
If you encounter:
```
cv2.error: The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Cocoa support
```
Reinstall OpenCV:
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python
```

### Poor OCR Results
- Ensure good lighting
- Hold documents steady
- Adjust threshold parameters
- Try different PSM modes (1-13)
- Ensure text is clearly visible and in focus

### Webcam Not Found
- Check camera permissions
- Verify camera index (change `0` in `cv.VideoCapture(0)` to `1`, `2`, etc.)
- Ensure no other application is using the camera

## Known Issues
- `webcam.py` line 50: Uses `cv.contoursArea` (should be `cv.contourArea`)
- Exception handling in `align()` function could be more specific
- `scale_2` vs `scale2` variable naming inconsistency

## Future Improvements
- Add support for multiple document detection
- Implement automatic language detection
- Save processed documents to file
- Add configuration file for parameters
- Improve error handling and logging

## License
*(Add your license information here)*

## Author
*(Add your information here)*
