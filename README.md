# MyIP - macOS Menu Bar Tool

A lightweight, native-feeling macOS menu bar application that displays your Public and Local IP addresses, ISP, and detailed location information.

Built with Python and `rumps`, it is designed to sit quietly in your system status bar, providing network information at a glance.

<img width="576" height="293" alt="myip-macos-screenshot" src="https://github.com/user-attachments/assets/6a769653-67f1-482f-8a5d-4deadd9153fd" />


## Features

- **🌐 Public IP:** Real-time display of your external IP address directly in the menu bar.
- **📍 Detailed Location:** Displays your City, Country, and ISP information in the dropdown menu.
- **🏠 Local Network:** Shows your local IP (LAN) and the active network interface (e.g., `Wi-Fi` or `Ethernet`).
- **📋 One-Click Copy:** Easily copy your Public or Local IP to the clipboard.
- **🚀 Launch at Login:** Built-in preference to automatically start the app when you log in.
- **🛡️ Robust:** Automatically switches between multiple API providers to ensure data is always available.
- **🎨 Native Design:** Supports Dark Mode and uses native macOS fonts and alignment.

## Installation & Usage

### 1. Prerequisites
You need **Python 3** installed on your Mac. You can check if you have it by running:
```bash
python3 --version
```

### 2. Setup
Open your terminal in the folder containing these files and run the start script. This will automatically set up a virtual environment and install dependencies (`rumps`, `requests`, `pyobjc`) on the first run.

```bash
./run.sh
```

### 3. Using the App
- The app will appear in your menu bar as: `🌐 <Your IP>`
- **Refresh:** Click the icon and select "Refresh" to force an update.
- **Copy IP:** Click on the "Public" or "Local" menu items to copy that IP to your clipboard.
- **Auto-Start:** To make it start automatically when you restart your Mac:
    1. Click the menu bar icon.
    2. Go to **Preferences**.
    3. Click **Launch at Login** (ensure the checkmark is visible).

### 4. Quitting
To close the app completely, click the menu bar icon and select **Quit**.

## Technical Details
- **Language:** Python 3.15+ (Compatible with newer macOS versions including Sonoma/Sequoia)
- **Dependencies:**
    - `rumps` (macOS status bar bindings)
    - `requests` (API fetching)
    - `pyobjc-framework-Cocoa` (Native macOS UI access)
- **Privacy:** This app **does not** log or send your data anywhere except to the public IP providers (ipapi.co, ip-api.com) strictly to fetch your location info.

## Troubleshooting
If the app doesn't appear or you see errors:
1. Ensure you have given the terminal accessibility permissions if prompted (rarely needed).
2. Check your internet connection.
3. Run `./run.sh` from the terminal to see any error output.
