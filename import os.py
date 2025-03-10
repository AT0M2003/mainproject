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

    # Apply OCR to extract text
    text = pytesseract.image_to_string(gray_frame, config='--psm 6', lang='eng').strip()

    if text:
        print("Extracted Text:", text)
        text_to_speech_espeak(text)
    else:
        print("No text detected in the captured frame.")

def text_to_speech_espeak(text):
    """Convert extracted text to speech using eSpeak with a specified female voice and reduced speed."""
    try:
        # Call eSpeak with the female voice en+f2 and reduced speed (-s)
        subprocess.call([r'C:\Program Files\eSpeak\command_line\espeak.exe', '-v', 'en+f2', '-s', '150', text])
        print("Speech finished.")
    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")

# Run the function to capture and process text
if __name__ == "__main__":
    capture_and_process_text()
