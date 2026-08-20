import re

from typing import Dict, Generator
from collections import Counter

from src.analyzer.reader import LogReader
from src.analyzer.parser import LogParser


class LogAnalyzer:
    def __init__(self) -> None:
        self.stats: Dict[str, Counter] = {
            "INFO": Counter(), 
            "WARNING": Counter(), 
            "ERROR": Counter()
        }


    def _mask_message(self, message: str) -> str:
        """Masks dynamic data (like IPs) to group similar log messages."""
        
        mod_message = re.sub(
            r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", 
            "<IP>", 
            message
        )
        
        return mod_message


    def process(self, reader: LogReader, parser: LogParser, follow: bool = False) -> Generator[None, None, None]:
        """Processes logs using the injected reader and parser."""
        for line in reader.read_lines(follow=follow):
            entry = parser.parse_line(line)
            if entry and entry.level in self.stats:
                masked_message = self._mask_message(entry.message)
                self.stats[entry.level][masked_message] += 1

                yield