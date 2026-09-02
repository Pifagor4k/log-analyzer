import logging
from typing import Optional
from src.analyzer.parser import LogEntry

class AIAgentParser:
    def __init__(self) -> None:
        logging.info("Initializing AI Agent Parser (Mock Engine)...")

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Fallback parser powered by AI. 
        Triggers only when standard regex fails.
        """
        line = line.strip()
        if not line:
            return None
        
        upper_line = line.upper()
        if "CRITICAL" in upper_line or "FATAL" in upper_line:
            return LogEntry(level="ERROR", message=f"[AI-Parsed] {line}")

        return None