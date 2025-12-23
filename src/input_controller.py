import pyautogui
import time
from src.window_manager import WindowManager

class InputController:
    def __init__(self, config_manager, overlay=None):
        self.config_manager = config_manager
        self.window_manager = WindowManager()
        self.overlay = overlay
        self.last_gesture = None
        self.last_time = 0

        self.COOLDOWN = 1.0  # seconds
        pyautogui.FAILSAFE = True

    def execute_action(self, gesture_name):
        current_time = time.time()
        
        if gesture_name == "UNKNOWN" or not gesture_name:
            return

        # Cooldown check: prevent spamming the same gesture
        # Allow different gestures to fire immediately
        if gesture_name == self.last_gesture and (current_time - self.last_time) < self.COOLDOWN:
            return

        app_name = self.window_manager.get_active_app_name() or "default"
        # Optional: Print active app for debugging
        # print(f"Active App: {app_name}")

        mapping = self.config_manager.get_mapping(gesture_name, app_name)
        if mapping:
            print(f"Executing ({app_name}): {gesture_name} -> {mapping}")
            
            # Smart execution:
            # 1. If all keys are the same (e.g. volumeup, volumeup...), press sequentially
            if len(mapping) > 1 and all(x == mapping[0] for x in mapping):
                pyautogui.press(mapping[0], presses=len(mapping))
            # 2. Otherwise treat as hotkey (e.g. ctrl, c)
            else:
                pyautogui.hotkey(*mapping)
            
            if self.overlay:
                display_msg = "Volume" if "volume" in str(mapping) else f"{mapping}"
                self.overlay.show_message(f"{gesture_name}: {display_msg}")
                
            self.last_gesture = gesture_name
            self.last_time = current_time
