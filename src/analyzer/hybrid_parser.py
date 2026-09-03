from typing import Optional
from src.analyzer.parser import LogEntry
from src.analyzer.base_parser import ParserProtocol
from src.analyzer.parser import LogParser
from src.analyzer.ai_parser import AIAgentParser

class HybridParser:
    """
    A hybrid parser that implements a Fallback Strategy.
    It tries the fast Regex parser first, and if it fails, 
    it delegates the line to the AI Agent parser.
    """
    def __init__(self) -> None:
        # Both parsers comply with ParserProtocol
        self.regex_parser: ParserProtocol = LogParser()
        self.ai_parser: ParserProtocol = AIAgentParser()

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Tries to parse a line using standard regex. 
        If it returns None, falls back to the AI agent.
        """
        # Step 1: Try fast standard regex parsing
        entry = self.regex_parser.parse_line(line)
        if entry is not None:
            return entry
        
        # Step 2: Fallback to AI agent for unstructured or custom logs
        return self.ai_parser.parse_line(line)