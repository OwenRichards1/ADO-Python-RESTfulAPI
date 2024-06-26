import itertools
import requests
import csv
import json
import os
import base64
from dotenv import load_dotenv

# LOAD .ENV FILE
load_dotenv()
# print("Tags array loaded.")

# AUTHENTICATION - LOAD FROM .ENV FILE
organization_url = os.environ['ORGANIZATION_URL']
personal_access_token = os.environ['PERSONAL_ACCESS_TOKEN']
user_name = os.environ['USER_NAME']
project = os.environ['PROJECT']
token_user_name = user_name + ':' + personal_access_token
b64_token_user_name = base64.b64encode(token_user_name.encode()).decode()

# WI TEMPLATE ITEMS - USING ENV VARIABLES
titleTemplate = os.environ['TITLE_TEMPLATE']
descriptionTemplate = os.environ['DESCRIPTION_TEMPLATE']
#descriptionTemplate2 = os.environ['DESCRIPTION_TEMPLATE2']
areaPathTemplate = os.environ['AREA_PATH_TEMPLATE']
iterationPathTemplate = os.environ['ITERATION_PATH_TEMPLATE']
userTemplate = os.environ['USER_TEMPLATE']
userEmailTemplate = os.environ['USER_EMAIL_TEMPLATE']
typeTemplate = os.environ['WORK_ITEM_TYPE']

# LINE BREAK (USED FOR FORMATTING)
line_space = " - "

# TAGS - ARRAY
tags = ['test-tag']
# tags = ['Azure AD PowerShell references', 'content-maintenance', 'content-health']
# tags = ['AzureAD-PS-Migration']

# HEADERS
headers = {
    'Authorization': 'Basic %s' % b64_token_user_name,
    'Content-Type': 'application/json-patch+json'
}
# print("Headers loaded.")

def read_work_item_fields(file_name):
    with open(file_name, "r") as jsonFile:
        data = json.load(jsonFile)
        # print("Work item fields read.")
        return data
        

def create_work_item(url, headers, work_item_fields):
    response = requests.post(url, headers=headers, json=work_item_fields)
    print(response.status_code)
    if response.status_code == 200 or response.status_code == 201:
        print("SUCCESS")
        response = json.dumps(response.json())
        response = json.loads(response)
        work_item_url = response['url']
        print(work_item_url)
    else:
        print("ERROR")
        print(response.status_code)
        print(response.text)

def get_csv_files():
    # Get a list of all the csv files in the csv-input directory
    return [f for f in os.listdir("csv-input") if f.endswith(".csv")]

def read_csv_file(filename):
    with open(filename, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        field_names = reader.fieldnames
        out = []
        for row in reader:
            # Check if all values in the row are empty (blank)
            if all(value == '' for value in row.values()):
                # Skip empty lines
                continue  
            formatted_row = {field: row[field] for field in field_names}
            out.append(formatted_row)
        return out


def write_json_file(data, filename):
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(data, indent=4))

# def get_groups(items):
#     return (items['FilePath'],items['ms.author'], items['Repo'])

def convert_csv_to_json():
    # Check if there is at least one csv file in the directory
    csv_files = get_csv_files()
    if len(csv_files) == 0:
        raise Exception("No csv files found in csv-input directory")
    else:
        # Use the first csv file found in the directory
        csv_filename = os.path.join("csv-input", csv_files[0])
        json_filename = os.path.join("json-output", "workItem.json")
        # grouped_json_filename = os.path.join("json-output", "grouped_workItem.json")
        data = read_csv_file(csv_filename)
        # grouped_items = itertools.groupby(data, get_groups)

        # groups=[]
        # for  (file, author, repo), items in grouped_items:
        #     groups.append({"FilePath": file, "ms.author": author, "Repo":repo, "items":list(items)})

        write_json_file(data, json_filename)
        # write_json_file(groups, grouped_json_filename)

        print("CSV file converted to JSON and saved to json-output directory.")


