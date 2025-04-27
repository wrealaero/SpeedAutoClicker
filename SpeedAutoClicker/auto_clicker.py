import time
import threading
import json
import os
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener

class AutoClicker:
    def __init__(self, config_path):
        self.mouse = MouseController()
        self.config_path = config_path
        self.load_config()
        
        self.running = False
        self.click_thread = None
        self.click_count = 0
        self.stop_event = threading.Event()
        
        # Button mapping
        self.button_map = {
            "left": Button.left,
            "right": Button.right,
            "middle": Button.middle
        }
        
        # Setup keyboard listener
        self.keyboard_listener = None
        self.setup_keyboard_listener()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                # Default configuration
                self.config = {
                    "click_interval_ms": 100.0,
                    "duty_cycle_percent": 50.0,
                    "mouse_button": "left",
                    "activation_mode": "toggle",
                    "hotkey": "f6",
                    "click_limit": {
                        "enabled": False,
                        "count": 1000
                    },
                    "last_position": {
                        "x": 0,
                        "y": 0
                    }
                }
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            # Set default values if loading fails
            self.config = {
                "click_interval_ms": 100.0,
                "duty_cycle_percent": 50.0,
                "mouse_button": "left",
                "activation_mode": "toggle",
                "hotkey": "f6",
                "click_limit": {
                    "enabled": False,
                    "count": 1000
                },
                "last_position": {
                    "x": 0,
                    "y": 0
                }
            }
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def update_config(self, key, value):
        """Update a specific configuration value"""
        if key in self.config:
            self.config[key] = value
            self.save_config()
        elif "." in key:
            # Handle nested config values like "click_limit.enabled"
            parts = key.split(".")
            if len(parts) == 2 and parts[0] in self.config and isinstance(self.config[parts[0]], dict):
                self.config[parts[0]][parts[1]] = value
                self.save_config()
    
    def setup_keyboard_listener(self):
        """Setup keyboard listener for hotkey detection"""
        def on_press(key):
            try:
                # Convert key to string for comparison
                if hasattr(key, 'char'):
                    key_str = key.char.lower() if key.char else None
                elif isinstance(key, Key):
                    key_str = key.name.lower()
                else:
                    key_str = key.name.lower() if hasattr(key, 'name') else str(key).lower()
                
                # Check if the pressed key matches the hotkey
                if key_str == self.config["hotkey"].lower():
                    if self.config["activation_mode"] == "toggle":
                        self.toggle_clicking()
                    elif self.config["activation_mode"] == "hold" and not self.running:
                        self.start_clicking()
            except AttributeError:
                # Special keys might not have char attribute
                pass
        
        def on_release(key):
            try:
                # Convert key to string for comparison
                if hasattr(key, 'char'):
                    key_str = key.char.lower() if key.char else None
                elif isinstance(key, Key):
                    key_str = key.name.lower()
                else:
                    key_str = key.name.lower() if hasattr(key, 'name') else str(key).lower()
                
                # For hold mode, stop clicking when hotkey is released
                if key_str == self.config["hotkey"].lower() and self.config["activation_mode"] == "hold" and self.running:
                    self.stop_clicking()
            except AttributeError:
                pass
        
        # Start the keyboard listener
        self.keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.start()
    
    def toggle_clicking(self):
        """Toggle the auto clicker on/off"""
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        """Start the auto clicking process"""
        if not self.running:
            self.running = True
            self.click_count = 0
            self.stop_event.clear()
            self.click_thread = threading.Thread(target=self._click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
            return True
        return False
    
    def stop_clicking(self):
        """Stop the auto clicking process"""
        if self.running:
            self.running = False
            self.stop_event.set()
            if self.click_thread:
                self.click_thread.join(timeout=1.0)
            return True
        return False
    
    def _click_loop(self):
        """Main clicking loop with high-precision timing"""
        button = self.button_map.get(self.config["mouse_button"], Button.left)
        interval_sec = self.config["click_interval_ms"] / 1000.0
        duty_cycle = self.config["duty_cycle_percent"] / 100.0
        
        # Calculate press and release durations
        press_duration = interval_sec * duty_cycle
        release_duration = interval_sec * (1 - duty_cycle)
        
        limit_enabled = self.config["click_limit"]["enabled"]
        limit_count = self.config["click_limit"]["count"]
        
        while self.running and not self.stop_event.is_set():
            # Perform mouse click
            click_start_time = time.perf_counter()
            
            # Press mouse button
            self.mouse.press(button)
            
            # Wait for press duration with high precision
            press_end_target = click_start_time + press_duration
            while time.perf_counter() < press_end_target and not self.stop_event.is_set():
                pass
            
            # Release mouse button
            self.mouse.release(button)
            
            # Increment click counter
            self.click_count += 1
            
            # Check if we've reached the click limit
            if limit_enabled and self.click_count >= limit_count:
                self.running = False
                break
            
            # Wait for release duration with high precision
            release_end_target = click_start_time + interval_sec
            while time.perf_counter() < release_end_target and not self.stop_event.is_set():
                pass
    
    def get_status(self):
        """Get the current status of the auto clicker"""
        return {
            "running": self.running,
            "click_count": self.click_count,
            "config": self.config
        }
    
    def cleanup(self):
        """Clean up resources before exiting"""
        self.stop_clicking()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
# This file is intentionally left empty to make the directory a Python package
