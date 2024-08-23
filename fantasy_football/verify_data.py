import csv

def filter_rows(filename):
    rows = []
    with open(filename, "r") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            if len(row) == 50:
                rows.append(row)
    return rows

def write_rows(filename, rows):
    with open(filename, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(rows)

def check_errors(filename):
    error_count = 0
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if len(row) != 50:
                print(f"Line {i+1}: {len(row)} columns (expected 50)")
                error_count += 1
    print(f"Total lines with errors: {error_count}")

def main():
    filename = "data.csv"
    filtered_rows = filter_rows(filename)
    write_rows(filename, filtered_rows)
    check_errors(filename)

if __name__ == "__main__":
    main()