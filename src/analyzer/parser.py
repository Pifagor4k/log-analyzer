import re

from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    level: str
    message: str


class LogParser:
    def __init__(self) -> None:
        self.pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\[(?P<level>[A-Z]+)\]\s(?P<message>.*)$")
        

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parses a raw log line into a LogEntry object.
        Returns None if the line doesn't match the expected format.
        """
        line = line.strip()
        if not line:
            return None

        match = self.pattern.match(line)
        if match:
            return LogEntry(
                level=match.group("level"), 
                message=match.group("message")
            )

        return None


if __name__ == '__main__':
    parser = LogParser()
    print(parser.parse_line("2026-08-18 10:00:01 [INFO] System started successfully"))
    print(parser.parse_line("Some random garbage line"))