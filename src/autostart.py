import sys
import os
import winreg

def add_to_startup(app_name, script_path):
    # Add the app to Windows startup using registry
    key = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
        winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')

def remove_from_startup(app_name):
    key = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
            winreg.DeleteValue(regkey, app_name)
    except FileNotFoundError:
        pass
