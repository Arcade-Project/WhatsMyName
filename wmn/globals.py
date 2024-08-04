total_url = 0
current_state = 0
found_counter = 0
timeout = 30  # in second
max_concurrent_threads = 100

print_not_founds = False
print_false_positives = False
print_errors = False
export_csv = False
export_json = False
username = ""

csv_list = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

# Contrib tools
errors_counter = 0
errors_list = []
self_check = False
summary_report = False
