import os
import cv2
import pytesseract
from gtts import gTTS
import subprocess

# Tesseract default path on Raspberry Pi (no need for Windows path)
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

# ---- MOBILE CAMERA CONFIGURATION ----
MOBILE_IP = '192.168.156.36'  # Change to your phone IP
PORT = '8080'                 
CAMERA_STREAM_URL = f'http://{MOBILE_IP}:{PORT}/video'

def capture_and_process_text():
    """Opens mobile camera feed and captures a frame ONLY when 'C' is pressed."""
    cap = cv2.VideoCapture(CAMERA_STREAM_URL)

    if not cap.isOpened():
        print("Error: Could not access the mobile camera stream.")
        return

    print("Press 'C' to capture a frame and process it.")
    print("Press 'Q' to quit the program.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image from mobile camera stream.")
                break

            # Display the live mobile camera feed
            cv2.imshow("Mobile Camera - Press 'C' to Capture, 'Q' to Quit", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):
                print("Capturing frame...")
                process_frame(frame)

            elif key == ord('q'):
                print("Exiting program...")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_frame(frame):
    """Processes the captured frame for OCR and text-to-speech."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_frame, config='--psm 6', lang='eng').strip()

    if text:
        print("Extracted Text:", text)
        text_to_speech_google(text)
    else:
        print("No text detected.")

def text_to_speech_google(text):
    """Convert extracted text to speech using Google Text-to-Speech (gTTS) and play it."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)

        temp_audio_path = os.path.join(os.getcwd(), "speech.mp3")
        tts.save(temp_audio_path)

        # Use omxplayer for playback on Pi
        subprocess.run(['omxplayer', temp_audio_path])

        os.remove(temp_audio_path)
        print("Speech finished.")

    except Exception as e:
        print(f"Speech synthesis error: {e}")

if __name__ == "__main__":
    capture_and_process_text()
