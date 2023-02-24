import csv
import json
import os

# Get a list of all the csv files in the csv-output directory
csv_files = [f for f in os.listdir("csv-output") if f.endswith(".csv")]

# Check if there is at least one csv file in the directory
if len(csv_files) == 0:
    print("No csv files found in csv-output directory")
else:
    # Use the first csv file found in the directory
    csv_filename = os.path.join("csv-output", csv_files[0])

    csvFile = open(csv_filename, "r")
    jsonFile = open("workItem.json", "w")

    reader = csv.DictReader(csvFile)

    # INT & ARRAY
    counter = 0
    out = []

    # ASK FOR USER INPUT TO DETERMINE HOW MANY ROWS TO CONVERT
    user_input = input("How many rows would you like to convert into JSON? ")
    user_input = int(user_input)

    # LOOP
    for row in reader:
        # Adjust the number of rows to be converted
        if counter == user_input:
            break
        formatted_row = {
            "title": row["TITLE"],
            "description": row["DESCRIPTION"],
        }
        out.append(formatted_row)
        counter += 1

    jsonFile.write(json.dumps(out, indent=4))

    csvFile.close()
    jsonFile.close()
