total_url = 0
current_state = 0
timeout = 2  # in second
max_concurrent_threads = 60

print_not_founds = False
print_false_positives = False
print_error = False
export_csv = False
export_json = False
username = ""

csv_list = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}