def main():

    # CONVERT CSV TO JSON
    convert_csv_to_json()
   
    # CONFIGURATION SECTION - READ FROM .ENV FILE:
    type = typeTemplate
    url = f'{organization_url}/{project}/_apis/wit/workitems/${type}?api-version=6.0'

    # Open the JSON file
    work_item_fields = read_work_item_fields("json-output/workItem.json")
    # work_item_fields = read_work_item_fields("json-output/grouped_workItem.json")

    # USER INPUT ABOUT HOW MANY WORK ITEMS TO CREATE
    while True:
        user_input = input("How many work items would you like to create (type 'ALL' for all work items)? ")
        print("User input:", user_input)
        if user_input.upper() == 'ALL':
            user_input = len(work_item_fields)
            break
        else:
            try:
                user_input = int(user_input)
                break
            except ValueError:
                print("Please type 'ALL' (ensure it is typed exactly as you see it).")
     

    # FOR LOOP: POPULATE A VARIABLE WITH THE WORK ITEM FIELDS
    for item in work_item_fields[:int(user_input)]:
    
        # description_items = []
        # work_item_header = '<p>% s </p><p><b>Repo:</b> % s </p><p><b>File path:</b> % s </p>'% (descriptionTemplate,item["Repo"],item["FilePath"])
        # description_items.append(work_item_header)

        # for i in item["items"]:
        #     description_item = '<p><b>Match:</b> % s </p><p><b>Context:</b> % s</p>'% ( i["Match"], i["Context"])
        #     description_items.append(description_item)
        # description = '<br>'.join(description_items)
        # assigned_to ='% s@% s' % (item["ms.author"],"microsoft.com")

        items = [
            # EACH ITEM REPRESENTS A CONFIGURABLE FIELD OF A WORKITEM - VALUE IS THE VALUE OF THE FIELD
            {
                "op": "add",
                "path": "/fields/System.Title",
                "from": None,
                # CONFIGURE USING YOUR CSV COLUMN HEADERS
                "value": titleTemplate + item["NAME"],
                # "value": titleTemplate + item["FilePath"],

            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "from": None,
                # CONFIGURE USING YOUR CSV COLUMN HEADERS
                "value": descriptionTemplate + item["HEALTHSCORE"] + item["LINKS"]
                #"value": descriptionTemplate + '\n\nMatch:' + item["Match"] + '\n\nContext:' + item["Context"],
                #"value": '<p>% s </p><p><b>Repo:</b> % s </p><p><b>Match:</b> % s </p><p><b>Context:</b> % s</p>'% (descriptionTemplate,item["Repo"], item["Match"], item["Context"]), 
            },
            {
                "op": "add",
                "path": "/fields/System.AreaPath",
                "from": None,
                # CONFIGURE USING YOUR CSV COLUMN HEADERS
                "value": areaPathTemplate,

            },
            {
                "op": "add",
                "path": "/fields/System.IterationPath",
                "from": None,
                # CONFIGURE USING YOUR CSV COLUMN HEADERS
                "value": iterationPathTemplate,

            },
            {
                "op": "add",
                "path": "/fields/System.Tags",
                "from": None,
                # CONFIGURE USING YOUR CSV COLUMN HEADERS
                "value": tags[0],
            },
            # CONFIGURE FURTHER FIELDS HERE - e.g.:
            # {
            #     "op": "add",
            #     "path": "/fields/System.ENTER_FIELD_NAME_HERE",
            #     "from": None,
            #     # CONFIGURE USING YOUR CSV COLUMN HEADERS
            #     "value": tags[0],
            # },
            # UNCOMMENT THE FOLLOWING SECTION TO ASSIGN WORK ITEMS TO A USER
            # {
            #     "op": "add",
            #     "path": "/fields/System.AssignedTo",
            #     "from": None,
            #     # "value": userTemplate,
            #     # "value": assigned_to,
            #     "value": item["ALIAS"] + userEmailTemplate,
            # }
        ]
        # POST REQUEST
        create_work_item(url, headers, items)

if __name__ == "__main__":
    main()