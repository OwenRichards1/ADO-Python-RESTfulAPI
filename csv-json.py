import csv
import json

csvFile = open("sampleInfo.csv", "r")
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
