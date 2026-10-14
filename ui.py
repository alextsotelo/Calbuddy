import crud
import visuals
from datetime import date, timedelta

""" This module contains the UI logic for the application and handles user input validation. 
    It uses the crud module to interact with the database. """

def get_valid_int(prompt):
    """ Validates user input for integers """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
def get_optional_valid_int(prompt, original_value):
    """ Validates user input for integers, returning original value if input is invalid """
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return original_value
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_float(prompt):
    """ Validates user input for floats """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid float.")


def display_active_meals():
    """ Handles the UI logic for viewing active meals """
    meals = crud.get_active_meals()

    if not meals:
        print("\nNo active meals found.")
        return
    print("\n--- Active Meals ---")

    for index, meal in enumerate(meals, start = 1):
        print(f"{index}. {meal['name']} | {meal['calories']} cal | {meal['protein_g']}g protein | {meal['carbs_g']}g carbs | {meal['fat_g']}g fat")



def add_meal():
    """ Handles the UI logic for adding a new meal """
    name = input("Enter meal name: ")
    calories = get_valid_int("Enter calories: ")
    protein = get_valid_int("Enter protein (g): ")
    carbs = get_valid_int("Enter carbs (g): ")
    fat = get_valid_int("Enter fat (g): ")

    success = crud.add_meal(name, calories, protein, carbs, fat)

    if not success:
        print("Error adding meal.")
    else:
        print("Meal added successfully.")


def update_meal():
    """ Handles the UI logic for updating a meal """
    meals = crud.get_active_meals()
    if not meals:
        print("\nNo active meals found.")
        return

    for index, meal in enumerate(meals, start = 1):
        print(f"{index}. {meal['name']} | {meal['calories']} cal | {meal['protein_g']}g protein | {meal['carbs_g']}g carbs | {meal['fat_g']}g fat")

    choice = get_valid_int("Select a meal number to update: ")
    if choice < 1 or choice > len(meals):
        print("Invalid input. Please enter a valid integer.")
        return

    selected_meal = meals[choice - 1]
    current_name = selected_meal['name']

    print(f"\n--- Update Meal Details for {current_name} ---")
    print("Enter new meal details (Press ENTER to keep current value):")
    new_name = input("Meal name: ")
    if new_name == "":
        new_name = current_name

    new_calories = get_optional_valid_int("Calories: ", selected_meal['calories'])
    new_protein = get_optional_valid_int("Protein (g): ", selected_meal['protein_g'])
    new_carbs = get_optional_valid_int("Carbs (g): ", selected_meal['carbs_g'])
    new_fat = get_optional_valid_int("Fat (g): ", selected_meal['fat_g'])

    success = crud.update_meal(current_name, new_name, new_calories, new_protein, new_carbs, new_fat)

    if not success:
        print("Error updating meal.")
    else:
        print("Meal updated successfully.")

def delete_meal():
    """ Handles the UI logic for deleting a meal """
    meals = crud.get_active_meals()
    if not meals:
        print("\nNo active meals found.")
        return

    print("\n--- Active Meals ---")

    for index, meal in enumerate(meals, start=1):
        print(f"{index}. {meal['name']} | {meal['calories']} cal | {meal['protein_g']}g protein | {meal['carbs_g']}g carbs | {meal['fat_g']}g fat")

    choice = get_valid_int("\nSelect a meal number to delete: ")
    if choice < 1 or choice > len(meals):
        print("Invalid input. Please enter a valid integer.")
        return

    selected_meal = meals[choice - 1]
    success = crud.deactivate_meal(selected_meal['name'])
    if not success:
        print("Error deleting meal.")
    else:
        print("Meal deleted successfully.")


def log_meal():
    """ Handles the UI logic for logging a meal """
    meals = crud.get_active_meals()
    if not meals:
        print("\nNo active meals found. Please add a meal to your diet first.")
        return
    print("\n--- LOG A MEAL ---")
    for index, meal in enumerate(meals, start=1):
        print(f"{index}. {meal['name']}")

    choice = get_valid_int("\nSelect a meal number to log: ")
    if choice < 1 or choice > len(meals):
        print("\nInvalid selection. Number out of range.")
        return

    selected_meal = meals[choice - 1]
    meal_id = selected_meal['id']
    servings = get_valid_float("Enter number of servings: ")
    today_date = date.today()
    log_date = input("Enter date (YYYY-MM-DD) or press ENTER for today's date: ").strip()
    if log_date == "":
        log_date = today_date

    meal_time = input("Enter meal time (e.g., breakfast, lunch, dinner): ").strip()
    if meal_time == "":
        print("Please enter a valid meal time.")
        return

    success = crud.log_meal(meal_id, servings, log_date, meal_time)
    if not success:
        print("\nError logging meal.")
    else:
        print("\nMeal logged successfully.")

