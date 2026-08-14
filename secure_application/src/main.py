from database import initialize_database
from auth import login


def main():

    # Initialize database when application starts
    initialize_database()

    while True:

        print("\n========================================")
        print("       HOSPITAL MANAGEMENT SYSTEM")
        print("========================================")

        print("1. Login")
        print("2. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":

            user = login()

            if user:
                print("\nLogin functionality is working.")
                print("Hospital modules will be added next.")

        elif choice == "2":

            print("\nThank you for using the Hospital Management System.")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()