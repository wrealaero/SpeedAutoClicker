# SpeedAutoClicker for macOS

An advanced, high-performance auto clicker for macOS with precision timing and extensive customization options.

![SpeedAutoClicker Screenshot](screenshot.png)

## Features

- **Ultra-Fast Clicking**: Capable of hundreds of clicks per second with high precision timing
- **Adjustable Click Rate**: Set the exact interval between clicks in milliseconds (supports decimal values)
- **Duty Cycle Control**: Precisely control how long the mouse button is held down during each click cycle
- **Multiple Mouse Buttons**: Support for left, right, and middle mouse buttons
- **Customizable Hotkeys**: Bind any key to activate/deactivate the auto clicker
- **Activation Modes**:
  - Toggle Mode: Press once to start, press again to stop
  - Hold Mode: Only clicks while the hotkey is being held down
- **Click Limit System**: Set a specific number of clicks or run indefinitely
- **Visual Status Indicator**: Clearly shows when the auto clicker is active or inactive

## System Requirements

- macOS 10.14 or later (Optimized for macOS Monterey 12.7.6)
- Python 3.6 or later

## Installation

### Option 1: Quick Install

1. Clone this repository:
   ```bash
   git clone https://github.com/wrealaero/SpeedAutoClicker.git
   cd SpeedAutoClicker
   ```

2. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. Launch the application:
   ```bash
   python3 SpeedAutoClicker/main.py
   ```

### Option 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/wrealaero/SpeedAutoClicker.git
   cd SpeedAutoClicker
   ```

2. Install the required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   python3 SpeedAutoClicker/main.py
   ```

## Usage Guide

### Setting Click Rate

1. Enter the desired interval in milliseconds in the "Interval (ms)" field
2. The corresponding Clicks Per Second (CPS) will be calculated automatically

### Configuring Duty Cycle

The duty cycle controls how long the mouse button is held down during each click cycle:
- 50% duty cycle: Equal time for press and release
- Higher values: Longer press duration
- Lower values: Shorter press duration

Adjust using the slider or enter a precise percentage value.

### Selecting Mouse Button

Choose which mouse button to simulate:
- Left Click (default)
- Right Click
- Middle Click

### Setting Up Hotkeys

1. Click "Record Key" to set your activation hotkey
2. Press any key when prompted
3. Choose the activation mode:
   - Toggle: Press once to start, press again to stop
   - Hold: Only clicks while the key is held down

### Using Click Limits

1. Check "Enable Click Limit" to set a maximum number of clicks
2. Enter the desired number of clicks
3. The auto clicker will stop automatically after reaching this limit

### Starting and Stopping

- Click the "Start Clicking" button or press your hotkey to begin
- Click the "Stop Clicking" button or press your hotkey again to stop

## Troubleshooting

### Common Issues

- **Permissions**: If clicking doesn't work, make sure your application has accessibility permissions in System Preferences > Security & Privacy > Privacy > Accessibility
- **Performance**: If experiencing lag, try increasing the click interval slightly
- **Hotkey Not Working**: Some keys may be reserved by the system. Try a different key.

### Getting Help

If you encounter any bugs or issues, please:
1. Check the [GitHub Issues](https://github.com/wrealaero/SpeedAutoClicker/issues) page
2. Join our Discord server using the "Join my Discord" button in the app
3. DM 5qvx for direct support

## Development

### Project Structure

- `SpeedAutoClicker/main.py`: Application entry point
- `SpeedAutoClicker/gui.py`: User interface implementation
- `SpeedAutoClicker/auto_clicker.py`: Core clicking functionality
- `SpeedAutoClicker/config.json`: User settings storage

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by SpeedAutoClicker for Windows
- Thanks to all contributors and testers
