from uninstaller import uninstall_program

def main():
    programs = {
        "1": "MonkiTableOrderInstaller",
        "2": "MonthlyKitchenPOS",
        "3": "both",
        "4": "exit"
    }

    while True:
        print("\n삭제할 프로그램을 선택하세요:")
        print("1: 윈도우즈 테이블오더")
        print("2: 테이블오더 에이전트")
        print("3: 윈도우즈, 에이전트 모두 삭제")
        print("4: 종료")

        choice = input("Enter your choice (1, 2, 3, or 4): ").strip()

        if choice == "1":
            uninstall_program(programs["1"])
        elif choice == "2":
            uninstall_program(programs["2"])
        elif choice == "3":
            uninstall_program(programs["1"])
            uninstall_program(programs["2"])
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

    print("Goodbye!")

if __name__ == "__main__":
    main()
