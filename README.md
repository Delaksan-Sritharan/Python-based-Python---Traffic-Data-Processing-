# Traffic Data Analysis

## Author

* Delaksan

## Date

* 19/11/2024

## Student IDs

* IIT: 20240242
* UOW: w2120777

## Coursework

* Coursework 1

## Description

This Python script analyzes traffic data from CSV files. It prompts the user to input a date in DD/MM/YYYY format, validates the input, and then processes the corresponding CSV file (named `traffic_dataDDMMYYYY.csv`). The script calculates various traffic statistics, such as total vehicles, truck percentages, peak hours, and more, and displays the results. It also saves the results to a text file named `results.txt`.

## Features

* **Date Input Validation:** Ensures the entered date is in the correct format and within a valid range, including leap year handling.
* **CSV Data Processing:** Reads traffic data from CSV files and calculates various statistics.
* **Statistical Analysis:** Computes total vehicles, truck percentages, electric vehicle counts, two-wheeler counts, peak hours, and more.
* **Result Display:** Prints the calculated statistics to the console.
* **Result Saving:** Saves the results to a text file (`results.txt`).
* **Continue Option:** Allows the user to run the program again with a new date.
* **Error Handling:** Handles `FileNotFoundError` and other potential exceptions.

## Files

* `traffic_data_analysis.py`: The main Python script.
* `traffic_dataDDMMYYYY.csv`: CSV files containing traffic data (where DDMMYYYY is the date).
* `results.txt`: Text file to store the analysis results.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Place the `traffic_data_analysis.py` script and your CSV data files in the same directory.
3.  Run the script from your terminal: `python traffic_data_analysis.py`
4.  Follow the prompts to enter the date of the traffic data you want to analyze.
5.  The results will be displayed on the console and saved to `results.txt`.
6.  You will be prompted to run the program again with a new date or to exit.

## Code Explanation

### Date Validation

The `validate_date_input()` function:

* Prompts the user to enter the day, month, and year.
* Validates each input to ensure it is an integer within the correct range.
* Checks for leap years to validate the day in February.
* Returns the date in DD/MM/YYYY format.

### CSV Data Processing

The `process_csv_data(file_name)` function:

* Reads the CSV file using `csv.DictReader`.
* Initializes counters for various statistics.
* Iterates through each row in the CSV file, updating the counters.
* Calculates percentages, averages, and peak hours.
* Returns a dictionary containing the calculated statistics.
* Handles FileNotFoundError.

### Result Display and Saving

* `display_outcome(outcome)`: Prints the results to the console.
* `save_results_to_file(outcomes, file_name="results.txt")`: Saves the results to a text file.

### Main Program

The `if __name__ == "__main__":` block:

* Enters a loop that continues until the user chooses to exit.
* Calls `validate_date_input()` to get the date.
* Constructs the CSV file name.
* Calls `process_csv_data()` to analyze the data.
* Calls `display_outcome()` to display the results.
* Calls `save_results_to_file()` to save the results.
* Validates user input for continuing the program.
