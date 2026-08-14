from database import initialize_database
from auth import login
from patients import register_patient, view_all_patients
from appointments import book_appointment, view_appointments


def hospital_menu(user):
    """Display the main hospital management menu."""

    while True:

        print("\n========================================")
        print("       HOSPITAL MANAGEMENT SYSTEM")
        print("========================================")

        print(f"Logged in as: {user['username']} ({user['role']})")
        print("----------------------------------------")

        print("1. Register Patient")
        print("2. View All Patients")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Logout")

        choice = input("\nEnter choice: ")

        if choice == "1":

            register_patient()

        elif choice == "2":

            view_all_patients()

        elif choice == "3":

            book_appointment()

        elif choice == "4":

            view_appointments()

        elif choice == "5":

            print("\nLogged out successfully.")
            break

        else:

            print("\nInvalid choice. Please try again.")


def main():

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
                hospital_menu(user)

        elif choice == "2":

            print("\nThank you for using the Hospital Management System.")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()