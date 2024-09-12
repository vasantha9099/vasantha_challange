import json
import re
from datetime import datetime

def is_rfc3339_date(date_string):
    """Check if a string is in RFC3339 format."""
    try:
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def rfc3339_to_epoch(date_string):
    """Convert RFC3339 formatted date string to Unix Epoch time."""
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp())

def transform_json(data):
    """Transform the input JSON data according to the criteria."""
    result = {}
    for key, val in data.items():
        key = key.strip()  # Sanitize the key by removing leading and trailing whitespace
        if not key:
            continue  # Skip empty keys

        if isinstance(val, dict):
            for dtype, dval in val.items():
                if dtype == "S":
                    dval = dval.strip()
                    if dval:
                        if is_rfc3339_date(dval):
                            result[key] = rfc3339_to_epoch(dval)
                        else:
                            result[key] = dval
                elif dtype == "N":
                    try:
                        dval = float(dval.strip())
                        result[key] = dval
                    except ValueError:
                        continue
                elif dtype == "BOOL":
                    dval = dval.strip().lower()
                    if dval in ["1", "t", "true"]:
                        result[key] = True
                    elif dval in ["0", "f", "false"]:
                        result[key] = False
                    else:
                        continue
                elif dtype == "NULL":
                    dval = dval.strip().lower()
                    if dval in ["1", "t", "true"]:
                        result[key] = None
                    elif dval in ["0", "f", "false"]:
                        continue
                elif dtype == "L":
                    if isinstance(dval, list):
                        transformed_list = []
                        for elem in dval:
                            transformed_elem = transform_json({"0": elem}).get("0")
                            if transformed_elem is not None:
                                transformed_list.append(transformed_elem)
                        if transformed_list:
                            result[key] = transformed_list
                elif dtype == "M":
                    nested_map = transform_json(dval)
                    if nested_map:
                        result[key] = nested_map
        elif isinstance(val, list):
            result[key] = [transform_json({"0": elem}).get("0") for elem in val if elem]
        elif val:
            result[key] = val

    return result

if __name__ == "__main__":
    # Sample input JSON
    input_json = {
        "number_1": { "N": "1.50" },
        "string_1": { "S": "784498 " },
        "string_2": { "S": "2014-07-16T20:55:46Z" },
        "map_1": {
            "M": {
                "bool_1": { "BOOL": "truthy" },
                "null_1": { "NULL": "true" },
                "list_1": {
                    "L": [
                        { "S": "" },
                        { "N": "011" },
                        { "N": "5215s" },
                        { "BOOL": "f" },
                        { "NULL": "0" }
                    ]
                }
            }
        },
        "list_2": { "L": "noop" },
        "list_3": { "L": [ "noop" ] },
        "": { "S": "noop" }
    }

    # Transform JSON and print the output
    transformed_output = transform_json(input_json)
    print(json.dumps([transformed_output], indent=2))
