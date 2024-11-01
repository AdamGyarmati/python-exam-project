import cv2
import mediapipe as mp
from utils.utils import SCREEN_HEIGHT, SCREEN_WIDTH
import time


class CV2_MediaPipe:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.cap = cv2.VideoCapture(0)

    def get_hand_coordinate(self):
        success, frame = self.cap.read()
        if not success:
            return

        # Flip és RGB átalakítás
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe kéz követés
        results = self.hands.process(rgb_frame)

        # Kéz koordináták lekérése
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Index ujj hegyének koordinátái
                x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * SCREEN_WIDTH)
                y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * SCREEN_HEIGHT)
                yield x, y

        return None

    def is_closed(self):
        success, frame = self.cap.read()
        if not success:
            return

        # Flip és RGB átalakítás
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe kéz követés
        results = self.hands.process(rgb_frame)

        # Kéz koordináták lekérése
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x, y = hand_landmarks.landmark[9].x * SCREEN_WIDTH, hand_landmarks.landmark[9].y * SCREEN_HEIGHT
                x1, y1 = hand_landmarks.landmark[12].x * SCREEN_WIDTH, hand_landmarks.landmark[12].y * SCREEN_HEIGHT

                if y1 > y:
                    return True
                else:
                    return False
