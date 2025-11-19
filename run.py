import sys
import subprocess
from pathlib import Path
import yaml


def get_config_path():
    return Path.home() / ".config" / "acli" / "rovodev_config.yaml"


def check_login_status():
    config_path = get_config_path()
    
    if not config_path.exists():
        return False, None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if config and 'profile' in config:
            profile = config['profile']
            if 'email' in profile and 'accountId' in profile:
                return True, config
        
        return False, None
    
    except Exception as e:
        print(f"Error reading configuration: {e}")
        return False, None


def display_login_info(config):
    profile = config.get('profile', {})
    email = profile.get('email', 'Unknown')
    account_id = profile.get('accountId', 'Unknown')
    
    print("Login found.")
    print(f"Email: {email}")
    print(f"Account ID: {account_id}")


def find_acli_executable():
    current_acli = Path("acli.exe")
    if current_acli.exists():
        return current_acli.resolve()
    
    home_acli = Path.home() / "acli.exe"
    if home_acli.exists():
        return home_acli.resolve()
    
    try:
        result = subprocess.run(
            ["where", "acli"],
            capture_output=True,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            return Path(result.stdout.strip().split('\n')[0])
    except Exception:
        pass
    
    return None


def launch_acli(logged_in=True):
    acli_path = find_acli_executable()
    
    if not acli_path:
        print("Error: Could not find acli.exe")
        return False
    
    print(f"Launching ACLI: {acli_path}")
    
    try:
        if logged_in:
            subprocess.run([str(acli_path)], shell=True)
        else:
            print("No login found. Starting login process...")
            subprocess.run([str(acli_path), "rovodev", "login"], shell=True)
        
        return True
    
    except Exception as e:
        print(f"Error launching ACLI: {e}")
        return False


def main():
    print("Rovodev ACLI Launcher")
    print("-" * 40)
    
    is_logged_in, config = check_login_status()
    
    if is_logged_in:
        display_login_info(config)
        launch_acli(logged_in=True)
    else:
        print("No saved login found.")
        launch_acli(logged_in=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
