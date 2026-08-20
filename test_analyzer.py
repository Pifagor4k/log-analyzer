import pytest

from src.analyzer.reader import LogReader
from src.analyzer.parser import LogParser
from src.analyzer.core import LogAnalyzer


# === Testing Reader ===

def test_reader_normal_file(tmp_path):
    """Test reading astandard log file line by line."""

    # 1. Arrange
    log_file = tmp_path / "test.log"
    log_file.write_text("line1\nline2\nline3", encoding="utf-8")

    # 2. Act
    reader = LogReader(str(log_file))
    lines = list(reader.read_lines(follow=False))

    # 3. Assert
    assert len(lines) == 3
    assert lines[0] == "line1"


def test_reader_file_not_found():
    """Test that reading a non-existent file triggers a SystemExit."""
    reader = LogReader("this_file_does_not_exitst.log")

    with pytest.raises(SystemExit) as exc_info:
        list(reader.read_lines(follow=False))

    assert exc_info.value.code == 1


# === Testing Parser ===

def test_parser_empty_line():
    """Test that an empty line return None."""
    parser = LogParser()
    entry = parser.parse_line("")

    assert entry is None


def test_parser_valid_line():
    """Test tat a valid log line is parsed correctly."""
    parser = LogParser()
    entry = parser.parse_line("2026-08-18 10:00:00 [ERROR] Disk full")

    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.message == "Disk full"


def test_parser_invalid_line():
    """Test tat aninvalid line returns None."""
    parser = LogParser()
    entry = parser.parse_line("This is complete garbage")

    assert entry is None


# === Testing Analyzer ===

def test_mask_message():
    """Test that IP addresses are correctly masked."""
    analyzer = LogAnalyzer()
    raw_message = "Connection timeout for IP 192.168.1.1 and 10.0.0.5"
    masked = analyzer._mask_message(raw_message)

    assert masked == "Connection timeout for IP <IP> and <IP>"


def test_analyzer_process(tmp_path):
    """Test the full flow: reading, parsing, and counting stats."""

    # 1. Arrange
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "2026-08-18 10:00:00 [ERROR] Connection timeout for IP 192.168.1.1\n"
        "2026-08-18 10:01:00 [ERROR] Connection timeout for IP 10.0.0.5\n"
        "2026-08-18 10:02:00 [INFO] System OK\n",
        encoding="utf-8"
    )

    reader = LogReader(str(log_file))
    parser = LogParser()
    analyzer = LogAnalyzer()

    # 2. Act
    list(analyzer.process(reader, parser))

    # 3. Assert
    assert analyzer.stats["INFO"]["System OK"] == 1
    assert analyzer.stats["ERROR"]["Connection timeout for IP <IP>"] == 2