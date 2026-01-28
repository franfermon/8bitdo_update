#!/usr/bin/env python3
"""
8BitDo Firmware Updater
Automates the process of downloading and flashing firmware for 8BitDo gamepads on Linux
"""

import requests
import subprocess
import sys
import json
import os
from pathlib import Path

# Gamepad types mapping
GAMEPADS = {
    "1": {"name": "Arcade Stick", "type": 34},
    "2": {"name": "Arcade Stick 2.4g Receiver for Xbox", "type": 52},
    "3": {"name": "Arcade Stick for Xbox", "type": 51},
    "4": {"name": "Arcade Stick for Xbox", "type": 56},
    "5": {"name": "Cube 2", "type": 112},
    "6": {"name": "Cube 2 Adapter", "type": 113},
    "7": {"name": "Dogbone Modkit", "type": 26},
    "8": {"name": "GBros. Adapter", "type": 20},
    "9": {"name": "Hitbox", "type": 101},
    "10": {"name": "Hitbox Adapter", "type": 102},
    "11": {"name": "Hitbox for Xbox", "type": 90},
    "12": {"name": "Joy_V1.42", "type": 5},
    "13": {"name": "Lite 2", "type": 47},
    "14": {"name": "Lite SE", "type": 46},
    "15": {"name": "Lite SE for Xbox", "type": 68},
    "16": {"name": "Lite gamepad", "type": 28},
    "17": {"name": "M30", "type": 23},
    "18": {"name": "M30 Modkit", "type": 14},
    "19": {"name": "M30 Wired for Xbox", "type": 69},
    "20": {"name": "Micro", "type": 60},
    "21": {"name": "N30 ArcadeStick", "type": 4},
    "22": {"name": "N30 ArcadeStick_V5.0", "type": 4},
    "23": {"name": "N30 Modkit", "type": 15},
    "24": {"name": "N30 NS", "type": 18},
    "25": {"name": "N30 Pro 2", "type": 13},
    "26": {"name": "N30+F30", "type": 2},
    "27": {"name": "N30+F30_V4.1", "type": 2},
    "28": {"name": "N30_ArcadeStick_V4.1", "type": 4},
    "29": {"name": "N30pro+F30pro", "type": 1},
    "30": {"name": "N30pro+F30pro_V4.1", "type": 1},
    "31": {"name": "N64 Modkit", "type": 53},
    "32": {"name": "NGC Adapter", "type": 92},
    "33": {"name": "NGC Modkit", "type": 91},
    "34": {"name": "P30 Modkit", "type": 24},
    "35": {"name": "Pro 2", "type": 33},
    "36": {"name": "Pro 3", "type": 86},
    "37": {"name": "Pro 3 Adapter", "type": 87},
    "38": {"name": "Pro2 Wired", "type": 37},
    "39": {"name": "Pro2 Wired for Xbox", "type": 36},
    "40": {"name": "Pro2 Wired for Xbox", "type": 63},
    "41": {"name": "Retro 87 Keyboard X", "type": 80},
    "42": {"name": "Retro 87 Keyboard X Adapter", "type": 81},
    "43": {"name": "Retro 87 Keyboard X UK", "type": 106},
    "44": {"name": "Retro 87 Keyboard X UK Adapter", "type": 107},
    "45": {"name": "Retro Keyboard", "type": 61},
    "46": {"name": "Retro Keyboard 108", "type": 82},
    "47": {"name": "Retro Keyboard 108 Adapter", "type": 83},
    "48": {"name": "Retro Keyboard Receiver", "type": 62},
    "49": {"name": "Retro Keyboard UK", "type": 88},
    "50": {"name": "Retro Mouse", "type": 84},
    "51": {"name": "Retro Mouse Adapter", "type": 85},
    "52": {"name": "Retro Numpad", "type": 73},
    "53": {"name": "Retro Numpad Adapter", "type": 74},
    "54": {"name": "Retro Receiver for Classic", "type": 6},
    "55": {"name": "Retro Receiver for MD/Genesis", "type": 22},
    "56": {"name": "Retro Receiver for NES/SFC", "type": 7},
    "57": {"name": "Retro Receiver for PS", "type": 59},
    "58": {"name": "S30 Modkit", "type": 27},
    "59": {"name": "SN30 Modkit", "type": 16},
    "60": {"name": "SN30 Pro for Android", "type": 31},
    "61": {"name": "SN30 Pro+", "type": 25},
    "62": {"name": "SN30 V2", "type": 17},
    "63": {"name": "SN30+SF30", "type": 3},
    "64": {"name": "SN30+SF30_V4.1", "type": 3},
    "65": {"name": "SN30pro+SF30pro", "type": 9},
    "66": {"name": "Saturn Adapter", "type": 99},
    "67": {"name": "USB Adapter", "type": 8},
    "68": {"name": "USB Adapter 2", "type": 39},
    "69": {"name": "USB Adapter for PS classic", "type": 21},
    "70": {"name": "USB Apdater", "type": 8},
    "71": {"name": "Ultimate", "type": 41},
    "72": {"name": "Ultimate 2", "type": 97},
    "73": {"name": "Ultimate 2", "type": 108},
    "74": {"name": "Ultimate 2 Adapter", "type": 98},
    "75": {"name": "Ultimate 2 wireless", "type": 94},
    "76": {"name": "Ultimate 2 wireless Adapter", "type": 95},
    "77": {"name": "Ultimate 2.4g", "type": 43},
    "78": {"name": "Ultimate 2.4g Adapter", "type": 44},
    "79": {"name": "Ultimate 2C", "type": 75},
    "80": {"name": "Ultimate 2C Adapter", "type": 76},
    "81": {"name": "Ultimate 2C Wired", "type": 77},
    "82": {"name": "Ultimate 3M Receiver", "type": 65},
    "83": {"name": "Ultimate 3M for Rare", "type": 104},
    "84": {"name": "Ultimate Adapter", "type": 42},
    "85": {"name": "Ultimate C 2.4g", "type": 48},
    "86": {"name": "Ultimate C 2.4g Adapter", "type": 49},
    "87": {"name": "Ultimate C Bluetooth", "type": 66},
    "88": {"name": "Ultimate C N64 2.4g", "type": 71},
    "89": {"name": "Ultimate C N64 2.4g Adapter", "type": 72},
    "90": {"name": "Ultimate C Wired", "type": 50},
    "91": {"name": "Ultimate C Wired for Xbox", "type": 70},
    "92": {"name": "Ultimate MG", "type": 100},
    "93": {"name": "Ultimate MGX", "type": 79},
    "94": {"name": "Ultimate Mini Wired for Xbox", "type": 93},
    "95": {"name": "Ultimate N64", "type": 78},
    "96": {"name": "Ultimate Wired", "type": 45},
    "97": {"name": "Ultimate Wired for Xbox", "type": 67},
    "98": {"name": "Ultimate Wired for Xbox", "type": 40},
    "99": {"name": "Zero 2 gamepad", "type": 30},
}

