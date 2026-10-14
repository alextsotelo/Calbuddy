import pandas as pd
from db_connection import get_db_connection
""" This module contains the CRUD operations for the database. It uses the get_db_connection function to establish a connection to the database."""

# MEAL FUNCTIONS

def add_meal(name, calories, protein_g, carbs_g, fat_g): # Inserts a new meal into the database
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """INSERT INTO meals (name, calories, protein_g, carbs_g, fat_g)
            VALUES(%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            calories = VALUES(calories),
            protein_g = VALUES(protein_g),
            carbs_g = VALUES(carbs_g),
            fat_g = VALUES(fat_g),
            is_active = TRUE"""
    values = (name, calories, protein_g, carbs_g, fat_g)

    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error adding meal: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def deactivate_meal(name): # "Deactivates" (soft deletes) a meal from the database
    connection = get_db_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    query = """UPDATE meals 
                SET is_active = FALSE
                WHERE name = %s"""
    values = (name,)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            print("No meal found with the given name.")
            return False
        return True
    except Exception as e:
        print(f"Error deactivating meal: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_meal_by_name(name): # Returns a meal's data by its name'
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    query = """ SELECT *
                FROM meals
                WHERE name = %s"""
    values = (name,)

    try:
        cursor.execute(query, values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error fetching meal by name: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_active_meals(raise_on_error=False): # Returns all active meals
    connection = get_db_connection()
    if connection is None:
        if raise_on_error:
            raise RuntimeError("Could not connect to the database.")
        return []
    cursor = connection.cursor(dictionary=True)
    query = """ SELECT *
                FROM meals
                WHERE is_active = TRUE"""
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        if raise_on_error:
            raise RuntimeError("Could not retrieve active meals.") from e
        print(f"Error fetching active meals: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_meal(current_name, new_name, calories, protein_g, carbs_g, fat_g): # Updates a meal's data
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """ UPDATE meals
                SET name = %s, calories = %s, protein_g = %s, carbs_g = %s, fat_g = %s
                WHERE name = %s
                """
    values = (new_name, calories, protein_g, carbs_g, fat_g, current_name)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            print("No meal found with the given name.")
            return False
        return True
    except Exception as e:
        print(f"Error updating meal: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# LOGGING MEALS FUNCTIONS

def log_meal(meal_id, servings, log_date, meal_time): # Logs a meal
    connection = get_db_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    query = """INSERT INTO log_entries (meal_id, servings, log_date, meal_time)
                VALUES (%s, %s, %s, %s)"""
    values = (meal_id, servings, log_date, meal_time)

    try:
        cursor.execute(query, values)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error logging meal: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def get_log_for_date(log_date): # Return all log entries for a given day
    connection = get_db_connection()
    if connection is None:
        return []
    cursor = connection.cursor(dictionary=True)
    query = """ SELECT l.id, m.name, l.meal_time, l.servings,
                (m.calories * l.servings) as total_calories,
                (m.protein_g * l.servings) as total_protein,
                (m.carbs_g * l.servings) as total_carbs,
                (m.fat_g * l.servings) as total_fat
                FROM log_entries as l
                JOIN meals as m
                ON l.meal_id = m.id
                WHERE l.log_date = %s
                ORDER BY l.meal_time"""
    values = (log_date,)

    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching log entries for date: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_period_summary(start_date, end_date): # Returns a summary of all total macros for a given interval
    connection = get_db_connection()
    if connection is None:
        return None
    cursor = connection.cursor(dictionary=True)

    query = """SELECT COUNT(DISTINCT l.log_date) AS total_days,
                      COALESCE(SUM(m.calories * l.servings) / NULLIF(COUNT(DISTINCT l.log_date), 0),0) as avg_calories, 
                      COALESCE(SUM(m.protein_g * l.servings) / NULLIF(COUNT(DISTINCT l.log_date), 0), 0) as avg_protein, 
                      COALESCE(SUM(m.carbs_g * l.servings) / NULLIF(COUNT(DISTINCT l.log_date), 0), 0) as avg_carbs,
                      COALESCE(SUM(m.fat_g * l.servings) / NULLIF(COUNT(DISTINCT l.log_date), 0), 0) as avg_fat
                FROM log_entries as l
                JOIN meals as m
                ON l.meal_id = m.id
                WHERE l.log_date BETWEEN %s and %s"""

    values = (start_date, end_date)

    try:
        cursor.execute(query, values)
        results = cursor.fetchone()
        return results
    except Exception as e:
        print(f"Error fetching period summary: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_log_entry(entry_id): # Deletes a log entry
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """DELETE FROM log_entries 
                WHERE log_entries.id = %s"""
    values = (entry_id,)
    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            print("No log entry found with the given ID.")
            return False
        return True
    except Exception as e:
        print(f"Error deleting log entry: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


""" FUNCTIONS FOR DATA VISUALIZATION """

def get_log_dataframe(start_date, end_date):
    """ Extracts raw SQL data and returns it as a Pandas DataFrame"""
    connection = get_db_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    query = """ SELECT l.log_date,
                SUM(m.calories * l.servings) as total_calories,
                SUM(m.protein_g * l.servings) as total_protein,
                SUM(m.carbs_g * l.servings) as total_carbs,
                SUM(m.fat_g * l.servings) as total_fat
                FROM log_entries as l
                JOIN meals m ON l.meal_id = m.id
                WHERE l.log_date BETWEEN %s AND %s
                GROUP BY l.log_date
                ORDER BY l.log_date"""
    values = (start_date, end_date)

    try:
        cursor.execute(query, values)
        results = cursor.fetchall()
        return pd.DataFrame(results)
    except Exception as e:
        print(f"Error fetching log data: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

