import psutil
import win32gui
import win32process
import os

class WindowManager:
    def get_active_app_name(self):
        try:
            # Get the foreground window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Get the process ID from the window handle
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            if pid <= 0:
                return None
                
            # Get the process name from the PID
            process = psutil.Process(pid)
            process_name = process.name()  # e.g., "chrome.exe"
            
            return process_name.lower()
        except Exception:
            return None
