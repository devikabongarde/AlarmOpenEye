import cv2
import time
import pygame

def detect_eyes(frame):
    # Load the pre-trained Haar Cascade for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return len(eyes) > 0

def play_alarm():
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound file
    pygame.mixer.music.load('alarmring.mp3')
    # Play the sound
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

def stop_alarm():
    # Stop the alarm sound
    pygame.mixer.music.stop()

def main():
    # Set the time for the alarm
    alarm_time = "01:53"  # Change this to your desired alarm time
    print("Alarm set for", alarm_time)

    while True:
        current_time = time.strftime("%H:%M")
        print("Current time:", current_time)
        if current_time == alarm_time:
            print("Alarm ringing...")
            play_alarm()
            
            # Initialize webcam
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if detect_eyes(frame):
                    print("Open eyes detected. Alarm stopped.")
                    stop_alarm()
                    break
                else:
                    print("No open eyes detected. Alarm continues...")

                # Display the frame (for debugging purposes)
                cv2.imshow('Alarm', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            break

        time.sleep(30)  # Check the time every 30 seconds

if __name__ == "__main__":
    main()
