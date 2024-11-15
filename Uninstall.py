import os
import winreg
import subprocess
import pyautogui
import time

def uninstall_program_from_registry(root_key, uninstall_key_path, program_name):
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

                                # 프로그램 제거 실행
                                process = subprocess.Popen(uninstall_string, shell=True)

                                # 확인 창 기다리기 및 처리 (5초 대기 후 o선택)
                                time.sleep(5)  # 확인 창이 나타날 시간을 기다림
                                pyautogui.press("o")  # o 키로 확인 창 처리
                                
                                process.wait()  # 제거 프로세스가 종료될 때까지 대기
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
    uninstall_key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    if uninstall_program_from_registry(winreg.HKEY_LOCAL_MACHINE, uninstall_key_path, program_name):
        return
    if uninstall_program_from_registry(winreg.HKEY_CURRENT_USER, uninstall_key_path, program_name):
        return
    print(f"{program_name} is not installed in either HKEY_LOCAL_MACHINE or HKEY_CURRENT_USER.")


# 삭제하려는 프로그램 이름
programs_to_remove = ["MonkiTableOrderInstaller", "MonthlyKitchenPOS"]

for program in programs_to_remove:
    uninstall_program(program)

print("모든 제거가 완료되었습니다.")
time.sleep(3)
