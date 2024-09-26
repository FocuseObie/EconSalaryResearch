import requests
import pandas as pd

# URL of the API endpoint
api_url = "https://careers.kelley.iu.edu/api/uconnect/v1/odv/get-data"

# Updated headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Origin': 'https://careers.kelley.iu.edu',
    'Referer': 'https://careers.kelley.iu.edu/outcomes/',
    'User-Agent': 'Mozilla/5.0'
}

# Years to include
years = ["2017", "2018", "2019", "2020", "2021", "2022", "2023"]

# Initialize an empty list to store the data
all_flat_data = []

# Loop over each year
for year in years:
    # Request body with added year in filter and groupBy
    body = {
        "data_queries": {
            "salary_by_major_and_year": [{
                "groupBy": ["major"],  # Group by major
                "select": {"job_salary": ["count", "mean", "median"]},
                "filter": {
                    "first_destination": {"$contains": ["Employed"]},
                    "job_salary": {"$gt": 0},
                    "year": year
                },
                "clean_null_values": False
            }]
        },
        "instance": {
            "id": "default",
            "title": "Default",
            "template": "nace_first_destination"
        },
        "community": "",
        "program": ""
    }

    # Send the POST request
    response = requests.post(api_url, headers=headers, json=body)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        print(data)
        # Extract the salary data
        salary_data = data.get('salary_by_major_and_year', [{}])[0].get('data', [])
        if salary_data:
            # Flatten the JSON structure
            for item in salary_data:
                # Extract and flatten 'key' and 'value' fields
                key_list = item.get('key', [])
                value_dict = item.get('value', {})

                # Extract values
                count = value_dict.get('count', 0)
                mean_salary = value_dict.get('mean', 0)
                median_salary = value_dict.get('median', 0)

                # Flatten the majors, handling nested lists
                def flatten_majors(majors):
                    flat_list = []
                    for major in majors:
                        if isinstance(major, list):
                            flat_list.extend(flatten_majors(major))
                        else:
                            flat_list.append(major)
                    return flat_list

                majors_flat = flatten_majors(key_list)
                majors_str = ", ".join(majors_flat)

                # Append flattened data
                all_flat_data.append({
                    'Major': majors_str,
                    'Year': year,
                    'Count': count,
                    'Mean Salary': mean_salary,
                    'Median Salary': median_salary
                })
        else:
            print(f"No salary data found for year {year}.")
    else:
        print(f"Failed to retrieve data for year {year}. Status code: {response.status_code}")

if all_flat_data:
    # Convert to a DataFrame
    df_salary = pd.DataFrame(all_flat_data)

    # Save to CSV
    df_salary.to_csv('salary_by_major_and_year2.csv', index=False)
    print("Salary data by major and year has been saved to 'salary_by_major_and_year.csv'")
else:
    print("No salary data found.")
