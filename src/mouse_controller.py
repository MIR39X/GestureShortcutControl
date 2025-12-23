import pyautogui
import time

class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_w, self.screen_h = pyautogui.size()
        
        # State
        self.prev_norm_x = None
        self.prev_norm_y = None
        
        # Sensitivity (Higher = faster cursor)
        self.sensitivity = 1.6 # 1.0 = 1:1 mapping (slow), 2.0 = 2x speed
        
        self.is_pinched = False
        self.PINCH_THRESHOLD = 0.08 # Increased for easier clicks 
        
    def move(self, x_norm, y_norm):
        # Initialize on first detection
        if self.prev_norm_x is None or self.prev_norm_y is None:
            self.prev_norm_x = x_norm
            self.prev_norm_y = y_norm
            return

        # Calculate Delta
        dx = x_norm - self.prev_norm_x
        dy = y_norm - self.prev_norm_y
        
        # Invert dx? 
        # Screen Logic: Left is 0, Right is 1. Camera is mirrored?
        # If camera is mirrored in main.py (flip 1), then:
        # User moves Right -> Camera shows Right -> x increases -> dx > 0.
        # Screen Mouse should move Right -> dx > 0.
        # Seems correct.
        
        # Scale to pixels
        # movement = delta * screen_dimension * sensitivity
        move_x = int(dx * self.screen_w * self.sensitivity)
        move_y = int(dy * self.screen_h * self.sensitivity)
        
        # Apply Movement (Relative)
        pyautogui.move(move_x, move_y)
        
        self.prev_norm_x = x_norm
        self.prev_norm_y = y_norm

    def reset(self):
        self.prev_norm_x = None
        self.prev_norm_y = None

    def check_and_click(self, distance):
        if distance < self.PINCH_THRESHOLD:
            if not self.is_pinched:
                pyautogui.mouseDown()
                self.is_pinched = True
        else:
            if self.is_pinched:
                pyautogui.mouseUp()
                self.is_pinched = False
