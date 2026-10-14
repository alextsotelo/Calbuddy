import ui

def main():
    while True:
        print("\n--- CalBuddy ---")
        print("1. View Active Meals")
        print("2. Add a New Meal")
        print("3. Update a Meal")
        print("4. Delete a Meal")
        print("5. Log Meal")
        print("6. Delete a Log Entry")
        print("7. View Today's Log")
        print("8. View Period Summary")
        print("9. Data Visualizations")
        print("10. Exit")

        choice = input("\nSelect an option (1-10): ")

        if choice == "1":
            ui.display_active_meals()
        elif choice == "2":
            ui.add_meal()
        elif choice == "3":
            ui.update_meal()
        elif choice == "4":
            ui.delete_meal()
        elif choice == "5":
            ui.log_meal()
        elif choice == "6":
            ui.delete_log_entry()
        elif choice == "7":
            ui.view_today_log()
        elif choice == "8":
            ui.view_period_summary()
        elif choice == "9":
            ui.view_visualizations()
        elif choice == "10":
            print("Exiting CalBuddy...")
            break
        else:
            print("Invalid option. Please type a valid number.")

if __name__ == "__main__":
    main()
