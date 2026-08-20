# 📊 Advanced Log Analyzer CLI & Real-Time Monitor

A robust, enterprise-grade Command Line Interface (CLI) utility for parsing, analyzing, and monitoring application log files in real-time. Built with Python using modern architectural patterns (Dependency Injection, Data Classes, Generators), static typing, unit testing with high coverage, and automated CI/CD pipelines.

## 🚀 Key Features
- **Modular Architecture:** Clean separation of concerns (`Reader`, `Parser`, `Analyzer`).
- **Memory Efficient:** Uses Python Generators (`yield`) to process massive files (e.g., 50GB+) line-by-line with constant RAM usage.
- **Advanced Parsing:** Utilizes Regular Expressions (Regex) with named capture groups to extract data securely.
- **On-the-Fly Decompression:** Transparently reads `.gz` compressed log archives without extracting them to disk.
- **Data Masking (Anonymization):** Automatically masks sensitive dynamic data (like IPv4 addresses) using `re.sub` to accurately group similar error messages via `collections.Counter`.
- **Real-Time Streaming (`tail -f` mode):** Supports `--follow` flag to monitor log file growth in real-time.
- **Rich Terminal UI:** Displays dynamic, color-coded tables using the `rich` library.
- **Containerized:** Fully packaged with Docker, optimizing layer caching for fast builds.
- **CI/CD Pipeline:** Automated testing (`pytest`), static type checking (`mypy`), and test coverage reporting via GitHub Actions.

## 🛠️ Tech Stack
- **Language:** Python 3.11+
- **Core Modules:** `pathlib`, `re`, `gzip`, `collections`, `dataclasses`, `argparse`, `logging`
- **UI & Formatting:** `rich`
- **Testing & Quality:** `pytest`, `pytest-cov`, `mypy`
- **Infrastructure:** Docker, GitHub Actions

---

## 📦 Installation & Setup

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/Pifagor4k/log-analyzer.git
   cd log-analyzer
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

---

## 💻 Usage

### 1. Analyze a Static Log File
Run the analyzer on a standard log file and output a JSON report:
```bash
python3 main.py --log test_log.log --out report.json
```

### 2. Analyze a Compressed `.gz` Archive
```bash
python3 main.py --log test_log.log.gz
```

### 3. Real-Time Monitoring (`--follow` mode)
Stream and visualize log updates live in your terminal with a Rich dashboard:
```bash
python3 main.py --log test_log.log --follow
```

---

## 🧪 Testing & Code Quality

To ensure code health, run the static type checker and unit tests with coverage:

```bash
# Check types
mypy main.py src/

# Run tests with coverage report
pytest --cov=src test_analyzer.py
```

---

## 🐳 Running via Docker

Build the container image:
```bash
docker build -t log-analyzer .
```

Run the container, mounting your local directory to process logs:
```bash
docker run --rm -v $(pwd):/app log-analyzer --log test_log.log --follow
```