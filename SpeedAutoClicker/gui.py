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
        
        # CPS display
        cps_frame = ttk.Frame(frame)
        cps_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(cps_frame, text="Clicks Per Second (CPS):").pack(side=tk.LEFT)
        
        self.cps_var = tk.StringVar()
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
                self.cps_var.set("Invalid")
        
        self.interval_var.trace_add("write", update_cps)
        update_cps()  # Initial update
    
    def _create_duty_cycle_section(self):
        """Create the duty cycle section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Click Duty Cycle", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Duty cycle input
        duty_frame = ttk.Frame(frame)
        duty_frame.pack(fill=tk.X)
        
        ttk.Label(duty_frame, text="Duty Cycle (%):").pack(side=tk.LEFT)
        
        self.duty_var = tk.StringVar(value=str(self.config["duty_cycle_percent"]))
        duty_entry = ttk.Entry(duty_frame, textvariable=self.duty_var, width=10)
        duty_entry.pack(side=tk.LEFT, padx=5)
        
        # Explanation
        explanation = ttk.Label(
            frame, 
            text="Duty cycle controls how long the mouse button is held down.\n"
                 "50% means equal press and release time.",
            wraplength=450
        )
        explanation.pack(pady=(5, 0))
        
        # Update duty cycle when value changes
        def update_duty(*args):
            try:
                duty = float(self.duty_var.get())
                if 0 <= duty <= 100:
                    self.auto_clicker.update_config("duty_cycle_percent", duty)
            except ValueError:
                pass
        
        self.duty_var.trace_add("write", update_duty)
    
    def _create_mouse_button_section(self):
        """Create the mouse button selection section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Mouse Button", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Mouse button selection
        self.mouse_button_var = tk.StringVar(value=self.config["mouse_button"])
        
        left_radio = ttk.Radiobutton(
            frame, 
            text="Left Click", 
            value="left", 
            variable=self.mouse_button_var
        )
        left_radio.pack(anchor=tk.W)
        
        right_radio = ttk.Radiobutton(
            frame, 
            text="Right Click", 
            value="right", 
            variable=self.mouse_button_var
        )
        right_radio.pack(anchor=tk.W)
        
        middle_radio = ttk.Radiobutton(
            frame, 
            text="Middle Click", 
            value="middle", 
            variable=self.mouse_button_var
        )
        middle_radio.pack(anchor=tk.W)
        
        # Update config when selection changes
        def update_mouse_button(*args):
            self.auto_clicker.update_config("mouse_button", self.mouse_button_var.get())
        
        self.mouse_button_var.trace_add("write", update_mouse_button)
    
    def _create_hotkey_section(self):
        """Create the hotkey configuration section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Hotkey Configuration", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Hotkey input
        hotkey_frame = ttk.Frame(frame)
        hotkey_frame.pack(fill=tk.X)
        
        ttk.Label(hotkey_frame, text="Hotkey:").pack(side=tk.LEFT)
        
        self.hotkey_var = tk.StringVar(value=self.config["hotkey"])
        hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=10)
        hotkey_entry.pack(side=tk.LEFT, padx=5)
        
        # Activation mode
        mode_frame = ttk.Frame(frame)
        mode_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(mode_frame, text="Activation Mode:").pack(side=tk.LEFT)
        
        self.activation_mode_var = tk.StringVar(value=self.config["activation_mode"])
        
        toggle_radio = ttk.Radiobutton(
            mode_frame, 
            text="Toggle", 
            value="toggle", 
            variable=self.activation_mode_var
        )
        toggle_radio.pack(side=tk.LEFT, padx=(5, 10))
        
        hold_radio = ttk.Radiobutton(
            mode_frame, 
            text="Hold", 
            value="hold", 
            variable=self.activation_mode_var
        )
        hold_radio.pack(side=tk.LEFT)
        
        # Update config when values change
        def update_hotkey(*args):
            self.auto_clicker.update_config("hotkey", self.hotkey_var.get())
        
        def update_activation_mode(*args):
            self.auto_clicker.update_config("activation_mode", self.activation_mode_var.get())
        
        self.hotkey_var.trace_add("write", update_hotkey)
        self.activation_mode_var.trace_add("write", update_activation_mode)
    
    def _create_click_limit_section(self):
        """Create the click limit section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Click Limit", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Enable/disable click limit
        limit_enable_frame = ttk.Frame(frame)
        limit_enable_frame.pack(fill=tk.X)
        
        self.limit_enabled_var = tk.BooleanVar(value=self.config["click_limit"]["enabled"])
        limit_check = ttk.Checkbutton(
            limit_enable_frame, 
            text="Enable Click Limit", 
            variable=self.limit_enabled_var
        )
        limit_check.pack(side=tk.LEFT)
        
        # Click count input
        count_frame = ttk.Frame(frame)
        count_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(count_frame, text="Number of Clicks:").pack(side=tk.LEFT)
        
        self.click_count_var = tk.StringVar(value=str(self.config["click_limit"]["count"]))
        count_entry = ttk.Entry(count_frame, textvariable=self.click_count_var, width=10)
        count_entry.pack(side=tk.LEFT, padx=5)
        
        # Update config when values change
        def update_limit_enabled(*args):
            self.auto_clicker.update_config("click_limit.enabled", self.limit_enabled_var.get())
        
        def update_click_count(*args):
            try:
                count = int(self.click_count_var.get())
                if count > 0:
                    self.auto_clicker.update_config("click_limit.count", count)
            except ValueError:
                pass
        
        self.limit_enabled_var.trace_add("write", update_limit_enabled)
        self.click_count_var.trace_add("write", update_click_count)
    
    def _create_status_section(self):
        """Create the status section of the GUI"""
        frame = ttk.LabelFrame(self.main_frame, text="Status", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Status indicator
        status_frame = ttk.Frame(frame)
        status_frame.pack(fill=tk.X)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar(value="Inactive")
        self.status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            foreground="red"
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Click counter
        counter_frame = ttk.Frame(frame)
        counter_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(counter_frame, text="Clicks:").pack(side=tk.LEFT)
        
        self.click_counter_var = tk.StringVar(value="0")
        click_counter_label = ttk.Label(counter_frame, textvariable=self.click_counter_var)
        click_counter_label.pack(side=tk.LEFT, padx=5)
        
        # Manual control buttons
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
        """Create the Discord section of the GUI"""
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(20, 0))
        
        # Discord message
        message_label = ttk.Label(
            frame, 
            text="DM 5qvx for bugs and issues :D",
            font=("Helvetica", 10)
        )
        message_label.pack(pady=(0, 10))
        
        # Discord button
        discord_button = ttk.Button(
            frame, 
            text="Join my Discord", 
            command=self._open_discord
        )
        discord_button.pack()
    
    def _open_discord(self):
        """Open the Discord invite link"""
        webbrowser.open("https://discord.gg/MxGV8fGzpR")
    
    def _start_clicking(self):
        """Start the auto clicker from the GUI"""
        if self.auto_clicker.start_clicking():
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
    
    def _stop_clicking(self):
        """Stop the auto clicker from the GUI"""
        if self.auto_clicker.stop_clicking():
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
