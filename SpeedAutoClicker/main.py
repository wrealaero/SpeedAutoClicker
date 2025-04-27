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
    
    # Set application icon (if available)
    try:
        icon_path = os.path.join(script_dir, "icon.png")
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
    except Exception as e:
        print(f"Could not load icon: {e}")
    
    # Apply a more native macOS look
    try:
        root.tk.call('tk::mac::useTkAqua', 1)
    except:
        pass  # Not on macOS or Tk version doesn't support this
    
    # Create the GUI
    app = AutoClickerGUI(root, auto_clicker)
    
    # Set up exception handling for the GUI
    def handle_exception(exc_type, exc_value, exc_traceback):
        import traceback
        print("".join(traceback.format_exception(exc_type, exc_value, 
exc_traceback)))
        tk.messagebox.showerror(
            "Error",
            f"An unexpected error occurred:\n{exc_value}\n\nPlease report 
this to the developer."
        )
    
    # Set the exception handler
    sys.excepthook = handle_exception
    
    # Start the GUI main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application terminated by user")
    finally:
        # Clean up resources
        auto_clicker.cleanup()

if __name__ == "__main__":
    main()

