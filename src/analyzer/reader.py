import logging
import sys
import gzip
import time

from pathlib import Path
from typing import Generator


class LogReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)


    def read_lines(self, follow: bool = False) -> Generator[str, None, None]:
        try:
            is_gzipped = self.file_path.suffix == ".gz"
            opener = gzip.open if is_gzipped else open

            with opener(self.file_path, 'rt', encoding='utf-8') as file:
                while True:
                    line = file.readline()

                    if not line: # End of file reached
                        if follow:
                            time.sleep(0.1) # Wait for new data
                            continue
                        else:
                            break # Normal mode: just exit

                    yield line.strip()
        
        except FileNotFoundError:
            logging.error(f"Error: File '{self.file_path}' not found.")
            sys.exit(1)

        except PermissionError:
            logging.error(f"Error: Permission denied for '{self.file_path}'.")
            sys.exit(1)


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = LogReader('/home/keylogin/myprojects/log-analyzer/test_log.log')

    for line in parser.read_lines():
        print(line)
        pass
    logging.info(f"Report successfully saved!")