import time
import cv2
import pygame
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner  # Import Spinner

class AlarmApp(App):
    def build(self):
        self.alarms = []  # List to store multiple alarms
        self.alarm_ringing = False  # Tracks if an alarm is ringing
        return self.root

    def detect_eyes(self, frame):
        # Detect eyes in the webcam frame
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(eyes) > 0

    def play_alarm(self):
        pygame.mixer.init()
        pygame.mixer.music.load('alarmring.mp3')
        pygame.mixer.music.play(-1)

    def stop_alarm(self):
        pygame.mixer.music.stop()
        self.alarm_ringing = False

    def add_alarm(self, alarm_time):
        # Add a new alarm
        self.alarms.append(alarm_time)
        self.root.ids.status_label.text = f"Alarms set: {', '.join(self.alarms)}"
        label = Label(text=f"Alarm set for {alarm_time}", font_size=16)
        self.root.ids.alarm_list.add_widget(label)
        Clock.schedule_interval(self.check_alarms, 1)

    def check_alarms(self, dt):
        # Check if the current time matches any set alarms
        current_time = time.strftime("%H:%M")
        if current_time in self.alarms and not self.alarm_ringing:
            self.alarms.remove(current_time)  # Remove alarm once it rings
            self.update_status_label(f"Alarm ringing for {current_time}")
            self.play_alarm()
            self.alarm_ringing = True
            self.activate_webcam()

    def activate_webcam(self):
        # Initialize webcam and countdown
        self.cap = cv2.VideoCapture(0)
        self.required_open_time = 5  # Required time (seconds) to keep eyes open
        self.countdown = self.required_open_time
        Clock.schedule_interval(self.update_webcam_frame, 1)  # Check every second

    def update_webcam_frame(self, dt):
        # Capture webcam frame
        ret, frame = self.cap.read()
        if not ret:
            return False

        if self.detect_eyes(frame):
            # Decrease countdown if eyes are detected open
            self.countdown -= 1
            self.update_countdown_label(self.countdown)
            if self.countdown == 0:
                # Stop alarm when countdown reaches zero
                self.update_status_label("Open eyes detected. Alarm stopped.")
                self.stop_alarm()
                self.cap.release()
                cv2.destroyAllWindows()
                self.clear_countdown_label()
                return False  # Stop scheduling this method
        else:
            # Reset countdown if eyes close
            self.countdown = self.required_open_time
            self.update_countdown_label(self.countdown, reset=True)

        # Exit loop if user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.clear_countdown_label()
            return False  # Stop scheduling this method

        return True  # Continue scheduling

    def update_countdown_label(self, countdown, reset=False):
        if reset:
            self.root.ids.countdown_label.text = "Please keep your eyes open for 5 seconds."
        else:
            self.root.ids.countdown_label.text = f"Keep your eyes open: {countdown} seconds left"

    def update_status_label(self, message):
        self.root.ids.status_label.text = message

    def clear_countdown_label(self):
        self.root.ids.countdown_label.text = ""

if __name__ == "__main__":
    AlarmApp().run()
