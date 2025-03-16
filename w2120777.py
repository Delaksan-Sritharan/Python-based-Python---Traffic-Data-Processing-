#Aurthor:Delaksan
#Date: 10/12/2024
#Student ID (IIT): 20240242
#Student ID (UOW): w2120777
#Coursework 1 D&E Part
import csv
from collections import Counter
import math
from pathlib import Path
import tkinter as tk #Create the GUI
from tkinter import filedialog #For file selection dialog

def prepare_histogram_data(file_name):
    '''
    Read CSV file for hourly vehicle count for two location
    '''
    #Intitalize counter for both locations within 24 hours.
    hourly_counts = {"Elm": [0] * 24, "Hanley": [0] * 24}
    try:
        #open and read csv file
        with open(file_name, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            #Read each row in the CSV file
            for line in csv_data:
                hour = int(line["timeOfDay"].split(":")[0])
                if line["JunctionName"] == "Elm Avenue/Rabbit Road":
                    hourly_counts["Elm"][hour] += 1
                elif line["JunctionName"] == "Hanley Highway/Westway":
                    hourly_counts["Hanley"][hour] += 1

    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")

    return hourly_counts

# Validation for date and month and year
def validate_date_input():
    """
    Validating date input in the format of DD/MM/YYYY. 
    Validating date, month and year are within the range and handling leap year input.
    """
    def is_leap_year(year):
        # Function to check if a year is a leap year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    while True:
        # Input day and validate it.
        while True:
            try:
                day = int(input("Please enter the day of the survey in the format dd: "))
                if 1 <= day <= 31:  #Day range validation
                    break
                else:
                    print("Out of range - values must be in the range 1 and 31.")
            except ValueError:
                print("Integer required for the day.")

        # Input and validate month
        while True:
            try:
                month = int(input("Please enter the month of the survey in the format MM: "))
                if 1 <= month <= 12: #Month range validation
                    break
                else:
                    print("Out of range - values must be in the range 1 to 12.")
            except ValueError:
                print("Integer required for the month.")

        # Input and validate year
        while True:
            try:
                year = int(input("Please enter the year of the survey in the format YYYY: "))
                if 2000 <= year <= 2024: #Year range validation
                    break
                else:
                    print("Out of range - values must range from 2000 to 2024.")
            except ValueError:
                print("Integer required for the year.")

        # Validate the day based on the month and year
        max_days = 31  # Default for months with 31 days
        if month == 2:  # Edge case for February
            max_days = 29 if is_leap_year(year) else 28
        elif month in {4, 6, 9, 11}:  # Months with 30 days
            max_days = 30

        if not (1 <= day <= max_days):
            print(f"Invalid day for month {month} in year {year}. Please enter a value between 1 and {max_days}.")
            continue  # Go back to re-enter day, month, and year as needed

        # If all validations pass, return the date
        return f"{day:02d}/{month:02d}/{year:04d}"

class HistogramApp:
    # Class used to represent GUI application for vehicle data
    def __init__(self, master, data, date):
        master.title("Histogram")  # GUI Window title
        self.master = master
        self.data = data
        self.date = date 
        #Assigning dimensions of the canvas.
        self.canvas_width = 800
        self.canvas_height = 400
        self.margin = 60  # Adjusted margin for better alignment

        # Create canvas
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Draw histogram
        self.draw_histogram()

    def draw_histogram(self):
        # Title with date.
        self.canvas.create_text(
            40, 20, anchor="w",  # Position at top-left
            text=f"Histogram of Vehicle Frequency Per Hour ({self.date})", font=("Arial", 14, "bold"), fill="black"
        )

        # Data
        hours = list(range(24))
        elm_data = self.data.get("Elm", [0] * 24)
        hanley_data = self.data.get("Hanley", [0] * 24)

        max_value = max(max(elm_data), max(hanley_data))
        bar_width = 9  # width of each bar.
        spacing = 2  # space bewteen bars.
        total_width = len(hours) * (2 * bar_width + spacing + 10)
        x_offset = (self.canvas_width - total_width) // 2 - 20  # Shifted slightly to the left
        bar_gap = 5  # Space between pairs of bars
        #edge handling for no data.
        if max_value == 0:
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2,
                text="No Data Available", font=("Arial", 12, "bold"), fill="red"
            )
            return

        # Axes
        x_axis_start = self.margin + x_offset - (bar_gap // 2)  # Starting at the first bar
        x_axis_end = self.margin + x_offset + len(hours) * (2 * bar_width + spacing + bar_gap) - (bar_gap // 2)  # Ending at last bar
        # X-Axis line
        self.canvas.create_line(
            x_axis_start, self.canvas_height - self.margin,
            x_axis_end, self.canvas_height - self.margin,
            width=2, fill="black"  # Black X-axis line
        )

        # Axis Labels
        self.canvas.create_text(
            self.canvas_width // 2, self.canvas_height - 20, text="Hours 00:00 to 24:00", font=("Arial", 10), fill="black"
        )

        # Draw Bars for each hour
        for i, hour in enumerate(hours):
            x = self.margin + x_offset + i * (2 * bar_width + spacing + bar_gap)  # Adjust x-position for pairs
            elm_height = (elm_data[hour] / max_value) * (self.canvas_height - 2 * self.margin)
            hanley_height = (hanley_data[hour] / max_value) * (self.canvas_height - 2 * self.margin)

            # Elm Avenue Bars
            self.canvas.create_rectangle(
                x, self.canvas_height - self.margin - elm_height,
                x + bar_width, self.canvas_height - self.margin,
                fill="SeaGreen1", outline="gray69"
            )
            # Value on top of Elm bar
            self.canvas.create_text(
                x + bar_width // 2, self.canvas_height - self.margin - elm_height - 10,
                text=str(elm_data[hour]), font=("Arial", 8), fill="SeaGreen1"
            )
            # Hanley highway Bars
            self.canvas.create_rectangle(
                x + bar_width, self.canvas_height - self.margin - hanley_height,
                x + 2 * bar_width + spacing, self.canvas_height - self.margin,
                fill="salmon1", outline="gray69"
            )
            # Value on top of Hanley bar
            self.canvas.create_text(
                x + bar_width + bar_width // 2 + spacing, self.canvas_height - self.margin - hanley_height - 10,
                text=str(hanley_data[hour]), font=("Arial", 8), fill="salmon1"
            )

            # Hour Labels belwo the bars.
            self.canvas.create_text(
                x + bar_width + spacing // 2, self.canvas_height - self.margin + 6,
                text=f"{hour:02}", font=("Arial", 8), fill="black"
            )

        # Legend
        legend_x = 40
        legend_y = 30
        #Elm avenue legend 
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 12, legend_y + 12, fill="SeaGreen1", outline="black")
        self.canvas.create_text(legend_x + 20, legend_y + 6, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10), fill="black")
        #Hanley highway legend
        self.canvas.create_rectangle(legend_x, legend_y + 20, legend_x + 12, legend_y + 32, fill="salmon1", outline="black")
        self.canvas.create_text(legend_x + 20, legend_y + 26, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10), fill="black")


#Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None #Initialize the processor with empty data

    def load_csv_file(self, file_path): # Load and process CSV data.
        data = {"Elm": [0] * 24, "Hanley": [0] * 24}
        date = "Unknown"

        with open(file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            date = reader.fieldnames[0] #Get date from the header
            for row in reader:
                hour = int(row["Hour"])
                data["Elm"][hour] = int(row["Elm"])
                data["Hanley"][hour] = int(row["Hanley"])

        return data, date

    def clear_previous_data(self): # Clear the current loaded data.
        self.current_data = None

    def handle_user_interaction(self): # Allow the user to select file and view each histograms.
        while True: #Open file selection dialog
            file_path = filedialog.askopenfilename(title="Select a CSV File", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                break
            #Load and process selected file
            data, date = self.load_csv_file(file_path)

            self.current_data = data
            #Create and display histogram.
            root = tk.Tk()
            app = HistogramApp(root, data, date)
            root.mainloop()

            self.clear_previous_data()

def validate_continue_input(): #Validate use input and continue the program depending on user choice.
    while True:
        user_input = input("Do you want to run the program again with a new date? (Y/N): ").strip().upper()
        if user_input in ['Y', 'N']:
            return user_input
        else:
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.")

# Main program
def main(): #Initialize and run the processor for handling multiple files
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()

if __name__ == "__main__":
    while True:
        date = validate_date_input() #Get validated date input
        file_name = f"traffic_data{date.replace('/', '')}.csv" #get the file from the date
        outcome = prepare_histogram_data(file_name)

        if outcome:
            # Prepare data for histogram and display
            hourly_data = prepare_histogram_data(file_name)
            root = tk.Tk()
            app = HistogramApp(root, hourly_data, date)
            root.mainloop()

        # Ask if the user wants to run the program again
        continue_input = validate_continue_input()
        if continue_input == 'N':
            print("Thank you for using the traffic data analysis program. Goodbye!")
            break

    # Allow optional execution of MultiCSVProcessor
    main()
