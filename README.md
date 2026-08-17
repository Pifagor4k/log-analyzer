# 📊 Log Analyzer CLI

A robust, containerized Command Line Interface (CLI) utility for analyzing application log files. Built with Python, featuring static typing, unit testing, and CI/CD pipelines.

## 🚀 Features
- Parses logs efficiently (line-by-line memory management).
- Counts log levels (`INFO`, `WARNING`, `ERROR`).
- Outputs statistics to a JSON report.
- Fully containerized with Docker/Podman.
- Continuous Integration via GitHub Actions.

## 🛠️ Usage

### Running Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python3 analyzer.py --log test_log.log --out report.json
```

### Running via Docker
```bash
docker build -t log-analyzer .
docker run --rm -v $(pwd):/app log-analyzer --log test_log.log
```

## 🧪 Testing
To run unit tests and static type checking:
```bash
mypy analyzer.py
pytest
```
