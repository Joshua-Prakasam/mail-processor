# Mail Processor

## Pre-requisite
 - python >= 3.12.5
 - pdm >= 2.19.3

## Required Steps
 - Create a file `.env` and copy the contents of the file `.env.example`
 - Generate client secret by following the guide [OAuth 2.0 for Installed Applications](https://googleapis.github.io/google-api-python-client/docs/oauth-installed.html) and give the downloaded path of the json to the env variable `CREDENTIALS_JSON_PATH`

 > Note: You can change the values according to your liking.

## Installing dependency

> NOTE: Run all the commands inside the project root directory.

### Verify python version
```bash
python --version
```

It must be `>= 3.12.5`

### Install pdm using pip
```bash
pip install pdm==2.19.3
```

### To setup the application, run
```bash
pdm install
```

## Running the application
Activate the virtual environment

For bash terminal
```bash
source .venv/bin/activate
```

To get help on the program
```bash
python -m mail_processor -h
```

## Usage
 1. Authenticate User
 ```bash
 python -m mail_processor auth
 ```
 2. Synchronized the App with GMail
 ```bash
 python -m mail_processor sync
 ```
 3. To get all the labels
 ```bash
 python -m mail_processor labels
 ```
 4. To execute rules.
 ```bash
 python -m mail_processor rules.json
 ```
 > NOTE: A sample rules.json is present in the `samples` directory 


## Rules json
```json
[
    {
        "name": "Any name for the rule",
        "predicate": "One of `all` or `any`",
        "conditions": [
            {
                "field_name": "One of `From`, `To`, `Subject`, `Body`",
                "predicate": "One of `contains, `does not contain`, `equals`, `does not equal`",
                "value": "Any text"
            },
            {
                "field_name": "Date",
                "predicate": "One of `less than`, `greater than`",
                "value": "Any number",
                "unit": "One of `days`, `months`"
            },
        ],
        "actions": [
            {
                "type": "Mark as Read"
            },
            {
                "type": "Mark as Unread"
            },
            {
                "type": "Move Message",
                "from": "INBOX", // You can get these by running labels command
                "to": "CATEGORY_SOCIAL"
            },
        ]
    },
]
```
> NOTE: For full schema refer `rule_engine/schema.py`