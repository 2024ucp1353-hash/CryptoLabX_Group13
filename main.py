# ==========================================
# CryptoLabA2 - Main Program
# Week 1 Foundation
# ==========================================

from utils.file_analysis import analyze_file
from utils.logger import log_execution

def display_banner():
    print("\n" + "=" * 45)
    print("            Welcome to CryptoLabA2")
    print("=" * 45)


def display_menu():
    print("\nSelect an option:")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")


def encrypt():
    print("\n[Encrypt]")
    print("Feature Coming Soon...")


def decrypt():
    print("\n[Decrypt]")
    print("Feature Coming Soon...")


def attack():
    print("\n[Attack]")
    print("Feature Coming Soon...")


def analyze():
    analyze_file()


def get_choice():
    return input("\nEnter your choice (1-5): ").strip()


def main():

    while True:

        display_banner()
        display_menu()

        choice = get_choice()

        if choice == "1":
            log_execution("1. Encrypt")
            encrypt()

        elif choice == "2":
            log_execution("2. Decrypt")
            decrypt()

        elif choice == "3":
            log_execution("3. Attack")
            attack()

        elif choice == "4":
            log_execution("4. Analyze")
            analyze()

        elif choice == "5":
            log_execution("5. Exit")
            print("\nThank you for using CryptoLabA2.")
            print("Exiting...")
            break

        else:
            log_execution(f"Invalid Choice ({choice})")
            print("\nInvalid choice! Please enter a number between 1 and 5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()