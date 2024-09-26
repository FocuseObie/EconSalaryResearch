import csv
import json

def extract_salary_data(data_dict):
    # Navigate the correct path to extract salary data
    all_real_values = data_dict["vqlCmdResponse"]["layoutStatus"]["applicationPresModel"]["dataDictionary"]["dataSegments"]["1"]["dataColumns"][1]["dataValues"]
    
    # Filter out percentage values (if applicable)
        # Filter out percentage values (which are between -1 and 1), keeping only salary values
    salary_data = [value for value in all_real_values if value > 1 or value < -1]
    
    return salary_data



def extract_program_name(data_dict):
    # Navigate the correct path to extract program name
    program_name = data_dict["vqlCmdResponse"]["layoutStatus"]["applicationPresModel"]["dataDictionary"]["dataSegments"]["1"]["dataColumns"][2]["dataValues"][0]
    return program_name



def write_salary_data_to_csv(salary_values, program_name, file_path):
    # Define possible labels
    cohorts = ["2016-2018", "2013-2015", "2010-2012", "2007-2009", "2004-2006", "2001-2003"]
    years_out_list = ["1 year out", "5 years out", "10 years out"]
    percentiles = ["75th percentile", "50th percentile", "25th percentile"]
    
    # Generate labels dynamically based on the available data length
    labels = []
    index = 0
    while len(labels) < len(salary_values):
        years_out = years_out_list[(index // (len(cohorts) * len(percentiles))) % len(years_out_list)]
        percentile = percentiles[(index // len(cohorts)) % len(percentiles)]
        cohort = cohorts[index % len(cohorts)]
        labels.append((cohort, years_out, percentile))
        index += 1

    # Open the CSV file to write
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Program", "Cohort", "Years Out", "Percentile", "Salary ($)"])
        
        # Write the data rows
        for i, (cohort, years_out, percentile) in enumerate(labels):
            writer.writerow([program_name, cohort, years_out, percentile, f"${salary_values[i]:,.2f}"])
    
# Load the JSON content (adjust the path to your file location)
with open(r"C:\Users\H3AD\Desktop\saved_json_response_1.json", 'r') as f:
    json_data = json.load(f)

# Extract salary data
salary_values = extract_salary_data(json_data)

# Extract the program name
program_name = extract_program_name(json_data)

# Write the salary data to a CSV file
csv_file_path = r"C:\Users\H3AD\Desktop\salary_data3.csv"
write_salary_data_to_csv(salary_values, program_name, csv_file_path)

print(f"Salary data has been written to {csv_file_path}")
