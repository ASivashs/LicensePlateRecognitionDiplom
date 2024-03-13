import requests
import json
from typing import Final

# URL: Final = "https://app.airops.com/public_api/data_apps/1009/execute"
URL: Final = "https://app.airops.com/public_api/data_apps/5247/execute"
# API_KEY: Final = 'PXzgyDmk4lbkgCIvNw3o2cDa9We4IzBKDntkLOSIIJ4mf1l1GfAJ0GNNKPhf'
API_KEY: Final = 'qBGJQVkh9kIzpZRXNGHwu_N9rCcdJFqOeqlKYboZAfwgHV62jx4wLIGXQVFA'


def ai_query(query: str) -> str:
    def remove_substring(string: str) -> str:
        string = string.replace('DISTINCT', '')
        string = string.replace('public.', '')
        string = string.replace('SQL', '')
        string = string.replace('sql', '')
        string = string.replace('```', '')
        string = string.replace('haidisiz.', '')
        string = string.replace(';', '')
        string = string.replace('\n', ' ')
        return string

    def add_id(string_: str) -> str:
        string_ = string_.split()
        string_.insert(1, 'id,')
        return " ".join(string_)

    # payload = {
    #     "input": {
    #         "provider": ["Postgres"],
    #         "schema": '''{
    #         "table": "license_plate_table_license_plate"
    #         "fields": {
    #                     "license_plate": "",
    #                     "region": "",
    #                     "date_time": "",
    #                     "user_name": "",
    #                     "field_name": "",
    #                     "source": ""
    #                     }
    #         }''',
    #         "question": f'{query}',
    #         "dbt_boolean": [
    #             "false"
    #         ]
    #     }
    # }

    payload = {"input": {
        "provider": ["PostgreSQL"],
        "schema": '''{
            "table": "license_plate_table_license_plate"
            "fields": {
                        "license_plate": "",
                        "region": "",
                        "date_time": "",
                        "user_name": "",
                        "field_name": "",
                        "source": ""
                        }
            }''',
        "question": f'{query}',
        "dbt_boolean": [],
        "model": ["gpt-3.5-turbo-0301"]
    }}

    print(payload)
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    print(payload)
    print(json.dumps(payload, indent=4))
    response = requests.post(URL, json=payload, headers=headers)
    print(response.text)
    query_json: dict[str, str] = response.json()
    print(query_json)
    string_query = add_id(remove_substring(query_json['result']))
    return string_query
