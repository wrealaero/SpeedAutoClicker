import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os
import json
from PIL import Image, ImageTk
import threading
import time

class AutoClickerGUI:
    def __init__(self, root, auto_clicker):
        self.root = root
        self.auto_clicker = auto_clicker
        self.config = auto_clicker.config
        
        # Set window properties
        self.root.title("SpeedAutoClicker for macOS")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self._create_title_section()
        self._create_click_rate_section()
        self._create_duty_cycle_section()
        self._create_mouse_button_section()
        self._create_hotkey_section()
        self._create_click_limit_section()
        self._create_status_section()
        self._create_discord_section()
        
        # Status update thread
        self.status_thread = threading.Thread(target=self._update_status_loop, daemon=True)
        self.status_thread.start()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_title_section(self):
        """Create the title section of the GUI"""
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="SpeedAutoClicker",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Advanced Auto Clicker for macOS",
            font=("Helvetica", 12)
        )
        subtitle_label.pack()
    
    def _create_click_rate_section(self):
        """Create the click rate section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Click Rate", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Interval input
        interval_frame = ttk.Frame(frame)
        interval_frame.pack(fill=tk.X)
        
        ttk.Label(interval_frame, text="Interval (ms):").pack(side=tk.LEFT)
        
        self.interval_var = tk.StringVar(value=str(self.config["click_interval_ms"]))
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=10)
        interval_entry.pack(side=tk.LEFT, padx=5)
        
        cps_frame = ttk.Frame(frame)
        cps_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(cps_frame, text="Clicks Per Second:").pack(side=tk.LEFT)
        
        self.cps_var = tk.StringVar(value=str(1000 / self.config["click_interval_ms"]))
        cps_label = ttk.Label(cps_frame, textvariable=self.cps_var)
        cps_label.pack(side=tk.LEFT, padx=5)
        
        # Update CPS when interval changes
        def update_cps(*args):
            try:
                interval = float(self.interval_var.get())
                if interval > 0:
                    cps = 1000 / interval
                    self.cps_var.set(f"{cps:.2f}")
                    self.auto_clicker.update_config("click_interval_ms", interval)
            except ValueError:
                pass
        
        self.interval_var.trace_add("write", update_cps)
    
    def _create_duty_cycle_section(self):
        """Create the duty cycle section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Duty Cycle", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Explanation label
        explanation = ttk.Label(
            frame,
            text="Duty cycle controls how long the mouse button is held down\nduring each click cycle.",
            justify=tk.LEFT
        )
        explanation.pack(fill=tk.X, pady=(0, 5))
        
        # Duty cycle slider
        duty_frame = ttk.Frame(frame)
        duty_frame.pack(fill=tk.X)
        
        ttk.Label(duty_frame, text="Duty Cycle (%):").pack(side=tk.LEFT)
        
        self.duty_var = tk.StringVar(value=str(self.config["duty_cycle_percent"]))
        duty_entry = ttk.Entry(duty_frame, textvariable=self.duty_var, width=10)
        duty_entry.pack(side=tk.LEFT, padx=5)
        
        # Slider
        self.duty_slider = ttk.Scale(
            frame,
            from_=1,
            to=99,
            orient=tk.HORIZONTAL,
            value=self.config["duty_cycle_percent"]
        )
        self.duty_slider.pack(fill=tk.X, pady=(5, 0))
        
        # Connect slider and entry
        def update_duty_from_slider(*args):
            value = self.duty_slider.get()
            self.duty_var.set(f"{value:.2f}")
            self.auto_clicker.update_config("duty_cycle_percent", value)
        
        def update_slider_from_duty(*args):
            try:
                value = float(self.duty_var.get())
                if 1 <= value <= 99:
                    self.duty_slider.set(value)
                    self.auto_clicker.update_config("duty_cycle_percent", value)
            except ValueError:
                pass
        
        self.duty_slider.configure(command=lambda x: update_duty_from_slider())
        self.duty_var.trace_add("write", update_slider_from_duty)
    
    def _create_mouse_button_section(self):
        """Create the mouse button selection section"""
        frame = ttk.LabelFrame(self.main_frame, text="Mouse Button", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Radio buttons for mouse button selection
        self.button_var = tk.StringVar(value=self.config["mouse_button"])
        
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X)
        
        for button_text, button_value in [("Left", "left"), ("Right", "right"), ("Middle", "middle")]:
            radio = ttk.Radiobutton(
                buttons_frame,
                text=button_text,
                value=button_value,
                variable=self.button_var
            )
            radio.pack(side=tk.LEFT, padx=10)
        
        # Update config when button changes
        def update_button(*args):
            self.auto_clicker.update_config("mouse_button", self.button_var.get())
        
        self.button_var.trace_add("write", update_button)
    
    def _create_hotkey_section(self):
        """Create the hotkey configuration section"""
        frame = ttk.LabelFrame(self.main_frame, text="Hotkey Configuration", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Hotkey input
        hotkey_frame = ttk.Frame(frame)
        hotkey_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(hotkey_frame, text="Activation Key:").pack(side=tk.LEFT)
        
        self.hotkey_var = tk.StringVar(value=self.config["hotkey"])
        self.hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=10)
        self.hotkey_entry.pack(side=tk.LEFT, padx=5)
        
        # Hotkey recording button
        self.record_button = ttk.Button(
            hotkey_frame,
            text="Record Key",
            command=self._record_hotkey
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Activation mode
        mode_frame = ttk.Frame(frame)
        mode_frame.pack(fill=tk.X)
        
        ttk.Label(mode_frame, text="Activation Mode:").pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value=self.config["activation_mode"])
        
        for mode_text, mode_value in [("Toggle", "toggle"), ("Hold", "hold")]:
            radio = ttk.Radiobutton(
                mode_frame,
                text=mode_text,
                value=mode_value,
                variable=self.mode_var
            )
            radio.pack(side=tk.LEFT, padx=10)
        
        # Update config when mode changes
        def update_mode(*args):
            self.auto_clicker.update_config("activation_mode", self.mode_var.get())
        
        self.mode_var.trace_add("write", update_mode)
        
        # Update config when hotkey changes
        def update_hotkey(*args):
            self.auto_clicker.update_config("hotkey", self.hotkey_var.get())
        
        self.hotkey_var.trace_add("write", update_hotkey)
    
    def _record_hotkey(self):
        """Record a new hotkey"""
        # Disable the button while recording
        self.record_button.configure(text="Press a key...", state=tk.DISABLED)
        self.root.update()
        
        # Create a temporary window to capture the key
        capture_window = tk.Toplevel(self.root)
        capture_window.title("Press a Key")
        capture_window.geometry("300x100")
        capture_window.resizable(False, False)
        
        label = ttk.Label(
            capture_window,
            text="Press any key to set as the hotkey...",
            font=("Helvetica", 12)
        )
        label.pack(pady=20)
        
        def on_key(event):
            key_name = event.keysym.lower()
            self.hotkey_var.set(key_name)
            self.auto_clicker.update_config("hotkey", key_name)
            capture_window.destroy()
            self.record_button.configure(text="Record Key", state=tk.NORMAL)
        
        capture_window.bind("<Key>", on_key)
        capture_window.focus_force()
    
    def _create_click_limit_section(self):
        """Create the click limit section"""
        frame = ttk.LabelFrame(self.main_frame, text="Click Limit", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Enable/disable click limit
        limit_enable_frame = ttk.Frame(frame)
        limit_enable_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.limit_enabled_var = tk.BooleanVar(value=self.config["click_limit"]["enabled"])
        limit_check = ttk.Checkbutton(
            limit_enable_frame,
            text="Enable Click Limit",
            variable=self.limit_enabled_var
        )
        limit_check.pack(side=tk.LEFT)
        
        # Click count input
        limit_count_frame = ttk.Frame(frame)
        limit_count_frame.pack(fill=tk.X)
        
        ttk.Label(limit_count_frame, text="Number of Clicks:").pack(side=tk.LEFT)
        
        self.limit_count_var = tk.StringVar(value=str(self.config["click_limit"]["count"]))
        limit_entry = ttk.Entry(limit_count_frame, textvariable=self.limit_count_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=5)
        
        # Update config when limit settings change
        def update_limit_enabled(*args):
            self.auto_clicker.update_config("click_limit.enabled", self.limit_enabled_var.get())
        
        def update_limit_count(*args):
            try:
                count = int(self.limit_count_var.get())
                if count > 0:
                    self.auto_clicker.update_config("click_limit.count", count)
            except ValueError:
                pass
        
        self.limit_enabled_var.trace_add("write", update_limit_enabled)
        self.limit_count_var.trace_add("write", update_limit_count)
    
    def _create_status_section(self):
        """Create the status section"""
        frame = ttk.LabelFrame(self.main_frame, text="Status", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Status indicator
        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(status_frame, text="Auto Clicker Status:").pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Inactive")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            foreground="red",
            font=("Helvetica", 10, "bold")
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Click counter
        counter_frame = ttk.Frame(frame)
        counter_frame.pack(fill=tk.X)
        
        ttk.Label(counter_frame, text="Clicks Performed:").pack(side=tk.LEFT)
        
        self.click_counter_var = tk.StringVar(value="0")
        ttk.Label(counter_frame, textvariable=self.click_counter_var).pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start Clicking",
            command=self._start_clicking
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Clicking",
            command=self._stop_clicking,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT)
    
    def _create_discord_section(self):
        """Create the Discord section"""
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=10)
        
        # Discord message
        message_label = ttk.Label(
            frame,
            text="DM 5qvx for bugs and issues :D",
            font=("Helvetica", 10)
        )
        message_label.pack(pady=(0, 5))
        
        # Discord button
        discord_button = ttk.Button(
            frame,
            text="Join my Discord",
            command=lambda: webbrowser.open("https://discord.gg/MxGV8fGzpR")
        )
        discord_button.pack()
    
    def _start_clicking(self):
        """Start the auto clicker"""
        if self.auto_clicker.start_clicking():
            self.status_var.set("Active")
            self.status_label.config(foreground="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
    
    def _stop_clicking(self):
        """Stop the auto clicker"""
        if self.auto_clicker.stop_clicking():
            self.status_var.set("Inactive")
            self.status_label.config(foreground="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _update_status_loop(self):
        """Update the status display periodically"""
        while True:
            status = self.auto_clicker.get_status()
            
            # Update status text and color
            if status["running"]:
                self.status_var.set("Active")
                self.status_label.config(foreground="green")
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
            else:
                self.status_var.set("Inactive")
                self.status_label.config(foreground="red")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
            
            # Update click counter
            self.click_counter_var.set(str(status["click_count"]))
            
            # Sleep for a short time before updating again
            time.sleep(0.1)
    
    def _on_close(self):
        """Handle window close event"""
        # Stop the auto clicker if it's running
        self.auto_clicker.cleanup()
        
        # Destroy the window
        self.root.destroy()

