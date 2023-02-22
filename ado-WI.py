import requests
import json
import os
from dotenv import load_dotenv
import base64

# CONFIGURATION SECTION:

# LOAD .ENV FILE
load_dotenv()
# AUTHENTICATION - LOAD FROM .ENV FILE
organization_url = os.environ['ORGANIZATION_URL']
# PERSONAL ACCESS TOKEN - LOAD FROM .ENV FILE
personal_access_token = os.environ['PERSONAL_ACCESS_TOKEN']
# USER NAME - LOAD FROM .ENV FILE
user_name = os.environ['USER_NAME']
# PROJECT
project = os.environ['PROJECT']
# COMBINED_USER_NAME
token_user_name = user_name + ':' + personal_access_token
# ENCODING - UFT - 8
b64_token_user_name = base64.b64encode(token_user_name.encode()).decode()

# WORK ITEM
type = 'task'
# URL
url = f'{organization_url}/{project}/_apis/wit/workitems/${type}?api-version=6.0'
# print(url)

# HEADERS
headers = {
    'Authorization': 'Basic %s' % b64_token_user_name,
    'Content-Type': 'application/json-patch+json'
}

# Open the JSON file
with open("workitem.json", "r") as jsonFile:
    # Load the JSON data from the file
    data = json.load(jsonFile)
    # print(data)

# WI TEMPLATE ITEMS - USING ENV VARIABLES
titleTemplate = os.environ['TITLE_TEMPLATE']
DescriptionTemplate = os.environ['DESCRIPTION_TEMPLATE']
AreaPathTemplate = 'testProject\\ContentFreshness\\'
IterationPath = 'testProject\\23-YEAR\\03-MAR'

# TAGS - ARRAY
tags = ['content-engagement', 'content-maintenance', 'content-health']

# USER INPUT ABOUT HOW MANY WORK ITEMS TO CREATE
user_input = input("How many work items would you like to create? ")

# FOR LOOP: POPULATE A VARIABLE WITH THE WORK ITEM FIELDS
for item in data[:int(user_input)]:
    work_item_fields = [
        # EACH ITEM REPRESENTS A CONFIGURABLE FIELD OF A WORKITEM - VALUE IS THE VALUE OF THE FIELD
        {
            "op": "add",
            "path": "/fields/System.Title",
            "from": None,
            "value": titleTemplate+item["title"],
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "from": None,
            "value": DescriptionTemplate + " " + item["description"],

        },
        {
            "op": "add",
            "path": "/fields/System.AreaPath",
            "from": None,
            "value": AreaPathTemplate,

        },
        {
            "op": "add",
            "path": "/fields/System.IterationPath",
            "from": None,
            "value": IterationPath,

        },
        {
            "op": "add",
            "path": "/fields/System.Tags",
            "from": None,
            "value": tags[0]+','+tags[1]+','+tags[2],

        }
    ]

    # POST REQUEST
    response = requests.post(url, headers=headers, json=work_item_fields)
    print(response.status_code)
    # print(response.json())

    # RESPONSE - with verification
    # Check if the request was successful
    if response.status_code == 200:
        print("SUCCESS")
        # Get the URL to the created work item from the location header
        # PUT THE JSON INFO INTO A STRING
        response = json.dumps(response.json())
        # print(response)
        # PARSE THE STRING
        response = json.loads(response)
        # print(response)
        # GET THE URL FROM THE RESPONSE
        work_item_url = response['url']
        print(work_item_url)
    else:
        # Print the response status code and error message
        print("ERROR")
        print(response.status_code)
        print(response.text)

# GET ALL WORK ITEMS
# getResponse = requests.get(url, headers=headers)
# print(getResponse.status_code)
# print(getResponse.json())
# GET A URL FOR A WORK ITEM
# work_item_url = getResponse.headers['System.Id']
# print(work_item_url)
