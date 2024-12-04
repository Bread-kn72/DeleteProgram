import winreg
import subprocess
import time
import pyautogui

def uninstall_with_wmic(program_name):
    try:
        find_command = f'wmic product where "name like \'%{program_name}%\'" get name'
        process = subprocess.run(find_command, shell=True, capture_output=True, text=True)

        if program_name not in process.stdout:
            print(f"{program_name} is not installed via WMIC.")
            return False

        uninstall_command = f'wmic product where "name like \'%{program_name}%\'" call uninstall /nointeractive /noreboot'
        print(f"Attempting to uninstall {program_name} using WMIC...")
        uninstall_process = subprocess.run(uninstall_command, shell=True, capture_output=True, text=True)

        if "ReturnValue = 0" in uninstall_process.stdout:
            print(f"{program_name} has been successfully uninstalled.")
            return True
        else:
            print(f"Failed to uninstall {program_name} using WMIC.")
            return False
    except Exception as e:
        print(f"An error occurred while trying to uninstall {program_name} with WMIC: {e}")
        return False


def uninstall_from_registry(root_key, uninstall_key_path, program_name):
    try:
        with winreg.OpenKey(root_key, uninstall_key_path) as key:
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, index)
                    index += 1

                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if program_name.lower() in display_name.lower():
                                uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                print(f"Uninstalling {display_name} using {uninstall_string}...")

                                process = subprocess.Popen(uninstall_string, shell=True)
                                time.sleep(5)
                                pyautogui.press("o")
                                process.wait()
                                print(f"{display_name} has been successfully uninstalled.")
                                return True
                        except FileNotFoundError:
                            continue
                except OSError:
                    break
        return False
    except Exception as e:
        print(f"An error occurred while trying to access the registry: {e}")
        return False


def uninstall_program(program_name):
    if program_name == "MonkiTableOrderInstaller":
        if uninstall_with_wmic(program_name):
            return

    uninstall_key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    if uninstall_from_registry(winreg.HKEY_LOCAL_MACHINE, uninstall_key_path, program_name):
        return
    if uninstall_from_registry(winreg.HKEY_CURRENT_USER, uninstall_key_path, program_name):
        return

    print(f"{program_name} could not be uninstalled.")