import os
import subprocess
from .config import Config

class UpdateManager:
    @staticmethod
    def check_for_updates():
        """
        Checks for updates in Dashboard and HexStrike Core repos.
        Returns True if updates were applied.
        """
        updates_applied = False

        # Update HexStrike Core
        if os.path.exists(Config.HEXSTRIKE_CORE_DIR):
            print("Checking for HexStrike Core updates...")
            try:
                # Check if behind remote
                subprocess.run(["git", "-C", Config.HEXSTRIKE_CORE_DIR, "fetch"], check=True, stdout=subprocess.DEVNULL)
                status = subprocess.run(
                    ["git", "-C", Config.HEXSTRIKE_CORE_DIR, "status", "-uno"],
                    capture_output=True, text=True
                )
                if "Your branch is behind" in status.stdout:
                    print("Update found for HexStrike Core. Pulling...")
                    subprocess.run(["git", "-C", Config.HEXSTRIKE_CORE_DIR, "pull"], check=True)
                    # Re-install requirements
                    # Assuming pip is in venv
                    pip_exe = os.path.join(Config.HEXSTRIKE_CORE_DIR, "venv", "bin", "pip")
                    req_file = os.path.join(Config.HEXSTRIKE_CORE_DIR, "requirements.txt")
                    if os.path.exists(pip_exe) and os.path.exists(req_file):
                        subprocess.run([pip_exe, "install", "-r", req_file], check=True)
                    updates_applied = True
                else:
                    print("HexStrike Core is up to date.")
            except Exception as e:
                print(f"Failed to update HexStrike Core: {e}")

        # Update Dashboard (Self)
        # Assuming we are in a git repo
        dashboard_dir = Config.BASE_DIR
        try:
             # Check if behind remote
            subprocess.run(["git", "-C", dashboard_dir, "fetch"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status = subprocess.run(
                ["git", "-C", dashboard_dir, "status", "-uno"],
                capture_output=True, text=True
            )
            if "Your branch is behind" in status.stdout:
                print("Update found for Dashboard. Pulling...")
                subprocess.run(["git", "-C", dashboard_dir, "pull"], check=True)
                updates_applied = True
            else:
                 print("Dashboard is up to date.")
        except Exception:
            # We might not be in a git repo or no network
            pass

        return updates_applied
