import os
import cv2
import pytesseract
import pyttsx3
import numpy as np
from PIL import Image

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_and_process_text():
    """Opens the camera feed and captures a frame ONLY when 'C' is pressed."""
    cap = cv2.VideoCapture(0)  # Use the system's built-in webcam

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Press 'C' to capture a frame and process it.")
    print("Press 'Q' to quit the program.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image from camera.")
                break

            # Display the live camera feed
            cv2.imshow("System Camera - Press 'C' to Capture, 'Q' to Quit", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                print("Capturing frame...")
                process_frame(frame)  # Call function to process the captured frame

            elif key == ord('q'):
                print("Exiting program...")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_frame(frame):
    """Processes the captured frame for OCR and text-to-speech."""
    # Convert frame to grayscale for better OCR accuracy
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to improve text detection
    _, thresh_frame = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply OCR to extract text
    text = pytesseract.image_to_string(thresh_frame, config='--psm 6', lang='eng').strip()

    if text:
        print("Extracted Text:", text)
        text_to_speech_pyttsx3(text)
    else:
        print("No text detected in the captured frame.")

def text_to_speech_pyttsx3(text):
    """Convert extracted text to speech using pyttsx3 with adjustable tone and speed."""
    try:
        engine = pyttsx3.init(driverName='sapi5')  # Force sapi5 driver

        # Set properties for voice and speed
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Select a female voice
        engine.setProperty('rate', 150)  # Set speech speed (default ~200)

        engine.say(text)
        engine.runAndWait()
        print("Speech finished.")

    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

# Run the function to capture and process text
if __name__ == "__main__":
    capture_and_process_text()
