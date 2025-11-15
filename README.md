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
