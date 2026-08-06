# ==========================================
# CryptoLabX - Main Program
# Week 1 Foundation
# ==========================================

from utils.file_analysis import analyze_file

def display_banner():
    print("\n" + "=" * 45)
    print("            Welcome to CryptoLabX")
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
            encrypt()

        elif choice == "2":
            decrypt()

        elif choice == "3":
            attack()

        elif choice == "4":
            analyze()

        elif choice == "5":
            print("\nThank you for using CryptoLabX.")
            print("Exiting...")
            break

        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()