import requests
import json

# Define the URL of the API endpoint MUST CHANGE WITH NEW SESSIONS !!!!!!!!!!!!!!!!!!!
url = "https://tableau.bi.iu.edu/vizql/t/prd/w/PSEO/v/TrendsAcrossTime/sessions/6B068AF0F3544007AEF847773C32D00D-3:1/commands/tabdoc/categorical-filter-by-index"

# Define the headers for the request
headers = {
    "Host": "tableau.bi.iu.edu",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/javascript",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://tableau.bi.iu.edu/t/prd/views/PSEO/TrendsAcrossTime",
    "Content-Type": "multipart/form-data; boundary=twL5SEGl",
    "X-Tsi-Active-Tab": "Trends Across Time",
    "X-Tableau-Version": "2023.1",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://tableau.bi.iu.edu",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "tableau_locale=en",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0"
}

# Function to save the JSON response
def save_json_response(json_data, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"JSON data successfully saved to {output_file_path}")

# Loop through indices 0 to 26
for index in range(29):
    # Update the data payload with the current index
    data = (
        "--twL5SEGl\r\n"
        "Content-Disposition: form-data; name=\"visualIdPresModel\"\r\n\r\n"
        "{\"worksheet\":\"Summary, CIP Program Family Selection\",\"dashboard\":\"Trends Across Time\"}\r\n"
        "--twL5SEGl\r\n"
        "Content-Disposition: form-data; name=\"globalFieldName\"\r\n\r\n"
        "[federated.0rrz07507tj0de10k4qp31dezgqn].[Cip Family Label Set]\r\n"
        "--twL5SEGl\r\n"
        "Content-Disposition: form-data; name=\"membershipTarget\"\r\n\r\n"
        "set\r\n"
        "--twL5SEGl\r\n"
        "Content-Disposition: form-data; name=\"filterIndices\"\r\n\r\n"
        f"[{index}]\r\n"  # Adjust index based on desired data
        "--twL5SEGl\r\n"
        "Content-Disposition: form-data; name=\"filterUpdateType\"\r\n\r\n"
        "filter-replace\r\n"
        "--twL5SEGl--\r\n"
    )

    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Attempt to parse the response as JSON
            json_response = response.json()
            
            # Define a dynamic file name based on the index
            output_file_path = rf'C:\Users\H3AD\Desktop\saved_json_response_{index}.json'
            
            # Save the JSON response to a file
            save_json_response(json_response, output_file_path)
        
        except json.JSONDecodeError:
            print(f"Failed to decode JSON at index {index}. The response might not be in JSON format.")
    else:
        print(f"Failed to retrieve data for index {index}. Status code: {response.status_code}")
