import argparse
import logging
import json

from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.live import Live

from src.analyzer.reader import LogReader
from src.analyzer.parser import LogParser
from src.analyzer.core import LogAnalyzer


def save_report(stats: dict, output_path: str) -> None:
    """Saves the log statistics to a JSON file."""
    report_path = Path(output_path)
    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)


def generate_table(stats: dict) -> Table:
    """Generates a beautiful colored table with the Top 3 messages per level."""
    
    # Creating table
    table = Table(title="📊 Log Analysis Top Errors")
    table.add_column("Level", style="cyan", no_wrap=True)
    table.add_column("Message", style="magenta")
    table.add_column("Count", justify="right", style="green")

    for level, counter in stats.items():
        mc_messages = counter.most_common(3)

        for message, count in mc_messages:
            table.add_row(level, message, str(count))
    
    return table


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
    parser.add_argument("--follow", 
                        action="store_true", 
                        help="follow lof file growth (like tail -f)")
    args = parser.parse_args()


    reader = LogReader(args.log)
    parser_obj = LogParser()
    analyzer = LogAnalyzer()


    if args.follow:
        with Live(generate_table(analyzer.stats), refresh_per_second=4) as live:
            for _ in analyzer.process(reader, parser_obj, follow=True):
                live.update(generate_table(analyzer.stats))

    else:
        list(analyzer.process(reader, parser_obj, follow=False))

        console = Console()
        console.print(generate_table(analyzer.stats))

        save_report(analyzer.stats, args.out)
        logging.info(f"Report successfully saved to {args.out}")