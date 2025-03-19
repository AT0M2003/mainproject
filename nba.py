import os
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound

# Specify the path to the Tesseract executable (Update if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# ---- MOBILE CAMERA CONFIGURATION ----
# Replace with your phone's IP and port shown in IP Webcam app
MOBILE_IP = '192.168.x.x'  # <<<<<<<< CHANGE THIS
PORT = '8080'              # Default port

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
        text_to_speech_google(text)
    else:
        print("No text detected in the captured frame.")

def text_to_speech_google(text):
    """Convert extracted text to speech using Google Text-to-Speech (gTTS)."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)

        # Create a custom temp directory
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)

        temp_audio_path = os.path.join(temp_dir, "speech.mp3")
        tts.save(temp_audio_path)

        playsound(temp_audio_path)
        print("Speech finished.")

        os.remove(temp_audio_path)

    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")

# Run the function to capture and process text
if __name__ == "__main__":
    capture_and_process_text()
