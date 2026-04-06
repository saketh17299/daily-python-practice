"""
Day 1 - Basic Log Analyzer

This script:
1. Reads a log file
2. Counts log levels (INFO, ERROR, WARNING)
3. Extracts error messages
"""

from collections import Counter


def analyze_logs(file_path):
    log_counts = Counter()
    error_messages = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                if "INFO" in line:
                    log_counts["INFO"] += 1
                elif "ERROR" in line:
                    log_counts["ERROR"] += 1
                    error_messages.append(line.strip())
                elif "WARNING" in line:
                    log_counts["WARNING"] += 1

    except FileNotFoundError:
        print("Log file not found.")
        return

    print("\nLog Summary:")
    for level, count in log_counts.items():
        print(f"{level}: {count}")

    print("\nSample Errors:")
    for error in error_messages[:5]:
        print(error)


if __name__ == "__main__":
    file_path = "day1/sample.log"
    analyze_logs(file_path)