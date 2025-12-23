import cv2
import threading
import time
import os
from src.camera import Camera
from src.detector import HandDetector
from src.config_manager import ConfigManager
from src.input_controller import InputController
from src.gui import SettingsGUI
from src.tray_icon import TrayIcon
from src.overlay import Overlay

from src.mouse_controller import MouseController

class LazyHandsApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.camera = None
        self.detector = None
        self.input_controller = None
        self.mouse_controller = None
        self.running = True
        self.gui = None
        self.tray = None
        
        self.mode = "GESTURE" # GESTURE or MOUSE
        self.last_mode_toggle = 0

    def detection_loop(self):
        try:
            self.camera = Camera()
            self.detector = HandDetector()
            # Overlay is initialized in run() and assigned to self.overlay
            self.input_controller = InputController(self.config_manager, self.overlay)
            self.mouse_controller = MouseController()
            
            print("Detection Loop Started")
            
            while self.running:
                # If GUI is destroyed (app closing), stop
                if self.gui and not self.gui.is_running:
                     break

                frame = self.camera.read_frame()
                if frame is None:
                    time.sleep(0.1)
                    continue

                result = self.detector.detect(frame)
                gesture_name = "UNKNOWN"
                event_to_show = f"Mode: {self.mode}"

                if result.hand_landmarks:
                    for hand_landmarks in result.hand_landmarks:
                        fingers = self.detector.get_fingers_state(hand_landmarks)
                        gesture_name = self.detector.recognize_gesture(fingers)
                        
                        # Mode Toggle Logic (ROCK gesture)
                        current_time = time.time()
                        if gesture_name == "ROCK" and (current_time - self.last_mode_toggle) > 2.0:
                            self.mode = "MOUSE" if self.mode == "GESTURE" else "GESTURE"
                            self.last_mode_toggle = current_time
                            self.mouse_controller.reset()
                            event_to_show = f"SWITCHED TO {self.mode}"
                        
                        if self.mode == "MOUSE":
                            # Strict Safety Check: Only move/click if Middle/Ring/Pinky are DOWN
                            # This prevents 'Open Palm' or 'Fist' from simulating a mouse
                            if self.detector.is_pointing(fingers):
                                # Mouse Logic - Relative Movement
                                ix, iy = self.detector.get_index_tip_pos(hand_landmarks)
                                self.mouse_controller.move(ix, iy)
                                
                                # Clicking
                                dist = self.detector.detect_pinch(hand_landmarks)
                                self.mouse_controller.check_and_click(dist)
                                
                                # Visual Click Feedback
                                if dist < self.mouse_controller.PINCH_THRESHOLD: 
                                    h, w, _ = frame.shape
                                    thumb = hand_landmarks[4]
                                    index = hand_landmarks[8]
                                    tx, ty = int(thumb.x * w), int(thumb.y * h)
                                    idx, idy = int(index.x * w), int(index.y * h)
                                    cv2.line(frame, (tx, ty), (idx, idy), (0, 0, 255), 3)
                                    cv2.putText(frame, "CLICK", (idx, idy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            else:
                                # If not pointing strictly, reset tracker so we don't jump when we start pointing again
                                self.mouse_controller.reset()
                                cv2.putText(frame, "PAUSED (Point Filter)", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            
                        else:
                            # Gesture Logic
                            swipe = self.detector.detect_swipe(hand_landmarks)
                            final_event = swipe if swipe else gesture_name
                            
                            if final_event == "ROCK": 
                                final_event = "TOGGLING..." # Feedback
                            else:
                                event_to_show = f"{self.mode}: {final_event}"

                            if final_event and final_event != "UNKNOWN" and final_event != "ROCK":
                                self.input_controller.execute_action(final_event)
                        
                        # Draw landmarks
                        h, w, _ = frame.shape
                        for landmark in hand_landmarks:
                            x = int(landmark.x * w)
                            y = int(landmark.y * h)
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                else:
                    # Reset mouse tracking if hand is lost
                    if self.mouse_controller:
                        self.mouse_controller.reset()

                # Show camera preview
                cv2.putText(
                    frame,
                    event_to_show,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255) if self.mode == "MOUSE" else (255, 255, 0),
                    2
                ) 
                cv2.imshow("LazyHands - Cam View", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.quit_app()
                    break
            
            self.camera.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            import traceback
            import datetime
            with open("crash_log.txt", "a") as f:
                f.write(f"\n[{datetime.datetime.now()}] Error: {str(e)}\n")
                f.write(traceback.format_exc())
            print(f"Error in detection loop: {e}")

    def quit_app(self):
        self.running = False
        if self.tray:
            self.tray.icon.stop()
        
        # Schedule GUI destruction on main thread
        if self.gui:
            self.gui.after(0, self.gui.quit_app)

    def run(self):
        # 1. Initialize GUI (Main Thread)
        self.gui = SettingsGUI(self.config_manager, None)
        self.gui.protocol("WM_DELETE_WINDOW", self.gui.on_close)
        
        # Initialize Overlay (requires GUI root)
        self.overlay = Overlay(self.gui)
        
        # 2. Setup Tray (Background Thread)
        def on_settings():
            self.gui.after(0, self.gui.show) # call show on main thread via after

        def on_quit():
            # Run quit_app logic
            self.quit_app()

        self.tray = TrayIcon(on_settings, on_quit)
        self.tray.run_detached()

        # 3. Start Detection (Background Thread)
        thread = threading.Thread(target=self.detection_loop, daemon=True)
        thread.start()
        
        # 4. Run GUI Main Loop
        print("LazyHands is running found in System Tray.")
        try:
            self.gui.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False


if __name__ == "__main__":
    app = LazyHandsApp()
    app.run()