API_URL = "http://dl.8bitdo.com:8080/firmware/select"
DOWNLOAD_URL = "http://dl.8bitdo.com:8080"


def print_header():
    print("\n" + "=" * 60)
    print("  8BitDo Firmware Updater")
    print("=" * 60 + "\n")


def display_gamepads():
    """Display available gamepad options"""
    print("Available gamepads:\n")
    for key, gamepad in GAMEPADS.items():
        print(f"  {key:2}. {gamepad['name']}")
    print()


def select_gamepad():
    """Prompt user to select their gamepad"""
    while True:
        choice = input("Enter the number of your gamepad: ").strip()
        if choice in GAMEPADS:
            return GAMEPADS[choice]
        print("Invalid selection. Please try again.\n")


def fetch_firmware_list(gamepad_type, include_beta=False):
    """Fetch available firmware versions from 8BitDo API"""
    print(f"\nFetching firmware list for {gamepad_type}...")
    
    headers = {
        'Type': str(gamepad_type),
        'Beta': '1' if include_beta else '0'
    }
    
    try:
        response = requests.post(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('msgState') != 1:
            print(f"Error from API: {data.get('error', 'Unknown error')}")
            return None
        
        return data.get('list', [])
    except requests.RequestException as e:
        print(f"Error fetching firmware list: {e}")
        return None


def display_firmware_versions(firmware_list):
    """Display available firmware versions"""
    if not firmware_list:
        print("No firmware versions found.")
        return None
    
    print("\nAvailable firmware versions:\n")
    for idx, fw in enumerate(firmware_list, 1):
        version = fw.get('version', 'Unknown')
        date = fw.get('date', 'Unknown')
        size_kb = fw.get('fileSize', 0) / 1024
        beta = " (BETA)" if fw.get('beta') else ""
        print(f"  {idx}. Version {version} - {date} ({size_kb:.1f} KB){beta}")
    
    return firmware_list


def select_firmware(firmware_list):
    """Prompt user to select firmware version"""
    while True:
        try:
            choice = input("\nEnter the number of the firmware to download (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(firmware_list):
                return firmware_list[idx]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def download_firmware(firmware):
    """Download the selected firmware file"""
    file_path = firmware.get('filePathName')
    if not file_path:
        print("Error: No file path found in firmware data")
        return None
    
    url = f"{DOWNLOAD_URL}{file_path}"
    filename = Path(file_path).name
    
    print(f"\nDownloading firmware: {filename}...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Firmware downloaded successfully: {filename}")
        return filename
    except requests.RequestException as e:
        print(f"Error downloading firmware: {e}")
        return None


def get_gamepad_device_id():
    """Get the device ID from fwupdmgr"""
    print("\nSearching for 8BitDo gamepad...")
    
    try:
        result = subprocess.run(
            ['fwupdmgr', 'get-devices', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        devices = json.loads(result.stdout)
        
        # Look for 8BitDo device
        for device in devices.get('Devices', []):
            vendor = device.get('Vendor', '').lower()
            if '8bitdo' in vendor or '8bit' in vendor:
                device_id = device.get('DeviceId')
                name = device.get('Name', 'Unknown')
                version = device.get('Version', 'Unknown')
                
                print(f"\n✓ Found: {name}")
                print(f"  Current version: {version}")
                print(f"  Device ID: {device_id}")
                
                return device_id
        
        print("No 8BitDo gamepad found.")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error running fwupdmgr: {e}")
        print("Make sure fwupd is installed and you have the necessary permissions.")
        return None
    except json.JSONDecodeError:
        print("Error parsing fwupdmgr output. Trying alternative method...")
        return get_device_id_fallback()


def get_device_id_fallback():
    """Fallback method to get device ID from text output"""
    try:
        result = subprocess.run(
            ['fwupdmgr', 'get-devices'],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.split('\n')
        device_id = None
        
        for i, line in enumerate(lines):
            if '8bitdo' in line.lower():
                # Look for Device ID in nearby lines
                for j in range(max(0, i-5), min(len(lines), i+10)):
                    if 'Device ID:' in lines[j]:
                        device_id = lines[j].split('Device ID:')[1].strip()
                        break
                if device_id:
                    print(f"\n✓ Found device ID: {device_id}")
                    return device_id
        
        return None
    except subprocess.CalledProcessError:
        return None


def flash_firmware(firmware_file, device_id):
    """Flash the firmware to the gamepad"""
    print("\nFlashing firmware to gamepad...")
    print("This may take a minute. Please do not disconnect the gamepad.")
    print("You may be prompted for your sudo password...\n")
    
    try:
        # Run with sudo for proper permissions
        result = subprocess.run(
            ['sudo', 'fwupdtool', 'install-blob', firmware_file, device_id],
            text=True
        )
        
        if result.returncode == 0:
            print("\n✓ Firmware flashed successfully!")
            print("\nThe gamepad may restart automatically.")
            print("If it doesn't, please manually restart it by disconnecting and reconnecting.")
            return True
        else:
            print(f"\n✗ Error flashing firmware (exit code: {result.returncode})")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error running fwupdtool: {e}")
        return False
    except FileNotFoundError:
        print("Error: fwupdtool not found. Please install fwupd.")
        return False


def print_instructions():
    """Print instructions for putting gamepad in bootloader mode"""
    print("\n" + "=" * 60)
    print("  INSTRUCTIONS")
    print("=" * 60)
    print("\n1. Put your gamepad in bootloader mode (if it is an adapter simply connect it and skip steps 2 and 3):")
    print("   - Hold down L1 + R1 + START for 3 seconds")
    print("   - A status LED should blink RED")
    print("\n2. Connect the gamepad to your computer via USB cable")
    print("\n3. Press Enter when ready...")
    print("=" * 60 + "\n")
    input()


def cleanup_firmware_file(filename):
    """Ask user if they want to keep the firmware file"""
    response = input(f"\nDo you want to keep the firmware file '{filename}'? (y/n): ").strip().lower()
    if response != 'y':
        try:
            os.remove(filename)
            print(f"✓ Removed {filename}")
        except OSError as e:
            print(f"Error removing file: {e}")


def main():
    """Main function"""
    print_header()
    
    # Check if fwupd tools are available
    try:
        subprocess.run(['fwupdmgr', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: fwupd is not installed or not in PATH.")
        print("Please install fwupd first: sudo apt install fwupd")
        sys.exit(1)
    
    # Step 1: Select gamepad
    display_gamepads()
    selected_gamepad = select_gamepad()
    print(f"\nSelected: {selected_gamepad['name']}")
    
    # Step 2: Fetch firmware list
    include_beta = input("\nInclude beta versions? (y/n): ").strip().lower() == 'y'
    firmware_list = fetch_firmware_list(selected_gamepad['type'], include_beta)
    
    if not firmware_list:
        print("Failed to fetch firmware list. Exiting.")
        sys.exit(1)
    
    # Step 3: Select firmware version
    firmware_list = display_firmware_versions(firmware_list)
    selected_firmware = select_firmware(firmware_list)
    
    if not selected_firmware:
        print("Exiting.")
        sys.exit(0)
    
    # Step 4: Download firmware
    firmware_file = download_firmware(selected_firmware)
    
    if not firmware_file:
        print("Failed to download firmware. Exiting.")
        sys.exit(1)
    
    # Step 5: Show instructions
    print_instructions()
    
    # Step 6: Get device ID
    device_id = get_gamepad_device_id()
    
    if not device_id:
        print("\nCouldn't find your gamepad. Make sure it's in bootloader mode and connected.")
        cleanup_firmware_file(firmware_file)
        sys.exit(1)
    
    # Step 7: Confirm before flashing
    response = input("\nProceed with firmware update? (y/n): ").strip().lower()
    if response != 'y':
        print("Update cancelled.")
        cleanup_firmware_file(firmware_file)
        sys.exit(0)
    
    # Step 8: Flash firmware
    success = flash_firmware(firmware_file, device_id)
    
    # Step 9: Cleanup
    cleanup_firmware_file(firmware_file)
    
    if success:
        print("\n" + "=" * 60)
        print("  Update completed successfully!")
        print("=" * 60 + "\n")
    else:
        print("\nUpdate failed. Please try again or update manually.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
