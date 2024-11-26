from uninstaller import uninstall_program

def main():
    programs = {
        "1": "MonkiTableOrderInstaller",
        "2": "MonthlyKitchenPOS",
        "3": "both",
        "4": "exit"
    }

    while True:
        print("\nChoose an option:")
        print("1: MonkiTableOrderInstaller")
        print("2: MonthlyKitchenPOS")
        print("3: Both")
        print("4: Exit")

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
