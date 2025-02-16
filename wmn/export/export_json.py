import json
from wmn import globals


def export_json(timestamp):

    json_output = {
        "found": {},
        "not found": {},
        "false positive": {},
        "error": {},
    }
    for line in globals.csv_list:
        raw_line = [part.strip().strip('"')
                    for part in line.split(",")]
        if len(raw_line) >= 3:
            category = raw_line[0]
            name = raw_line[1]
            url = raw_line[2]

            if category in json_output:
                json_output[category][name] = url
    file_name = f"wmn-{globals.username}-{timestamp}.json"
    with open(file_name, "w") as file:
        file.write(json.dumps(
            json_output, ensure_ascii=True, indent=2))
