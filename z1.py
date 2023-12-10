import cv2
import pyaudio
import speech_recognition as sr

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize the audio recorder
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# Initialize the speech recognizer
r = sr.Recognizer()

while True:
    # Capture the frame from the camera
    ret, frame = cap.read()

    # Read the audio from the microphone
    audio_data = stream.read(1024)

    # Convert the audio data to text
    try:
        text = r.recognize_google(audio_data)
    except:
        text = ""

    # Display the text on the image
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Image", frame)

    # Exit the program if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the resources
cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
p.terminate()
