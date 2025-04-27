import os
import sys
import tkinter as tk
from auto_clicker import AutoClicker
from gui import AutoClickerGUI

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the config file
    config_path = os.path.join(script_dir, "config.json")
    
    # Create the auto clicker instance
    auto_clicker = AutoClicker(config_path)
    
    # Create the GUI
    root = tk.Tk()
    app = AutoClickerGUI(root, auto_clicker)
    
    # Start the main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application terminated by user.")
    finally:
        # Clean up resources
        auto_clicker.cleanup()

if __name__ == "__main__":
    main()
