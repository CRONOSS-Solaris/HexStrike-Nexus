#!/usr/bin/env python3
"""
HexStrike Nexus Installation Script
Handles installation of HexStrike Core and dependencies
"""
import os
import sys
import subprocess
import shutil
import json
from pathlib import Path


class HexStrikeInstaller:
    """Installer for HexStrike Nexus"""
    
    def __init__(self):
        self.home_dir = Path.home()
        self.hexstrike_dir = self.home_dir / ".hexstrike"
        self.core_dir = self.hexstrike_dir / "core"
        self.config_file = self.hexstrike_dir / "config.json"
        
    def print_banner(self):
        """Print installation banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║              HexStrike Nexus Installer                    ║
║         Advanced Cybersecurity AI Framework               ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_python_version(self):
        """Ensure Python version is 3.8+"""
        print("[*] Checking Python version...")
        if sys.version_info < (3, 8):
            print("[✗] Error: Python 3.8 or higher is required")
            print(f"[!] Current version: {sys.version}")
            return False
        print(f"[✓] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    
    def create_directories(self):
        """Create necessary directories"""
        print("[*] Creating directories...")
        try:
            self.hexstrike_dir.mkdir(parents=True, exist_ok=True)
            self.core_dir.mkdir(parents=True, exist_ok=True)
            print(f"[✓] Created directory: {self.hexstrike_dir}")
            print(f"[✓] Created directory: {self.core_dir}")
            return True
        except PermissionError:
            print(f"[✗] Permission denied: Cannot create {self.hexstrike_dir}")
            print("[!] Try running with appropriate permissions")
            return False
        except Exception as e:
            print(f"[✗] Error creating directories: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("[*] Installing Python dependencies...")
        
        dependencies = [
            "requests",
            "PyQt6",
            "markdown"
        ]
        
        for dep in dependencies:
            print(f"[*] Installing {dep}...")
            
            # Try normal installation first
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"[✓] {dep} installed successfully")
                continue
            except subprocess.CalledProcessError as e:
                # Check if it's externally-managed environment error
                if "externally-managed-environment" in e.stderr or "externally managed" in e.stderr.lower():
                    print(f"[!] System Python is externally managed, trying --user installation...")
                    
                    # Try with --user flag
                    try:
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", "--user", dep],
                            check=True,
                            capture_output=True,
                            text=True
                        )
                        print(f"[✓] {dep} installed successfully (user install)")
                        continue
                    except subprocess.CalledProcessError as e2:
                        print(f"[✗] Failed to install {dep}")
                        print(f"[!] Error: {e2.stderr}")
                        print("\n[!] Alternative: Create a virtual environment:")
                        print("    python3 -m venv hexstrike-env")
                        print("    source hexstrike-env/bin/activate")
                        print("    python -m pip install requests PyQt6 markdown")
                        return False
                else:
                    print(f"[✗] Failed to install {dep}")
                    print(f"[!] Error: {e.stderr}")
                    return False
            except Exception as e:
                print(f"[✗] Unexpected error installing {dep}: {e}")
                return False
        
        return True
    
    def create_config(self):
        """Create initial configuration file"""
        print("[*] Creating configuration...")
        
        try:
            # Note: Language will be selected on first dashboard launch
            config = {
                "version": "1.0.0",
                "installed": True
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"[✓] Configuration created: {self.config_file}")
            print("[i] Language will be selected on first dashboard launch")
            return True
            
        except PermissionError:
            print(f"[✗] Permission denied: Cannot write to {self.config_file}")
            return False
        except Exception as e:
            print(f"[✗] Error creating config: {e}")
            return False
    
    def clone_hexstrike_core(self):
        """Clone or update HexStrike Core repository"""
        print("[*] Setting up HexStrike Core...")
        
        repo_url = "https://github.com/CRONOSS-Solaris/HexStrike-Core.git"
        
        try:
            if self.core_dir.exists() and (self.core_dir / ".git").exists():
                print("[*] HexStrike Core already exists, updating...")
                try:
                    subprocess.run(
                        ["git", "-C", str(self.core_dir), "pull"],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print("[✓] HexStrike Core updated")
                except subprocess.CalledProcessError:
                    print("[!] Git pull failed, attempting fresh clone...")
                    shutil.rmtree(self.core_dir, ignore_errors=True)
                    return self.clone_hexstrike_core()
            else:
                print(f"[*] Cloning HexStrike Core from {repo_url}...")
                subprocess.run(
                    ["git", "clone", repo_url, str(self.core_dir)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("[✓] HexStrike Core cloned successfully")
            
            return True
            
        except FileNotFoundError:
            print("[✗] Git is not installed or not in PATH")
            print("[!] Please install Git: https://git-scm.com/downloads")
            return False
        except subprocess.CalledProcessError as e:
            print("[✗] Failed to clone/update HexStrike Core")
            print(f"[!] Error: {e.stderr if e.stderr else 'Unknown error'}")
            return False
        except Exception as e:
            print(f"[✗] Unexpected error: {e}")
            return False
    
    def verify_installation(self):
        """Verify that installation completed successfully"""
        print("[*] Verifying installation...")
        
        checks = [
            (self.hexstrike_dir.exists(), f"Directory {self.hexstrike_dir}"),
            (self.core_dir.exists(), f"Directory {self.core_dir}"),
            (self.config_file.exists(), f"Config file {self.config_file}"),
        ]
        
        all_passed = True
        for check, description in checks:
            if check:
                print(f"[✓] {description}")
            else:
                print(f"[✗] {description}")
                all_passed = False
        
        return all_passed
    
    def run(self):
        """Run the installation process"""
        self.print_banner()
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating directories", self.create_directories),
            ("Installing dependencies", self.install_dependencies),
            ("Creating configuration", self.create_config),
            ("Setting up HexStrike Core", self.clone_hexstrike_core),
            ("Verifying installation", self.verify_installation),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*60}")
            print(f"Step: {step_name}")
            print('='*60)
            
            try:
                if not step_func():
                    print(f"\n[✗] Installation failed at step: {step_name}")
                    print("[!] Please fix the errors above and try again")
                    return False
            except KeyboardInterrupt:
                print("\n\n[!] Installation cancelled by user")
                return False
            except Exception as e:
                print(f"\n[✗] Unexpected error in {step_name}: {e}")
                print("[!] Please report this issue with the error details")
                return False
        
        print("\n" + "="*60)
        print("✓ Installation completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python -m hexstrike_nexus.main")
        print("2. Select your preferred language (PL/EN)")
        print("3. Configure your AI provider")
        print("4. Start using HexStrike Nexus!")
        print("\nFor help, visit: https://github.com/CRONOSS-Solaris/HexStrike-Nexus")
        return True


def main():
    """Main entry point"""
    installer = HexStrikeInstaller()
    
    try:
        success = installer.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[!] Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n[✗] Fatal error: {e}")
        print("[!] Please report this issue")
        sys.exit(1)


if __name__ == "__main__":
    main()
