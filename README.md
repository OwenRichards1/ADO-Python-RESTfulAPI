# Azure DevOps Work Item API - README

## Overview

This project consists of two Python scripts that work together to convert a CSV file into a JSON file and then creates a work item in Azure DevOps with the results.

As it is currently in rudimentary form, the code can be modified to broaden the work item parameters and the number created.

It is important to create and configure the .env file with the correct information before running. The following sections provide information on how to configure the scripts.

### Prerequisites

- An Azure DevOps organization and a project within that organization.
- A personal access token (PAT) with Work Items and Code permissions.
- Python 3.x installed on your system.

The following Python packages installed:

- requests
- json
- os
- dotenv
- base64
- csv (for CSV-JSON.py only)

To install the required packages, run the following command in your terminal/command prompt:

    ```bash
    pip install requests json os dotenv base64 csv
    ```

A CSV file named **sampleInfo.csv** containing the data that needs to be converted to JSON and used to create work items. The file should have the following columns:

- TITLE
- DESCRIPTION

## Running the scripts

To use this script, you need to set the following variables in a .env file:

    ```bash
    # CONFIGURATION SECTION:
    PERSONAL_ACCESS_TOKEN = 'ENTER YOUR PAT HERE'
    
    # PROJECT INFORMATION SECTION:
    ORGANIZATION_URL = 'https://dev.azure.com/ENTER_ORGANIZATION_NAME_HERE'
    PROJECT = 'ENTER_PROJECT_NAME_HERE'

    # NOTE: this can be left blank
    USER_NAME = ''

    # WORK ITEM TYPE SECTION:
    WORK_ITEM_TYPE = 'ENTER WORK ITEM TYPE HERE'

    # WORK ITEM CONFIGURATION SECTION:
    TITLE_TEMPLATE = 'ENTER TITLE TEMPLATE HERE'
    # PRE-POPULATE WORK ITEM DESCRIPTIONS:
    DESCRIPTION_TEMPLATE = 'ENTER DESCRIPTION TEMPLATE HERE'

    # WORK ITEM LOCATION SECTION:
    AREA_PATH = 'ENTER AREA PATH HERE'
    ITERATION_PATH = 'ENTER ITERATION PATH HERE'
    ```

### **CSV-JSON.py**

This script will convert a CSV file into a JSON file. The script reads data from a CSV file and converts the data into a a correct format for JSON. The two files that are required to run the script are:

- **sampleInfo.csv**
- **workItem.json**

The CSV file must be in the same directory as the script but can be named anything, provided the name is changed in the script.

The data is read from the CSV file and is appended to an array. The array is then written to the JSON file. The number of rows that are read from the CSV file can be are changed through user input - this is to ensure that the correct number of work items are created.

## **ADO-WI.py**

This script will create a work item in Azure DevOps using the API. To access the API, the script uses a **personal access token (PAT)** and the organization URL. It also encodes the PAT using base64 encoding, which is a requirement for the API.

The `url` is constructed of concatenating the organization URL and the project name. As a result, the project name is not hard-coded and is read from the .env file. This will ensure it can be changed easily and avoid security issues.

The script reads the data from a JSON file **workitem.json**, which must be in the same directory as the script. The data in the JSON file is used to populate the fields of the work item.

The script uses the `requests` package to send a POST request to the API. The request is sent to the URL that was constructed earlier. The request is sent with the following parameters. One field represents a configurable parameter of a work item, to add more simple continue the patter but update System. to the field you want to add.

    ```python
    work_item_fields = {
        'fields': {
            "op": "add",
            "path": "/fields/System.Title",
            "from": "null",
            "value": dataTitle
        }
    }
    ```

The response variable contains the response from the API. The response is then printed to the console. If a work item is successfully created, the status code will be 200 and will contain the ID of the work item.

### Conclusion

This project provides a basic example of how to use the Azure DevOps API to create a work item and how to convert a CSV file into a JSON file in Python. You can modify the scripts to meet your specific needs and requirements.

### References - ChatGPT assistance

**ChatGPT**: The code was built with the assistance of ChatGPT for experimentation purposes. Although some sections of the code were provided without issues, it's important to note that the code was not fully functional and required some modifications to work.

This did allow me to save time as I did not have to built the code incrementally.

The use cases I found most useful came through searching and troubleshooting. Instead of going straight to a search engine, I instead used ChatGPT to answer my questions. This was extremely beneficial as it would use the conversation history to provide a more accurate answer.

In certain cases however, I did have to resort to searching for the answer. This was usually due to the fact that the answer was not provided by ChatGPT or the answer was not accurate. In particular, ChatGPT was not able to explain the encoding process for the personal access token and Stack Overflow was able to resolve this instead.

As a side note, ChatGPT proved useful in other ways. For example, I was able to format a JSON output into a more readable format using ChatGPT. b

A copy of the ChatGPT code can withing this repository at **ChatGPT-ADO-CreateWI-using-code.txt**.
