#Aurthor:Delaksan
#Date: 19/11/2024
#Student ID (IIT): 20240242
#Student ID (UOW): w2120777
#Coursework 1

import csv
from collections import Counter
import math
from pathlib import Path

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

# Function to process CSV data
def process_csv_data(file_name):
    """
    Read and Analyse the CSV file.
    Calculate the various statistics and returns a dictinoary. 
    """
    try:
        #Open the CSV file
        with open(file_name, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            
            # Initialize counters
            total_vehicles = 0
            total_trucks = 0
            total_electric_vehicles = 0
            two_wheeled_vehicles = 0
            bus_north = 0
            vehicle_no_turn = 0
            total_bicycle = 0
            vehicle_over_speed = 0
            vehicle_elm_only = 0
            scooters_elm_only = 0
            vehicle_hanley = 0
            times = [] # List to store vehicle timing
            time_rain = [] # List to store duration of rain
            hanley_times = [] # TIme for hanley highway
            peak_hour_start = 0
            peak_hour_end = 0

            # Iterate through each record in the CSV file
            for line in csv_data:
                total_vehicles += 1 # Count the total vehicles.

                # Extract time and convert to numeric format
                time = line["timeOfDay"]
                hour, minutes, seconds = map(int, time.split(":"))
                time_number = hour + (minutes / 60) + (seconds / 3600)

                # Count vehicles by type
                if line["VehicleType"] == "Truck":
                    total_trucks += 1
                if line["VehicleType"] in ["Bicycle", "Motorcycle", "Scooter"]:
                    two_wheeled_vehicles += 1
                if line["VehicleType"] == "Bicycle":
                    total_bicycle += 1
                if line["VehicleType"] == "Buss" and line["JunctionName"] == "Elm Avenue/Rabbit Road" and line["travel_Direction_out"] == "N":
                    bus_north += 1
                
                # Count electric vehicles
                if line["elctricHybrid"] == "True":
                    total_electric_vehicles += 1

                # Count vehicles that do not turn
                if line["travel_Direction_in"] == line["travel_Direction_out"]:
                    vehicle_no_turn += 1
                
                # Count overspeeding vehicles
                if float(line["VehicleSpeed"]) > float(line["JunctionSpeedLimit"]):
                    vehicle_over_speed += 1

                # Count vehicles and scooters through Elm Avenue
                if line["JunctionName"] == "Elm Avenue/Rabbit Road":
                    vehicle_elm_only += 1
                    if line["VehicleType"] == "Scooter":
                        scooters_elm_only += 1

                # Count vehicles through Hanley Highway
                if line["JunctionName"] == "Hanley Highway/Westway":
                    vehicle_hanley += 1
                    times.append(time_number)

                # Count hours of rain
                if line["Weather_Conditions"] in ["Heavy Rain", "Light Rain"]:
                    time_rain.append(time_number)

            # Calculate statistics
            trucks_percentage = round((total_trucks / total_vehicles) * 100) if total_vehicles else 0
            average_bicycle = round(total_bicycle / 24) if total_bicycle else 0
            average_scooter_elm = round((scooters_elm_only / vehicle_elm_only) * 100) if vehicle_elm_only else 0
            peak_hour_start, peak_hour_end = None, None

            # Fiding peak hour based on vehicle counts.
            if times:
                hour_counter = Counter(map(math.floor, times))  # Count vehicles per hour
                peak_hour, peak_vehicles = hour_counter.most_common(1)[0]  # Get busiest hour and vehicle count
                peak_hour_start = peak_hour
                peak_hour_end = peak_hour + 1

            # Calculating the number of rainy hours.
            hours_rain = len(set(map(math.floor, time_rain)))

            # Returning calculated statistics as an dictionary.
            return {
                "File Name": file_name,
                "Total Vehicles": total_vehicles,
                "Total Trucks": total_trucks,
                "Total Electric Vehicles": total_electric_vehicles,
                "Two-Wheelers": two_wheeled_vehicles,
                "Bus North": bus_north,
                "No-Turn Vehicles": vehicle_no_turn,
                "Truck Percentage": trucks_percentage,
                "Average Bicycles": average_bicycle,
                "Overspeed Vehicles": vehicle_over_speed,
                "Elm Avenue Vehicles": vehicle_elm_only,
                "Hanley Vehicles": vehicle_hanley,
                "Scooters at Elm": average_scooter_elm,
                "hdu":peak_vehicles,
                "Peak hour start": peak_hour_start,
                "Peak hour end": peak_hour_end,
                "Rainy Hours": hours_rain
            }

    except FileNotFoundError: # Error handling if file doesn't exist
        print(f"Error: The file {file_name} does not exist in the current directory.")
        return None

# Display results
def display_outcome(outcome):
    if outcome:
        print("***************************")
        print(f"data file selected is {outcome['File Name']}")
        print("***************************")
        print(f"The total number of vehicles recorded for this date is {outcome['Total Vehicles']}")
        print(f"The total number of trucks recorded for this date is {outcome['Total Trucks']}")
        print(f"The total number of electric vehicles for this date is {outcome['Total Electric Vehicles']}")
        print(f"The total number of two-wheeled vehicles for this date is {outcome['Two-Wheelers']}")
        print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcome['Bus North']}")
        print(f"The total number of Vehicles through both junctions not turning left or right is {outcome['No-Turn Vehicles']}")
        print(f"The percentage of total vehicles recorded that are trucks for this date is {outcome['Truck Percentage']}%")
        print(f"the average number of Bikes per hour for this date is {outcome['Average Bicycles']}\n")
        print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcome['Overspeed Vehicles']}")
        print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcome['Elm Avenue Vehicles']}")
        print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcome['Hanley Vehicles']}")
        print(f"{outcome['Scooters at Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
        print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcome['hdu']}")
        print(f"The most vehicles through Hanley Highway/Westway were recorded between {outcome['Peak hour start']:.2f} and {outcome['Peak hour end']:.2f}")
        print(f"The number of hours of rain for this date is {outcome['Rainy Hours']}")
    else:
        print("No results to display.")
