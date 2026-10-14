import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import crud

def generate_calorie_trend_chart(start_date, end_date):
    df = crud.get_log_dataframe(start_date, end_date)

    if df is None or df.empty:
        return False

    # Draw plot
    plt.figure(figsize=(10,6))
    plt.plot(df['log_date'], df['total_calories'], color='red', label="Daily Calories")

    # Format
    plt.title(f"Calorie Trend from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Total Calories")
    # mplt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    #               ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    plt.legend()
    plt.grid(True)

    # Save it
    filename = "calorie_trend.png"
    plt.savefig(filename)
    plt.close()

    return filename
