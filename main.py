import csv
import os

def create_dummy_csv(filename, data):
    """Creates a dummy CSV file with the given data."""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Created dummy file: {filename}")

def compare_csv_files(file1_path, file2_path, key_column):
    """
    Compares two CSV files based on a key column and reports differences.
    This simulates a 'smart diff' for structured data, unlike line-by-line tools.
    """
    data1 = {}
    data2 = {}

    # Read file 1 into a dictionary keyed by the key_column
    with open(file1_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data1[row[key_column]] = row

    # Read file 2 into a dictionary keyed by the key_column
    with open(file2_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data2[row[key_column]] = row

    # Find added, deleted, and modified records
    added = []
    deleted = []
    modified = []

    # Check for deleted and modified records
    for key, row1 in data1.items():
        if key not in data2:
            deleted.append(row1) # Record present in file1 but not file2
        else:
            row2 = data2[key]
            if row1 != row2: # Record present in both, but content differs
                changes = {}
                for field, value1 in row1.items():
                    value2 = row2.get(field)
                    if value1 != value2:
                        changes[field] = {'old': value1, 'new': value2}
                modified.append({'key': key, 'changes': changes})

    # Check for added records
    for key, row2 in data2.items():
        if key not in data1:
            added.append(row2) # Record present in file2 but not file1

    return {'added': added, 'deleted': deleted, 'modified': modified}

if __name__ == "__main__":
    file1_name = "data_original.csv"
    file2_name = "data_modified.csv"
    key_col = "id"

    # --- Create dummy data files --- 
    # These files simulate large structured datasets that need comparison.
    original_data = [
        {'id': 'A001', 'name': 'Alice', 'city': 'New York', 'age': '30'},
        {'id': 'A002', 'name': 'Bob', 'city': 'London', 'age': '25'},
        {'id': 'A003', 'name': 'Charlie', 'city': 'Paris', 'age': '35'},
        {'id': 'A004', 'name': 'David', 'city': 'Tokyo', 'age': '40'},
    ]

    modified_data = [
        {'id': 'A001', 'name': 'Alice Smith', 'city': 'New York', 'age': '31'}, # Modified name and age
        {'id': 'A002', 'name': 'Bob', 'city': 'London', 'age': '25'},           # Unchanged
        {'id': 'A005', 'name': 'Eve', 'city': 'Berlin', 'age': '28'},           # Added new record
        {'id': 'A004', 'name': 'David', 'city': 'Kyoto', 'age': '40'},          # Modified city
    ]

    create_dummy_csv(file1_name, original_data)
    create_dummy_csv(file2_name, modified_data)

    print("\n--- Performing 'Smart Diff' Comparison ---")
    # This comparison goes beyond simple line-by-line diff. 
    # It understands the structure (records identified by 'id')
    # and reports specific field changes, which is the core concept of the article.
    diff_results = compare_csv_files(file1_name, file2_name, key_col)

    print("\n--- Diff Report ---")
    if not any(diff_results.values()):
        print("No differences found.")
    else:
        if diff_results['added']:
            print("\nAdded Records:")
            for record in diff_results['added']:
                print(f"  {record}")
        if diff_results['deleted']:
            print("\nDeleted Records:")
            for record in diff_results['deleted']:
                print(f"  {record}")
        if diff_results['modified']:
            print("\nModified Records:")
            for item in diff_results['modified']:
                print(f"  Record ID: {item['key']}")
                for field, change in item['changes'].items():
                    print(f"    Field '{field}': '{change['old']}' -> '{change['new']}'")

    # --- Clean up dummy files ---
    print("\n--- Cleaning up dummy files ---")
    os.remove(file1_name)
    os.remove(file2_name)
    print(f"Removed {file1_name} and {file2_name}")
