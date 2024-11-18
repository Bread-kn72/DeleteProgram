import os
import winreg
import subprocess
import time
import pyautogui

def uninstall_with_wmic(program_name):
    """
    WMIC를 사용해 프로그램 제거
    """
    try:
        # WMIC 명령어로 프로그램 검색
        find_command = f'wmic product where "name like \'%{program_name}%\'" get name'
        process = subprocess.run(find_command, shell=True, capture_output=True, text=True)

        # 검색 결과 확인
        if program_name not in process.stdout:
            print(f"{program_name} is not installed via WMIC.")
            return False

        # 프로그램 제거 명령 실행
        uninstall_command = f'wmic product where "name like \'%{program_name}%\'" call uninstall /nointeractive'
        print(f"Attempting to uninstall {program_name} using WMIC...")
        uninstall_process = subprocess.run(uninstall_command, shell=True, capture_output=True, text=True)

        # 제거 성공 여부 확인
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
    """
    레지스트리를 사용해 프로그램 제거
    """
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

                                # 확인 창 처리
                                time.sleep(5)  # 확인 창 대기
                                pyautogui.press("o")  # o 키 입력
                                
                                process.wait()  # 제거 프로세스 대기
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
    """
    프로그램 제거를 위한 메인 함수
    """
    # MonkiTableOrderInstaller는 WMIC 사용
    if program_name == "MonkiTableOrderInstaller":
        if uninstall_with_wmic(program_name):
            return

    # MonthlyKitchenPOS는 레지스트리 사용
    uninstall_key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    if uninstall_from_registry(winreg.HKEY_LOCAL_MACHINE, uninstall_key_path, program_name):
        return
    if uninstall_from_registry(winreg.HKEY_CURRENT_USER, uninstall_key_path, program_name):
        return

    print(f"{program_name} could not be uninstalled.")


# 삭제하려는 프로그램 이름
programs_to_remove = ["MonkiTableOrderInstaller", "MonthlyKitchenPOS"]

for program in programs_to_remove:
    uninstall_program(program)

print("모든 제거 작업이 완료되었습니다.")
time.sleep(3)
