from analyzer import LogAnalyzer

def test_analyze_counts_correctly(tmp_path):
    # tmp_path is a built-in pytest fixture. It provides a pathlib.Path object
    # pointing to a unique temporary directory (in /tmp/...)
    
    # 1. Arrange
    log_file = tmp_path / "test_app.log"
    log_file.write_text("[INFO] Start\n[ERROR] Crash\n[ERROR] DB Error\n[WARNING] Slow CPU", encoding="utf-8")
    
    # 2. Act
    analyzer = LogAnalyzer(str(log_file))
    analyzer.analyze()
    
    # 3. Assert
    assert analyzer.stats["INFO"] == 1
    assert analyzer.stats["ERROR"] == 2
    assert analyzer.stats["WARNING"] == 1