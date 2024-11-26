from uninstaller import uninstall_program

def main():
    programs = {
        "1": "MonkiTableOrderInstaller",
        "2": "MonthlyKitchenPOS",
        "3": "both"
    }

    print("Choose an option to uninstall:")
    print("1: MonkiTableOrderInstaller")
    print("2: MonthlyKitchenPOS")
    print("3: Both")

    choice = input("Enter your choice (1, 2, or 3): ").strip()

    if choice == "1":
        uninstall_program(programs["1"])
    elif choice == "2":
        uninstall_program(programs["2"])
    elif choice == "3":
        uninstall_program(programs["1"])
        uninstall_program(programs["2"])
    else:
        print("Invalid choice. No programs will be uninstalled.")

    print("Uninstallation process completed.")


if __name__ == "__main__":
    main()
