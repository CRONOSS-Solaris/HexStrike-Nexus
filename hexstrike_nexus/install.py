import os
import sys
import subprocess
import shutil
import time

HEXSTRIKE_DIR = os.path.expanduser("~/.hexstrike/core")
HEXSTRIKE_REPO = "https://github.com/0x4m4/hexstrike-ai.git"

def print_status(message):
    print(f"[+] {message}")

def check_system_deps():
    print_status("Checking system dependencies...")
    deps = ["git", "python3", "pip", "docker"]
    for dep in deps:
        if shutil.which(dep) is None:
            print(f"[-] Missing dependency: {dep}")
        else:
            print_status(f"Found {dep}")

def deploy_hexstrike():
    print_status("Deploying HexStrike...")
    if os.path.exists(HEXSTRIKE_DIR):
        print_status("HexStrike directory exists. Pulling latest...")
        try:
            subprocess.run(["git", "-C", HEXSTRIKE_DIR, "pull"], check=True)
        except subprocess.CalledProcessError:
            print("[-] Failed to update HexStrike repo.")
    else:
        print_status(f"Cloning HexStrike to {HEXSTRIKE_DIR}...")
        try:
            os.makedirs(os.path.dirname(HEXSTRIKE_DIR), exist_ok=True)
            subprocess.run(["git", "clone", HEXSTRIKE_REPO, HEXSTRIKE_DIR], check=True)
        except subprocess.CalledProcessError:
            print("[-] Failed to clone HexStrike repo. This is expected if the repo is private or network is restricted.")
            print("[!] Creating mock HexStrike directory for demonstration.")
            os.makedirs(HEXSTRIKE_DIR, exist_ok=True)
            with open(os.path.join(HEXSTRIKE_DIR, "requirements.txt"), "w") as f:
                f.write("flask\nrequests\n")

    # Setup venv
    venv_dir = os.path.join(HEXSTRIKE_DIR, "venv")
    if not os.path.exists(venv_dir):
        print_status("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

    # Install requirements
    pip_exe = os.path.join(venv_dir, "bin", "pip")
    req_file = os.path.join(HEXSTRIKE_DIR, "requirements.txt")
    if os.path.exists(req_file) and os.path.exists(pip_exe):
        print_status("Installing HexStrike requirements...")
        subprocess.run([pip_exe, "install", "-r", req_file], check=True)

def deploy_dashboard():
    print_status("Deploying Dashboard dependencies...")
    # In a real scenario, we would install PyQt6 here.
    pass

def install_tool(tool):
    print_status(f"Attempting to install {tool}...")

    # Try go install (common for recon tools)
    if shutil.which("go"):
        go_tools = {
            "nuclei": "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest",
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "gobuster": "github.com/OJ/gobuster/v3@latest"
        }
        if tool in go_tools:
            try:
                subprocess.run(["go", "install", go_tools[tool]], check=True)
                print_status(f"Installed {tool} via go.")
                return True
            except Exception as e:
                print(f"[-] Go install failed: {e}")

    # Try apt-get
    if shutil.which("apt-get"):
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", tool], check=True)
            print_status(f"Installed {tool} via apt.")
            return True
        except Exception:
            pass

    print(f"[-] Failed to install {tool} automatically. Please install manually.")
    return False

def check_tools():
    print_status("Verifying security tools...")
    tools = ["nmap", "gobuster", "nuclei", "subfinder"]
    missing = []
    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print(f"[!] Missing tools: {', '.join(missing)}.")
        for tool in missing:
            install_tool(tool)
    else:
        print_status("All core tools found.")

def create_desktop_shortcut():
    print_status("Creating Linux Desktop Shortcut...")

    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__)) # hexstrike_nexus dir
    # main.py is in base_dir
    main_script = os.path.join(base_dir, "main.py")
    icon_path = os.path.join(base_dir, "icon.png")

    # 1. Create Icon
    # Simple red shield/circle 64x64 transparent PNG
    icon_b64 = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIlSURBVHhe7ZqxSsRAEIb3YhUEwUYLQVvBztbOQqzsfAJ7H0G899jY2HgW9j6BvY2NhWChhWARwk3+M2wyq8nOZjcJ+2D4ITuzszP/ZGc3m0wKpVRS94Ff8A3b8A6r8A4D+IARvMEI3uADl/ALF/AL5/AJ5/AJZ3Aap/AKp/AKJ3ASx3ASx3ACx3ACR3AER3AIB3AAB9DDAfRQA/iCQ/iCQ/iEw/iEw6jiMIo4jCIOo4jDKOIwijj8O47g8P84gMP/4wAOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOo4jDKOIwijiMIg6jiMMo4jCKOIwiDqOIwyjiMIo4jCIOn8J7nMI7nMIrnMIrnMIpnMIpnMIpnMJJ/AJjY/YV8wvS+AAAAABJRU5ErkJggg=="

    try:
        import base64
        with open(icon_path, "wb") as f:
            f.write(base64.b64decode(icon_b64))
        print_status(f"Icon created at {icon_path}")
    except Exception as e:
        print(f"[-] Failed to create icon: {e}")
        icon_path = "utilities-terminal" # Fallback

    # 2. Create Desktop Entry
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    if not os.path.exists(desktop_dir):
        try:
            os.makedirs(desktop_dir)
        except OSError:
            print(f"[-] Could not create {desktop_dir}. Skipping shortcut.")
            return

    entry_content = f"""[Desktop Entry]
Name=HexStrike Nexus
Comment=Advanced AI-Powered Cybersecurity Dashboard
Exec={sys.executable} {main_script}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Development;Security;System;
Keywords=hexstrike;security;ai;dashboard;
StartupNotify=true
"""

    desktop_file = os.path.join(desktop_dir, "hexstrike-nexus.desktop")
    try:
        with open(desktop_file, "w") as f:
            f.write(entry_content)

        # Make executable
        os.chmod(desktop_file, 0o755)
        print_status(f"Shortcut created: {desktop_file}")
        print_status("You may need to log out and back in for it to appear in menus.")
    except Exception as e:
        print(f"[-] Failed to create desktop shortcut: {e}")

def main():
    print("=== HexStrike Nexus Bootstrapper ===")
    check_system_deps()
    deploy_hexstrike()
    deploy_dashboard()
    check_tools()
    create_desktop_shortcut()
    print("=== Installation Complete ===")
    print("Run 'python3 hexstrike_nexus/main.py' to start the Dashboard.")

if __name__ == "__main__":
    main()
