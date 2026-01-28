# 8BitDo Firmware Updater

A Python tool to automatically download and flash firmware updates for 8BitDo gamepads on Linux, without requiring the official Upgrade Tool.

## Why This Tool?

8BitDo provides an official Upgrade Tool for updating their gamepads, but it's only available for Windows and macOS. This tool allows Linux users to easily update their 8BitDo gamepad firmware using a simple command-line interface.

## Features

- 🎮 **Interactive menu** - Easy selection from all supported 8BitDo gamepads
- 📥 **Automatic firmware download** - Fetches the latest firmware directly from 8BitDo's servers
- 🔄 **Version selection** - Choose from multiple firmware versions, including beta releases
- 🔍 **Automatic device detection** - Finds your connected gamepad automatically
- ⚡ **One-command flashing** - Handles the entire update process
- 🧹 **Cleanup** - Optional removal of downloaded firmware files
- ✅ **User-friendly** - Clear instructions and confirmations at every step

## Supported Gamepads

- The list is being actively maintained to support all gamepads

## Requirements

### System Dependencies

- **Python 3.6+**
- **fwupd** - Firmware update daemon for Linux

Install fwupd on Ubuntu/Debian:
```bash
sudo apt install fwupd
```

Install fwupd on Fedora:
```bash
sudo dnf install fwupd
```

Install fwupd on Arch Linux:
```bash
sudo pacman -S fwupd
```

### Python Dependencies

```bash
pip3 install requests
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/franfermon/8bitdo_update.git
cd 8bitdo_update
```

2. Install Python dependencies:
```bash
pip3 install requests
```

3. Make the script executable:
```bash
chmod +x 8bitdo_updater.py
```

## Usage

### Basic Usage

Simply run the script:
```bash
./8bitdo_updater.py
```

Or with Python:
```bash
python3 8bitdo_updater.py
```

### Step-by-Step Process

1. **Select your gamepad** from the list
2. **Choose whether to include beta versions**
3. **Select the firmware version** you want to install
4. **Put your gamepad in bootloader mode**:
   - Hold down **L1 + R1 + START** for 3 seconds
   - The status LED should blink **RED**
   - Connect via USB cable
5. **Confirm the update** - the script will handle the rest!

### Optional: Install System-Wide

To run the updater from anywhere:
```bash
sudo cp 8bitdo_updater.py /usr/local/bin/8bitdo-updater
sudo chmod +x /usr/local/bin/8bitdo-updater
```

Then run with:
```bash
8bitdo-updater
```

## Example Session

```
============================================================
  8BitDo Firmware Updater
============================================================

Available gamepads:

   1. Arcade Stick
   2. Arcade Stick Receiver
   ...
  16. SN30 Pro+
  17. SN30 Pro

Enter the number of your gamepad: 17

Selected: SN30 Pro

Include beta versions? (y/n): n

Fetching firmware list for 9...

Available firmware versions:

  1. Version 1.36 - 2021-04-19 (87.0 KB)
  2. Version 1.33 - 2020-08-15 (86.5 KB)

Enter the number of the firmware to download (or 'q' to quit): 1

Downloading firmware: cab12b12-8e01-472f-a9f4-ec2237c598b9.dat...
✓ Firmware downloaded successfully: cab12b12-8e01-472f-a9f4-ec2237c598b9.dat

============================================================
  INSTRUCTIONS
============================================================

1. Put your gamepad in bootloader mode:
   - Hold down L1 + R1 + START for 3 seconds
   - A status LED should blink RED

2. Connect the gamepad to your computer via USB cable

3. Press Enter when ready...
============================================================

Searching for 8BitDo gamepad...

✓ Found: 8Bitdo SN30 Pro
  Current version: 2.04
  Device ID: 23ec719b6aabc2d2dac5176c232f0da7a21881b0

Proceed with firmware update? (y/n): y

Flashing firmware to gamepad...
This may take a minute. Please do not disconnect the gamepad.
You may be prompted for your sudo password...

✓ Firmware flashed successfully!

============================================================
  Update completed successfully!
============================================================
```

## Troubleshooting

### Gamepad Not Detected

- Make sure the gamepad is in **bootloader mode** (LED blinking red)
- Verify the USB cable is properly connected
- Try a different USB port or cable
- Check if fwupd detects the device: `fwupdmgr get-devices`

### Permission Errors

The script uses `sudo` for flashing firmware. If you encounter permission issues:
```bash
# Make sure your user is in the plugdev group
sudo usermod -a -G plugdev $USER
# Log out and back in for changes to take effect
```

### Firmware Flash Timeout

If the firmware flash times out:
1. Manually restart your gamepad by disconnecting and reconnecting it
2. Verify the update completed: `fwupdmgr get-devices`

### fwupd Not Found

Install fwupd for your distribution (see Requirements section above).
## Manual Update Process

If you prefer to update manually or troubleshoot issues, see the orgininal guide in https://ladis.cloud/blog/posts/firmware-update-8bitdo.html for detailed instructions.
## How It Works

This tool automates the process described in the original blog post:

    Queries 8BitDo's API to get available firmware versions
    Downloads the firmware file from 8BitDo's servers
    Uses fwupd to detect the connected gamepad in bootloader mode
    Flashes the firmware using fwupdtool

## Credits

    Based on the guide by ladis.cloud
    Uses fwupd for firmware flashing

## License

MIT License - feel free to use and modify as needed.
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is not officially affiliated with or endorsed by 8BitDo. Use at your own risk. Always ensure you're downloading the correct firmware for your specific gamepad model.
