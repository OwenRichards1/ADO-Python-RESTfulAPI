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
# COMBINED_USER_NAME
token_user_name = user_names + ':' + personal_access_token
# ENCODING - UFT - 8
b64_token_user_name = base64.b64encode(token_user_name.encode()).decode()
# PROJECT
project = 'testProject'
# WORK ITEM
work_item_type = 'Task'
# URL
url = f'{organization_url}/{project}/_apis/wit/workitems/${work_item_type}?api-version=6.0'
# print(url)
manualUrl = 'http://dev.azure.com/GTDtestDevOps/testProject/_apis/wit/workitems/$Task?api-version=6.0'

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

# FOR LOOP: POPULATE A VARIABLE WITH THE WORK ITEM FIELDS
for item in data[:1]:

    # SET VARIABLES FROM THE DATA
    dataTitle = data[0]['title']
    # print(dataTitle)

    work_item_fields = {
        'fields': {
            # MANDATORY FIELDS
            "op": "add",
            "path": "/fields/System.Title",
            "from": "null",
            "value": dataTitle
            # CUSTOM FIELDS
        }
    }
    # print(work_item_fields)

    # POST REQUEST
    response = requests.post(manualUrl, headers=headers, json=work_item_fields)
    print(response.status_code)
    print(response.json())

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
        print(response)
        # GET THE URL FROM THE RESPONSE
        work_item_url = response['url']
        print(work_item_url)

        # Send a GET request to retrieve information about the created work item
        # response = requests.get(work_item_url, headers=headers)

        # Print the response status code
        # print(response.status_code)

        # Print the work item information
        # print(response.json())
    else:
        # Print the response status code and error message
        print("ERROR")
        print(response.status_code)
        print(response.text)

# GET ALL WORK ITEMS
# getResponse = requests.get(manualUrl, headers=headers)
# print(getResponse.status_code)
# print(getResponse.json())
# GET A URL FOR A WORK ITEM
# work_item_url = getResponse.headers['System.Id']
# print(work_item_url)
