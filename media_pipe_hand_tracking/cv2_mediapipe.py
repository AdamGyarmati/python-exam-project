import cv2
import mediapipe as mp
from utils.utils import SCREEN_HEIGHT, SCREEN_WIDTH


class CV2_MediaPipe:
    def __init__(self):
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(min_detection_confidence=0.1, min_tracking_confidence=0.1)
        self._cap = cv2.VideoCapture(0)

    def get_hand_coordinate(self):
        success, frame = self._cap.read()
        if not success:
            return

        # Flip és RGB átalakítás
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe kéz követés
        results = self._hands.process(rgb_frame)

        # Kéz koordináták lekérése
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Középső ujj tövének koordinátája, kéz közepe
                x = int(hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * SCREEN_WIDTH)
                y = int(hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * SCREEN_HEIGHT)
                return x, y

        return None

    def is_closed(self):
        success, frame = self._cap.read()
        if not success:
            return

        # Flip és RGB átalakítás
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # MediaPipe kéz követés
        results = self._hands.process(rgb_frame)

        # Kéz koordináták lekérése
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Középső ujj teteje a tenyér közepe alatt van-e (csapás)
                _, y = (
                    hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * SCREEN_WIDTH,
                    hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * SCREEN_HEIGHT,
                )
                _, y1 = (
                    hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * SCREEN_WIDTH,
                    hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * SCREEN_HEIGHT,
                )

                if y1 > y:
                    return True
                else:
                    return False