def view_today_log():
    """ Handles the UI logic for viewing today's log """
    today_date = date.today()
    log_entries = crud.get_log_for_date(today_date)
    if not log_entries:
        print("\nNo log entries found for today.")
        return

    print("\n--- TODAY'S LOG ---")
    for index, entry in enumerate(log_entries, start=1):
        print(f"{index}. [{entry['meal_time']}] {entry['name']} ({entry['servings']} servings) | Total: {entry['total_calories']} cal | {entry['total_protein']}g protein | {entry['total_carbs']}g carbs | {entry['total_fat']}g fat")


def delete_log_entry():
    """ Handles the UI logic for deleting a log entry from any given date """
    today_date = date.today()
    selected_date = input("Enter date (YYYY-MM-DD) to delete log entries for or press ENTER for today's date: ").strip()
    if selected_date == "":
        selected_date = today_date

    log_entries = crud.get_log_for_date(selected_date)
    if not log_entries:
        print("\nNo log entries found for the selected date.")
        return

    print(f"\n --- LOG ENTRIES FOR {selected_date} ---")
    for index, entry in enumerate(log_entries, start=1):
        print(f"{index}. [{entry['meal_time']}] {entry['name']} ({entry['servings']} servings) | Total: {entry['total_calories']} cal | {entry['total_protein']}g protein | {entry['total_carbs']}g carbs | {entry['total_fat']}g fat")

    choice = get_valid_int("\nSelect a log entry number to delete: ")
    if choice < 1 or choice > len(log_entries):
        print("\nInvalid selection. Number out of range.")
        return

    selected_entry = log_entries[choice - 1]
    success = crud.delete_log_entry(selected_entry['id'])
    if not success:
        print("\nError deleting log entry.")
    else:
        print("\nLog entry deleted successfully.")

def view_period_summary():
    """ Handles the UI logic for viewing a summary of a given period (e.g., last week, last month) """
    print("\n--- PERIOD SUMMARY ---")
    print("1. Last 7 Days")
    print("2. Last 30 Days")
    print("3. Last 90 Days")
    print("4. Custom Period")
    choice = get_valid_int("\nSelect a period: ")
    if choice < 1 or choice > 4:
        print("\nInvalid selection. Number out of range.")
        return

    if choice == 1:
        start_date = date.today() - timedelta(days=7)
        end_date = date.today()
    elif choice == 2:
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
    elif choice == 3:
        start_date = date.today() - timedelta(days=90)
        end_date = date.today()
    else:
        start_date = input("\nEnter start date (YYYY-MM-DD) or press ENTER for today's date: ")
        if start_date == "":
            start_date = date.today()
        end_date = input("\nEnter end date (YYYY-MM-DD) or press ENTER for today's date: ")
        if end_date == "":
            end_date = date.today()

    period_summary = crud.get_period_summary(start_date, end_date)
    if not period_summary:
        print("\nNo period summary available for the given timeframe.")
        return

    print(f"\n--- MACRO AVERAGES FROM {start_date} TO {end_date} ---")
    print(f"Total Days: {period_summary['total_days']}")
    print(f"Average Calories: {period_summary['avg_calories']:.2f} cal")
    print(f"Average Protein: {period_summary['avg_protein']:.2f}g")
    print(f"Average Carbs: {period_summary['avg_carbs']:.2f}g")
    print(f"Average Fat: {period_summary['avg_fat']:.2f}g")


def view_visualizations():
    """ Handles the UI logic for visualizing data """
    print("\n--- VISUALIZATIONS ---")
    print("1. Calorie Trend")

    choice = get_valid_int("\nSelect a visualization: ")
    if choice < 1 or choice > 2:
        print("\nInvalid selection. Number out of range.")
        return

    if choice == 1:
        print("\n--- CALORIE TREND ---")
        start_date = input("\nEnter start date (YYYY-MM-DD) or press ENTER for today's date: ")
        if start_date == "":
            start_date = date.today()
        end_date = input("\nEnter end date (YYYY-MM-DD) or press ENTER for today's date: ")
        if end_date == "":
            end_date = date.today()
        visuals.generate_calorie_trend_chart(start_date, end_date)
