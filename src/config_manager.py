import json
import os

import sys

class ConfigManager:
    def __init__(self, config_file="config.json"):
        # Resolve config path relative to the executable if frozen, or source if script
        if getattr(sys, 'frozen', False):
            # If run as exe, look in the same folder as the exe
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            # src/config_manager.py -> base_path is .../src
            # We want .../config.json which is one level up
            base_path = os.path.dirname(base_path)
            
        self.config_path = os.path.join(base_path, config_file)
        print(f"Loading config from: {self.config_path}")
        self.config = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {"default": self._get_defaults()}
            
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                
            # Migration check: if the config is flat (old style), wrap it in "default"
            # We assume if "default" key is missing and it has gesture keys, it's old.
            if "default" not in data and "TWO_FINGERS" in data:
                print("Migrating config to profile format...")
                new_data = {"default": data}
                self._save_config_file(new_data)
                return new_data
                
            return data
        except json.JSONDecodeError:
            print("Error decoding config.json, using defaults.")
            return {"default": self._get_defaults()}

    def _get_defaults(self):
         return {
            "TWO_FINGERS": ["alt", "right"],
            "THREE_FINGERS": ["alt", "left"],
            "FOUR_FINGERS": ["win", "d"]
        }

    def _save_config_file(self, data):
        try:
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to save migrated config: {e}")

    def get_shortcuts(self, app_name="default"):
        return self.config.get(app_name, self.config.get("default", {}))

    def get_mapping(self, gesture_name, app_name="default"):
        # Try specific app profile first (exact match)
        app_config = self.config.get(app_name)
        
        # Try without .exe extension (e.g. "chrome" matches "chrome.exe")
        if not app_config and app_name.endswith(".exe"):
            short_name = app_name[:-4] # Remove .exe
            app_config = self.config.get(short_name)

        if app_config and gesture_name in app_config:
            return app_config[gesture_name]
            
        # Fallback to default
        default_config = self.config.get("default", {})
        return default_config.get(gesture_name)

    def save_profile(self, app_name, profile_data):
        self.config[app_name] = profile_data
        self._save_config_file(self.config)

