import os
import sys
import subprocess
import shutil
import time
import json

# Ensure we can import from hexstrike_nexus package if run directly
try:
    from hexstrike_nexus.i18n.manager import i18n
except ImportError:
    # If run from inside hexstrike_nexus or root without package structure
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from hexstrike_nexus.i18n.manager import i18n

HEXSTRIKE_DIR = os.path.expanduser("~/.hexstrike/core")
HEXSTRIKE_CONFIG = os.path.expanduser("~/.hexstrike/config.json")
HEXSTRIKE_REPO = "https://github.com/0x4m4/hexstrike-ai.git"

def print_status(message):
    print(f"[+] {message}")

def check_system_deps():
    print_status(i18n.get("check_system_deps"))
    deps = ["git", "python3", "pip", "docker"]
    for dep in deps:
        if shutil.which(dep) is None:
            print(i18n.get("missing_dep", dep=dep))
        else:
            print_status(i18n.get("found_dep", dep=dep))

def deploy_hexstrike():
    print_status(i18n.get("deploying_hexstrike"))
    if os.path.exists(HEXSTRIKE_DIR):
        print_status(i18n.get("hexstrike_exists"))
        try:
            subprocess.run(["git", "-C", HEXSTRIKE_DIR, "pull"], check=True)
        except subprocess.CalledProcessError:
            print(i18n.get("failed_update_repo"))
    else:
        print_status(i18n.get("cloning_hexstrike", path=HEXSTRIKE_DIR))
        try:
            os.makedirs(os.path.dirname(HEXSTRIKE_DIR), exist_ok=True)
            subprocess.run(["git", "clone", HEXSTRIKE_REPO, HEXSTRIKE_DIR], check=True)
        except subprocess.CalledProcessError:
            print(i18n.get("failed_clone_repo"))
            print(i18n.get("creating_mock_dir"))
            os.makedirs(HEXSTRIKE_DIR, exist_ok=True)
            with open(os.path.join(HEXSTRIKE_DIR, "requirements.txt"), "w") as f:
                f.write("flask\nrequests\n")

    # Setup venv
    venv_dir = os.path.join(HEXSTRIKE_DIR, "venv")
    if not os.path.exists(venv_dir):
        print_status(i18n.get("creating_venv"))
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

    # Install requirements
    pip_exe = os.path.join(venv_dir, "bin", "pip")
    req_file = os.path.join(HEXSTRIKE_DIR, "requirements.txt")
    if os.path.exists(req_file) and os.path.exists(pip_exe):
        print_status(i18n.get("installing_reqs"))
        subprocess.run([pip_exe, "install", "-r", req_file], check=True)

def deploy_dashboard():
    print_status(i18n.get("deploying_dashboard"))
    # Install dependencies from hexstrike_nexus/requirements.txt
    req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    if os.path.exists(req_path):
        try:
            print_status(i18n.get("installing_deps_from", path=req_path))
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path], check=True)
        except subprocess.CalledProcessError as e:
            print(i18n.get("failed_install_dashboard_deps", error=e))
    else:
        print(i18n.get("req_not_found", path=req_path))

def install_tool(tool):
    print_status(i18n.get("attempt_install_tool", tool=tool))

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
                print_status(i18n.get("installed_via_go", tool=tool))
                return True
            except Exception as e:
                print(i18n.get("go_install_failed", error=e))

    # Try apt-get
    if shutil.which("apt-get"):
        print(i18n.get("warning_apt_install", tool=tool))
        # In non-interactive mode or without password, this might fail.
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", tool], check=True)
            print_status(i18n.get("installed_via_apt", tool=tool))
            return True
        except Exception as e:
            print(i18n.get("apt_install_failed", error=e))

    print(i18n.get("failed_install_auto", tool=tool))
    return False

def check_tools():
    print_status(i18n.get("verifying_tools"))
    tools = ["nmap", "gobuster", "nuclei", "subfinder"]
    missing = []
    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print(i18n.get("missing_tools", tools=', '.join(missing)))
        for tool in missing:
            install_tool(tool)
    else:
        print_status(i18n.get("all_tools_found"))

def create_desktop_shortcut():
    print_status(i18n.get("creating_shortcut"))

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
        print_status(i18n.get("icon_created", path=icon_path))
    except Exception as e:
        print(i18n.get("failed_create_icon", error=e))
        icon_path = "utilities-terminal" # Fallback

    # 2. Create Desktop Entry
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    if not os.path.exists(desktop_dir):
        try:
            os.makedirs(desktop_dir)
        except OSError:
            print(i18n.get("failed_create_dir", path=desktop_dir))
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
        print_status(i18n.get("shortcut_created", path=desktop_file))
        print_status(i18n.get("logout_hint"))
    except Exception as e:
        print(i18n.get("failed_create_shortcut", error=e))

def select_language():
    print(i18n.get("select_language"))
    print(i18n.get("lang_en"))
    print(i18n.get("lang_pl"))
    choice = input(i18n.get("enter_choice"))

    if choice.strip() == "2":
        i18n.load_language("pl")
        lang = "pl"
    else:
        i18n.load_language("en")
        lang = "en"
        if choice.strip() != "1":
            print(i18n.get("invalid_choice"))

    # Save to config
    try:
        os.makedirs(os.path.dirname(HEXSTRIKE_CONFIG), exist_ok=True)
        config_data = {}
        if os.path.exists(HEXSTRIKE_CONFIG):
            try:
                with open(HEXSTRIKE_CONFIG, "r") as f:
                    config_data = json.load(f)
            except:
                pass

        config_data["language"] = lang

        with open(HEXSTRIKE_CONFIG, "w") as f:
            json.dump(config_data, f, indent=4)

    except Exception as e:
        print(f"[-] Failed to save language preference: {e}")

def main():
    select_language()
    print(i18n.get("bootstrapper_title"))
    check_system_deps()
    deploy_hexstrike()
    deploy_dashboard()
    check_tools()
    create_desktop_shortcut()
    print(i18n.get("install_complete"))
    print(i18n.get("run_instruction"))

if __name__ == "__main__":
    main()
