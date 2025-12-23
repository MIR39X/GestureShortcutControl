import customtkinter as ctk
import json
import threading
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SettingsGUI(ctk.CTk):
    def __init__(self, config_manager, run_callback):
        super().__init__()
        self.config_manager = config_manager
        self.run_callback = run_callback
        self.is_running = True
        
        # State
        self.current_profile = "default"

        self.title("LazyHands Config")
        self.geometry("450x650") # Added width for profile controls
        self.resizable(False, False)

        # Title
        self.label = ctk.CTkLabel(self, text="LazyHands Settings", font=("Roboto", 24, "bold"))
        self.label.pack(pady=10)

        # --- Profile Section ---
        self.profile_frame = ctk.CTkFrame(self)
        self.profile_frame.pack(fill="x", padx=20, pady=5)
        
        self.profile_label = ctk.CTkLabel(self.profile_frame, text="Profile:")
        self.profile_label.pack(side="left", padx=10)
        
        target_profiles = list(self.config_manager.config.keys())
        if "default" not in target_profiles: target_profiles.insert(0, "default")
        
        self.profile_combo = ctk.CTkComboBox(
            self.profile_frame, 
            values=target_profiles,
            command=self.change_profile
        )
        self.profile_combo.set("default")
        self.profile_combo.pack(side="left", padx=10, fill="x", expand=True)

        self.add_profile_btn = ctk.CTkButton(
            self.profile_frame, 
            text="+", 
            width=30, 
            command=self.add_profile
        )
        self.add_profile_btn.pack(side="right", padx=10)
        # -----------------------

        # Scrollable Frame for Gestures
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=400)
        self.scroll_frame.pack(pady=10)

        self.entries = {}
        
        self.known_gestures = [
            "TWO_FINGERS", "THREE_FINGERS", "FOUR_FINGERS", 
            "OPEN_PALM", "FIST", "THUMB", "ROCK",
            "SWIPE_LEFT", "SWIPE_RIGHT", "SWIPE_UP", "SWIPE_DOWN"
        ]
        
        self.gesture_display_names = {
            "TWO_FINGERS": "Two Fingers",
            "THREE_FINGERS": "Three Fingers",
            "FOUR_FINGERS": "Four Fingers",
            "OPEN_PALM": "Open Palm",
            "FIST": "Fist",
            "THUMB": "Thumb",
            "ROCK": "Rock (Mouse Toggle)",
            "SWIPE_LEFT": "Swipe Left",
            "SWIPE_RIGHT": "Swipe Right",
            "SWIPE_UP": "Swipe Up",
            "SWIPE_DOWN": "Swipe Down"
        }
        
        # Initialize Rows
        for gesture in self.known_gestures:
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=5, padx=5)
            
            display_name = self.gesture_display_names.get(gesture, gesture)
            lbl = ctk.CTkLabel(row, text=display_name, width=150, anchor="w") # Increased width for longer names
            lbl.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(row, placeholder_text="e.g. alt, right")
            entry.pack(side="right", expand=True, fill="x", padx=5)
            
            self.entries[gesture] = entry

        # Load Initial Data
        self.load_gestures("default")

        # Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.save_btn = ctk.CTkButton(
            self.btn_frame, 
            text="Save Config", 
            command=self.save_config, 
            fg_color="#2CC985", 
            hover_color="#229A66"
        )
        self.save_btn.pack(side="left", padx=10)
        
        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Status: Running", text_color="#2CC985")
        self.status_label.pack(side="bottom", pady=10)

        # Handle Close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def change_profile(self, new_profile):
        self.current_profile = new_profile
        self.load_gestures(new_profile)

    def load_gestures(self, profile_name):
        data = self.config_manager.get_shortcuts(profile_name)
        
        for gesture, entry in self.entries.items():
            entry.delete(0, "end")
            keys = data.get(gesture, [])
            if keys:
                entry.insert(0, ", ".join(keys))

    def add_profile(self):
        dialog = ctk.CTkInputDialog(text="Enter App Executable Name (e.g. spotify.exe):", title="New Profile")
        new_name = dialog.get_input()
        if new_name:
            new_name = new_name.strip().lower()
            if new_name not in self.profile_combo.cget("values"):
                # Update combo values
                current_values = self.profile_combo.cget("values")
                current_values.append(new_name)
                self.profile_combo.configure(values=current_values)
                
                # Switch to it
                self.profile_combo.set(new_name)
                self.change_profile(new_name)
                
                # Create empty entry in config manager implicitly on save, 
                # or we can explicitly init it.
                self.config_manager.config[new_name] = {} 

    def save_config(self):
        new_config = {}
        for gesture, entry in self.entries.items():
            text = entry.get().strip()
            if text:
                keys = [k.strip() for k in text.split(",") if k.strip()]
                new_config[gesture] = keys
        
        try:
            # Save to current profile
            self.config_manager.save_profile(self.current_profile, new_config)
            messagebox.showinfo("Success", f"Configuration saved for '{self.current_profile}'!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def on_close(self):
        self.withdraw()

    def show(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def quit_app(self):
        self.is_running = False
        self.destroy()
