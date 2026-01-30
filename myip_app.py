import rumps
import requests
import threading
import socket
import subprocess
import os
from pathlib import Path
from Cocoa import NSAttributedString, NSFont, NSFontAttributeName, NSBaselineOffsetAttributeName

class IPApp(rumps.App):
    def __init__(self):
        super(IPApp, self).__init__("🌐 ...")
        
        self.full_data = {}
        self.local_data = {}
        
        # --- Menu Items ---
        
        # Public IP Section
        self.public_ip_item = rumps.MenuItem("Public: Loading...", callback=self.on_copy_public)
        self.location_item = rumps.MenuItem("📍 Location: ---")
        self.isp_item = rumps.MenuItem("🏢 ISP: ---")
        
        # Local IP Section
        self.local_ip_item = rumps.MenuItem("Local: Loading...", callback=self.on_copy_local)
        self.interface_item = rumps.MenuItem("🔌 Interface: ---")
        
        # Preferences
        self.launch_login_item = rumps.MenuItem("🚀 Launch at Login", callback=self.toggle_launch_at_login)
        self.check_launch_at_login() # Update state

        # Construct Menu
        self.menu = [
            self.public_ip_item,
            self.location_item,
            self.isp_item,
            rumps.separator,
            self.local_ip_item,
            self.interface_item,
            rumps.separator,
            "Refresh",
            rumps.separator,
            ["Preferences", [
                self.launch_login_item,
                rumps.MenuItem("About MyIP", callback=self.on_about)
            ]],
            rumps.separator,
            # Quit is added automatically by rumps, but we can explicit if needed.
            # Rumps adds it at the end.
        ]
        
        # Start Timer (5 mins)
        self.timer = rumps.Timer(self.update_all, 300)
        self.timer.start()
        
        # Initial Update
        self.update_all(None)

    # --- UI Updates ---

    def set_title(self, text):
        """Sets the menu bar title with vertical alignment correction."""
        try:
            font = NSFont.menuBarFontOfSize_(0)
            attributes = {
                NSFontAttributeName: font,
                NSBaselineOffsetAttributeName: 2.0, # Push text up
            }
            attr_str = NSAttributedString.alloc().initWithString_attributes_(text, attributes)
            self._nsstatusitem.button().setAttributedTitle_(attr_str)
        except Exception:
            self.title = text

    def update_ui(self):
        # Public Data
        ip = self.full_data.get("ip") or self.full_data.get("query") or "Offline"
        city = self.full_data.get("city", "Unknown")
        country = self.full_data.get("country_name") or self.full_data.get("country") or "Unknown"
        org = self.full_data.get("org") or self.full_data.get("isp") or "Unknown ISP"
        
        # Set Bar Title
        self.set_title(f"🌐 {ip}")
        
        # Set Menu Items
        self.public_ip_item.title = f"Public: {ip}"
        self.location_item.title = f"📍 {city}, {country}"
        self.isp_item.title = f"🏢 {org}"
        
        # Local Data
        local_ip = self.local_data.get("ip", "Unknown")
        interface = self.local_data.get("interface", "Unknown")
        
        self.local_ip_item.title = f"Local:  {local_ip}"
        self.interface_item.title = f"🔌 {interface}"

    # --- Actions ---

    @rumps.clicked("Refresh")
    def on_refresh(self, _):
        self.set_title("🌐 ↻")
        self.public_ip_item.title = "Public: Refreshing..."
        self.update_all(_)

    def on_copy_public(self, _):
        ip = self.full_data.get("ip") or self.full_data.get("query")
        if ip:
            rumps.clipboard_copy(ip)
            rumps.notification("MyIP", "Copied Public IP", ip)

    def on_copy_local(self, _):
        ip = self.local_data.get("ip")
        if ip:
            rumps.clipboard_copy(ip)
            rumps.notification("MyIP", "Copied Local IP", ip)

    def on_about(self, _):
        rumps.alert("MyIP App", "A simple menu bar tool for IP details.\n\nVersion 1.0\nCreated with Python & Rumps")

    # --- Data Fetching ---

    def update_all(self, _):
        # Threaded fetch
        thread = threading.Thread(target=self._fetch_logic)
        thread.start()

    def _fetch_logic(self):
        # 1. Get Local IP & Interface (Fast, Synchronous-ish)
        self.local_data = self._get_local_info()
        
        # 2. Get Public IP (Network Request)
        self._fetch_public_ip()
        
        # 3. Update UI (Main Thread via rumps logic, though simple assigns usually safe)
        self.update_ui()

    def _get_local_info(self):
        """Determines local IP and active interface name."""
        info = {"ip": "Unknown", "interface": "Unknown"}
        try:
            # Get Local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            local_ip = s.getsockname()[0]
            s.close()
            info["ip"] = local_ip
            
            # Identify Interface for this IP
            # We use 'route get <ip>' to find the interface
            result = subprocess.run(["route", "get", "1.1.1.1"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "interface:" in line:
                        dev = line.split(":")[1].strip() # e.g., en0
                        # Now map en0 to "Wi-Fi"
                        info["interface"] = self._map_dev_to_name(dev)
                        break
        except Exception:
            pass
        return info

    def _map_dev_to_name(self, dev_id):
        """Maps 'en0' to 'Wi-Fi' using networksetup."""
        try:
            res = subprocess.run(["networksetup", "-listallhardwareports"], capture_output=True, text=True)
            lines = res.stdout.splitlines()
            # Format:
            # Hardware Port: Wi-Fi
            # Device: en0
            current_port = None
            for line in lines:
                if "Hardware Port:" in line:
                    current_port = line.split(":")[1].strip()
                if "Device:" in line:
                    if dev_id in line:
                        return f"{current_port} ({dev_id})"
            return dev_id
        except:
            return dev_id

    def _fetch_public_ip(self):
        # 1. Try ipapi.co
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get("https://ipapi.co/json/", headers=headers, timeout=10)
            if response.status_code == 200:
                self.full_data = response.json()
                return
        except: pass

        # 2. Try ip-api.com
        try:
            response = requests.get("http://ip-api.com/json/", timeout=10)
            if response.status_code == 200:
                self.full_data = response.json()
                return
        except: pass

        # 3. Fallback
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            if response.status_code == 200:
                self.full_data = {"ip": response.json().get("ip")}
                return
        except: pass
        
        self.full_data = {} # Offline

    # --- Launch at Login ---
    
    @property
    def plist_path(self):
        return Path.home() / "Library/LaunchAgents/com.user.myip.plist"

    def check_launch_at_login(self):
        self.launch_login_item.state = self.plist_path.exists()

    def toggle_launch_at_login(self, sender):
        if self.plist_path.exists():
            # Remove
            try:
                self.plist_path.unlink()
                sender.state = False
                rumps.notification("MyIP", "Launch at Login", "Disabled")
            except Exception as e:
                rumps.alert("Error", str(e))
        else:
            # Add
            try:
                self._create_plist()
                sender.state = True
                rumps.notification("MyIP", "Launch at Login", "Enabled")
            except Exception as e:
                rumps.alert("Error", str(e))

    def _create_plist(self):
        # We need the absolute path to the executable app. 
        # Since we are running as a script, this is tricky.
        # But if we build an .app, sys.executable will be inside the bundle.
        # For now, we point to the current script/venv runner for testing, 
        # or the App bundle if packaged.
        
        import sys
        if getattr(sys, 'frozen', False):
            # Running as .app
            app_path = sys.executable.split("/Contents/MacOS")[0]
            # Verify if it is actually the app wrapper or the binary
            # Usually sys.executable in py2app is .../Contents/MacOS/myip_app
            # We want to launch that executable directly.
            cmd_path = sys.executable
        else:
            # Running as script
            # Use the absolute path to our 'run.sh' or the python executable
            # Let's use the 'run.sh' wrapper for environment safety
            cmd_path = str(Path.cwd() / "run.sh")

        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.myip</string>
    <key>ProgramArguments</key>
    <array>
        <string>{cmd_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        self.plist_path.write_text(plist_content)

if __name__ == "__main__":
    IPApp().run()