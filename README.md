# Azure DevOps Work Item API - README

## Overview

This project is a Python script that reads data from a CSV file and uses the Azure DevOps API to create a work item in Azure DevOps with the results.

It is important to create and configure the .env file with the correct information before running. The following sections provide information on how to configure the script.

### Prerequisites

- An Azure DevOps organization and access to a project within that organization.
- A personal access token (PAT) with Work Items and Code permissions.
- Python 3.x installed on your system.

The following Python packages installed:

- requests
- json
- os
- dotenv
- base64
- csv

To install the required packages, run the following command in your terminal/command prompt:

    ```bash
    pip install requests json os dotenv base64 csv
    ```

A CSV file saved in /csv-input. It can be named anything but if more than one file exists - the scrip will not run. The script will also run the first file it finds in the directory.

**NOTE:** each row in the CSV file will be converted into a JSON object

## Running the scripts

To use this script, you need to create and set the following variables in a .env file:

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

## **ADO-WI.py**

This script will first convert a CSV file into a JSON file. The script reads data from a CSV file and converts the data into a correct format for JSON. The data is then written to a JSON file and will be created in /json-output named the following:

- **workItem.json**.

**NOTE:** The JSON file will be overwritten each time the script is run.

This script will create a work item in Azure DevOps using the API. To access the API, the script uses a **personal access token (PAT)** and the organization URL. It also encodes the PAT using base64 encoding, which is a requirement for the API.

The `url` is constructed of concatenating the organization URL and the project name. As a result, the project name is not hard-coded and is read from the .env file. This will ensure it can be changed easily and avoid security issues.

### Configuring the For Loop

Before running the script, make sure to configure the for loop in *ado-WI.py* correctly to read your JSON file. The loop is responsible for creating work items based on the data extracted from your JSON file.

Here's an explanation of each item in the loop:

- `for item in work_item_fields[:int(user_input)]`: - This line loops through the list of work item fields, up to the specified number of work items.
- `items` - This variable is a list of dictionaries representing the configurable fields of a work item.
- `op` - This field specifies the operation to be performed on the field, in this case, adding a new field.
- `path` - This field specifies the path of the field to be added, such as /fields/System.Title.
- `value` - This field specifies the value of the field to be added, such as titleTemplate + item["FilePath"]. Make sure to refer to the values used in the **workitem.json** file.
- `create_work_item(url, headers, items)` - This line sends a POST request to create a new work item using the specified url, headers, and items.

Make sure to modify the values of the fields in the items list according to your JSON file. You can refer to the json-output/workItem.json file to configure the value field.

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

### NOTE

Please ignore the placeholder.txt files, it is only there to ensure the json-output folder is created when the script is run.

### Conclusion

The response variable contains the response from the API. The response is then printed to the console. If a work item is successfully created, the status code will be 200 and will contain the ID of the work item.

This project provides a basic example of how to use the Azure DevOps API to create a work item and how to convert a CSV file into a JSON file in Python. You can modify the scripts to meet your specific needs and requirements.
