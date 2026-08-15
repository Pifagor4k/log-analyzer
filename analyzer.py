import argparse
import logging
import sys
import json
from pathlib import Path

class LogAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.stats = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    def analyze(self):
        """Reads the log file line by line and counts log levels."""
        try:
            # Using context manager to ensure the file is closed properly
            with open(self.file_path, "r", encoding="utf-8") as file:
                # Iterating directly over the file object to save RAM
                for log_line in file:
                    if "[INFO]" in log_line:
                        self.stats["INFO"] += 1
                    elif "[WARNING]" in log_line:
                        self.stats["WARNING"] += 1
                    elif "[ERROR]" in log_line:
                        self.stats["ERROR"] += 1

        except FileNotFoundError:
            logging.error(f"Error: File '{self.file_path}' not found.")
            sys.exit(1)
        except PermissionError:
            logging.error(f"Error: Permission denied for '{self.file_path}'.")
            sys.exit(1)

    def save_report(self, output_path: str):
        """Saves the log statistics to a JSON file."""
        # Using the parameter passed to the method, NOT a hardcoded string
        report_path = Path(output_path)
        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(self.stats, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    parser.add_argument("--log", 
                        type=str, 
                        required=True, 
                        help="path to the log-file")
    parser.add_argument("--out", 
                        type=str, 
                        required=False, 
                        default="report.json", 
                        help="path to the report-file"
                        )
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.log)
    analyzer.analyze()
    analyzer.save_report(args.out)

    logging.info(f"Report successfully saved to {args.out}")