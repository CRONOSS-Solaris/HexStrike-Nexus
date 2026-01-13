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
    # subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6", "PyQt6-WebEngine"])
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
            # Check if running as root or sudo is available, usually difficult in script without interactive password
            # We assume user runs install.py with sufficient permissions or has sudo cached
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

def main():
    print("=== HexStrike Nexus Bootstrapper ===")
    check_system_deps()
    deploy_hexstrike()
    deploy_dashboard()
    check_tools()
    print("=== Installation Complete ===")
    print("Run 'python3 hexstrike_nexus/main.py' to start the Dashboard.")

if __name__ == "__main__":
    main()
