import csv
import json

csvFile = open("sampleInfo.csv", "r")
jsonFile = open("workItem.json", "w")

reader = csv.DictReader(csvFile)

# INT & ARRAY
counter = 0
out = []

# LOOP
for row in reader:
    if counter == 10:
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
