from typing import Protocol, Optional
from src.analyzer.parser import LogEntry

class ParserProtocol(Protocol):
    """
    A structural interface (protocol) for all log parsers.
    Any parser class must implement the parse_line method to comply with this protocol.
    """
    def parse_line(self, line: str) -> Optional[LogEntry]:
        ...