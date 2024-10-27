import time
import cv2
import pygame
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

class AlarmApp(App):
    def build(self):
        return self.root

    def detect_eyes(self, frame):
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

    def start_alarm(self, alarm_time):
        self.alarm_time = alarm_time
        self.root.ids.status_label.text = f"Alarm set for {self.alarm_time}"
        Clock.schedule_interval(self.check_time, 1)

    def check_time(self, dt):
        current_time = time.strftime("%H:%M")
        if current_time == self.alarm_time:
            self.root.ids.status_label.text = "Alarm ringing..."
            self.play_alarm()
            Clock.unschedule(self.check_time)
            self.activate_webcam()

    def activate_webcam(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if self.detect_eyes(frame):
                self.root.ids.status_label.text = "Open eyes detected. Alarm stopped."
                self.stop_alarm()
                break
            else:
                self.root.ids.status_label.text = "No open eyes detected. Alarm continues..."

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    AlarmApp().run()
