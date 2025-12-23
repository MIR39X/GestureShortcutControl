import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

class HandDetector:
    def __init__(self, model_path='hand_landmarker.task'):
        import sys, os
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)
            
        final_path = resource_path(model_path)
        
        base_options = python.BaseOptions(model_asset_path=final_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Swipe detection state
        self.prev_wrist_x = None
        self.prev_wrist_y = None
        self.SWIPE_THRESHOLD = 0.15 # Increased for cleaner detection
        
        self.last_swipe_event = None
        self.last_swipe_time = 0

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        return self.detector.detect(mp_image)

    def get_fingers_state(self, hand_landmarks):
        fingers = []
        
        # Thumb
        thumb_tip = hand_landmarks[4]
        thumb_pip = hand_landmarks[3]
        fingers.append(1 if thumb_tip.x < thumb_pip.x else 0)

        # Other 4 fingers
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        
        for tip, pip in zip(tips, pips):
            fingers.append(1 if hand_landmarks[tip].y < hand_landmarks[pip].y else 0)
            
        return fingers

    def recognize_gesture(self, fingers):
        if fingers == [1,1,1,1,1]: return "OPEN_PALM"
        elif fingers == [0,0,0,0,0]: return "FIST"
        elif fingers == [0,1,1,0,0]: return "TWO_FINGERS"
        elif fingers == [0,1,1,1,0]: return "THREE_FINGERS"
        elif fingers == [0,1,1,1,1]: return "FOUR_FINGERS"
        elif fingers == [1,0,0,0,0]: return "THUMB"
        # Rock / Spiderman gesture (Index + Pinky) - Allow thumb to be either
        elif fingers == [0,1,0,0,1] or fingers == [1,1,0,0,1]: return "ROCK"
        return "UNKNOWN"

    def is_pointing(self, fingers):
        # Index must be UP. Middle, Ring, Pinky must be DOWN.
        # fingers order: [Thumb, Index, Middle, Ring, Pinky]
        # Allow Thumb to be anything (pinch uses thumb)
        return fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0

    def detect_swipe(self, hand_landmarks):
        wrist = hand_landmarks[0]
        current_x, current_y = wrist.x, wrist.y
        swipe = None
        import time

        if self.prev_wrist_x is not None and self.prev_wrist_y is not None:
            dx = current_x - self.prev_wrist_x
            dy = current_y - self.prev_wrist_y

            candidate = None
            if abs(dx) > abs(dy):
                if dx > self.SWIPE_THRESHOLD: candidate = "SWIPE_RIGHT"
                elif dx < -self.SWIPE_THRESHOLD: candidate = "SWIPE_LEFT"
            else:
                if dy > self.SWIPE_THRESHOLD: candidate = "SWIPE_DOWN"
                elif dy < -self.SWIPE_THRESHOLD: candidate = "SWIPE_UP"
            
            if candidate:
                curr_time = time.time()
                opposites = {
                    "SWIPE_LEFT": "SWIPE_RIGHT", "SWIPE_RIGHT": "SWIPE_LEFT",
                    "SWIPE_UP": "SWIPE_DOWN", "SWIPE_DOWN": "SWIPE_UP"
                }
                
                # Check against last_swipe_event (must ensure it exists in init later)
                last_event = getattr(self, 'last_swipe_event', None)
                last_time = getattr(self, 'last_swipe_time', 0)
                
                if (last_event == opposites.get(candidate) and (curr_time - last_time) < 0.6):
                    swipe = None # Ignored
                else:
                    swipe = candidate
                    self.last_swipe_event = swipe
                    self.last_swipe_time = curr_time

        self.prev_wrist_x = current_x
        self.prev_wrist_y = current_y
        return swipe

    def get_index_tip_pos(self, hand_landmarks):
        tip = hand_landmarks[8] # Index tip
        return tip.x, tip.y

    def detect_pinch(self, hand_landmarks):
        # Distance between Thumb Tip (4) and Index Tip (8)
        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]
        
        # Euclidean distance manually or just approx
        dist = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
        return dist
