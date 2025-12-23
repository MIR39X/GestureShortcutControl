import customtkinter as ctk
import time
import threading
import win32gui
import win32con
import win32api

class Overlay:
    def __init__(self, root):
        # We act as a Toplevel of the passed root
        self.root = root
        self.window = None
        
        self.label = None
        self.fade_job = None
        
    def create_window(self):
        if self.window is not None and self.window.winfo_exists():
            return

        self.window = ctk.CTkToplevel(self.root)
        self.window.geometry("400x100+50+50") # Temporary position default
        self.window.overrideredirect(True) # No title bar
        self.window.attributes("-topmost", True)
        self.window.attributes("-transparentcolor", "black") # For simple transparency
        
        # Make background black (which becomes transparent)
        self.window.configure(fg_color="black")
        
        self.label = ctk.CTkLabel(
            self.window, 
            text="", 
            font=("Roboto", 30, "bold"),
            text_color="#00FF00",
            bg_color="black"
        )
        self.label.pack(expand=True, fill="both")
        
        # Position at bottom center
        w = 400
        h = 100
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w // 2) - (w // 2)
        y = screen_h - h - 100
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        
        # Click-through hack
        self.make_click_through()

    def make_click_through(self):
        # Allow window to exist but ensure all clicks pass through
        # Wait for window ID
        self.window.update() 
        hwnd = win32gui.GetParent(self.window.winfo_id())
        
        # Get current styles
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        
        # Add transparent (click-through) and layered styles
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

    def show_message(self, text, duration=1.5):
        # Must run on main thread
        try:
            self.root.after(0, lambda: self._update_message(text, duration))
        except:
            pass

    def _update_message(self, text, duration):
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        
        self.window.deiconify()
        self.label.configure(text=text)
        
        # Cancel previous fade if any
        if self.fade_job:
            self.root.after_cancel(self.fade_job)
            
        self.fade_job = self.root.after(int(duration * 1000), self._hide)

    def _hide(self):
        if self.window and self.window.winfo_exists():
            self.window.withdraw()
