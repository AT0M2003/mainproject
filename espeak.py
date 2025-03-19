import os
import cv2
import subprocess
import pytesseract
from PIL import Image
import numpy as np

# Set the ESPEAK_DATA_PATH environment variable to the correct path
os.environ['ESPEAK_DATA_PATH'] = r'C:\Program Files\eSpeak\espeak-data'

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_extract_text():
    """Capture an image from the camera, perform OCR, and extract text."""
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None

    print("Press 'q' to quit the real-time extraction.")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image from camera.")
                break

            # Convert frame to grayscale for better OCR accuracy
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the frame in a window
            cv2.imshow("Camera - Press 'q' to quit", gray_frame)

            # Apply OCR to the frame
            text = pytesseract.image_to_string(gray_frame).strip()

            # If text is detected, speak it
            if text:
                print("Extracted Text:", text)
                text_to_speech_espeak(text)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera and close OpenCV window
        cap.release()
        cv2.destroyAllWindows()

def text_to_speech_espeak(text):
    """Convert extracted text to speech using eSpeak with a specified female voice."""
    try:
        # Call eSpeak with the female voice en+f2
        subprocess.call([r'C:\Program Files\eSpeak\command_line\espeak.exe', '-v', 'en+f2', text])
        print("Speech finished.")
    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")

# Run the real-time extraction function
if __name__ == "__main__":
    capture_and_extract_text()
