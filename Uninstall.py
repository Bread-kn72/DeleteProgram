import os
import subprocess

def uninstall_program(program_name):
    try:
        # WMIC 명령어로 프로그램 검색 및 제거
        find_command = f'wmic product where "name like \'%{program_name}%\'" get name'
        process = subprocess.run(find_command, shell=True, capture_output=True, text=True)

        # 검색 결과가 비어 있는지 확인
        if program_name not in process.stdout:
            print(f"{program_name} is not installed.")
            return

        # 프로그램 제거 명령 실행
        uninstall_command = f'wmic product where "name like \'%{program_name}%\'" call uninstall /nointeractive'
        print(f"Attempting to uninstall {program_name}...")
        uninstall_process = subprocess.run(uninstall_command, shell=True, capture_output=True, text=True)

        # 제거 성공 여부 확인
        if "ReturnValue = 0" in uninstall_process.stdout:
            print(f"{program_name} has been successfully uninstalled.")
        else:
            print(f"Failed to uninstall {program_name}. It may require additional permissions or a different method.")
    except Exception as e:
        print(f"An error occurred while trying to uninstall {program_name}: {e}")

# 삭제하려는 프로그램 이름
programs_to_remove = ["MonkiTableOrderInstaller", "MonthlyKitchenPOS"]

for program in programs_to_remove:
    uninstall_program(program)

print("엔터를 누르면 프로그램이 종료됩니다 새 버전을 설치해주세요")
input()
print("프로그램을 종료합니다.")
