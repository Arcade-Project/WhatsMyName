from wmn import globals


def export_csv(timestamp):
    file_name = f"wmn-{globals.username}-{timestamp}.csv"
    with open(file_name, "w") as file:
        for line in globals.csv_list:
            file.write(line + "\n")