# Save results as a text file.
def save_results_to_file(outcomes, file_name="results.txt"):
    try:
        # Prepare the results content
        content = (
            f"***************************\n"
            f"Data file selected: {outcomes['File Name']}\n"
            f"***************************\n"
            f"The total number of vehicles recorded for this date: {outcomes['Total Vehicles']}\n"
            f"The total number of trucks recorded for this date: {outcomes['Total Trucks']}\n"
            f"The total number of electric vehicles for this date: {outcomes['Total Electric Vehicles']}\n"
            f"The total number of two-wheeled vehicles for this date: {outcomes['Two-Wheelers']}\n"
            f"The total number of buses leaving Elm Avenue/Rabbit Road heading North: {outcomes['Bus North']}\n"
            f"The total number of vehicles not turning left or right: {outcomes['No-Turn Vehicles']}\n"
            f"The percentage of total vehicles recorded that are trucks: {outcomes['Truck Percentage']}%\n"
            f"The average number of bicycles per hour: {outcomes['Average Bicycles']}\n"
            f"The total number of vehicles over the speed limit: {outcomes['Overspeed Vehicles']}\n"
            f"The total number of vehicles recorded through Elm Avenue/Rabbit Road: {outcomes['Elm Avenue Vehicles']}\n"
            f"The total number of vehicles recorded through Hanley Highway/Westway: {outcomes['Hanley Vehicles']}\n"
            f"{outcomes['Scooters at Elm']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n"
            f"The highest number of vehicles in an hour on Hanley Highway/Westway: {outcomes['hdu']}\n"
            f"The peak hour for Hanley Highway/Westway: {outcomes['Peak hour start']}:00 - {outcomes['Peak hour end']}:00\n"
            f"The number of hours of rain for this date: {outcomes['Rainy Hours']}\n"
        )

        """ Write the calculated statistics to the file.
        if results exists as a file the append or else create a new file.
        """
        result_file = Path(file_name)
        mode = "a" if result_file.exists() else "w"
        with open(result_file, mode) as file:
            file.write(content + "\n\n")

        print(f"Results have been saved to {file_name}.")
    except KeyError as e:
        print(f"Error: Missing key {e} in the outcomes. Please verify the data processing logic.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def validate_continue_input():
    while True:
        user_input = input("Do you want to run the program again with a new date? (Y/N): ").strip().upper()
        if user_input in ['Y', 'N']:
            return user_input
        else:
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.")


# Main program
if __name__ == "__main__":
    while True:
        date = validate_date_input()
        file_name = f"traffic_data{date.replace('/', '')}.csv"
        outcome = process_csv_data(file_name)
        display_outcome(outcome)
        if outcome:
            save_results_to_file(outcome)
        
        # Ask if the user wants to run the program again
        continue_input = validate_continue_input()
        if continue_input == 'N':
            print("Thank you for using the traffic data analysis program. Goodbye!")
            break
