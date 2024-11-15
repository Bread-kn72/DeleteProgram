import os
import winreg
import subprocess
import keyboard

def uninstall_program_from_registry(root_key, uninstall_key_path, program_name):
    """
    지정된 레지스트리 경로에서 프로그램 제거
    """
    try:
        with winreg.OpenKey(root_key, uninstall_key_path) as key:
            index = 0
            while True:
                try:
                    # 하위 키 이름 가져오기
                    subkey_name = winreg.EnumKey(key, index)
                    index += 1

                    # 하위 키 열기
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        # DisplayName 확인
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if program_name.lower() in display_name.lower():
                                # UninstallString 확인
                                uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                print(f"Uninstalling {display_name} using {uninstall_string}...")

                                # 프로그램 제거 실행
                                subprocess.run(uninstall_string, shell=True)
                                print(f"{display_name} has been successfully uninstalled.")
                                return True
                        except FileNotFoundError:
                            continue
                except OSError:
                    # 더 이상 하위 키가 없을 때 루프 종료
                    break

        return False  # 프로그램을 찾지 못한 경우
    except Exception as e:
        print(f"An error occurred while trying to access the registry: {e}")
        return False


def uninstall_program(program_name):
    """
    HKEY_LOCAL_MACHINE 및 HKEY_CURRENT_USER에서 프로그램 제거
    """
    # HKEY_LOCAL_MACHINE 확인
    uninstall_key_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    if uninstall_program_from_registry(winreg.HKEY_LOCAL_MACHINE, uninstall_key_path, program_name):
        return

    # HKEY_CURRENT_USER 확인
    if uninstall_program_from_registry(winreg.HKEY_CURRENT_USER, uninstall_key_path, program_name):
        return

    print(f"{program_name} is not installed in either HKEY_LOCAL_MACHINE or HKEY_CURRENT_USER.")


# 삭제하려는 프로그램 이름
programs_to_remove = ["MonkiTableOrderInstaller", "MonthlyKitchenPOS"]

for program in programs_to_remove:
    uninstall_program(program)

print("아무 키를 누르면 프로그램이 종료됩니다. 먼키 윈도우, 먼키 에이전트의 새 버전을 설치해주세요.")
keyboard.read_event()
print("프로그램을 종료합니다.")
