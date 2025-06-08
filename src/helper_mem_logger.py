"""Memory Logger Class."""

import csv
import time
import tracemalloc
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper


class MemLogger:
    """Trace and log memory consumption and runtime."""  # noqa: D203

    def __init__(self, logfile: Path) -> None:  # noqa: D107
        self.logfile: Path = logfile
        self.logfile_handle: TextIOWrapper = self.logfile.open("a")
        self.csv_writer = csv.writer(self.logfile_handle, delimiter="\t")
        self.filename: str = ""
        self.function: str = ""
        self.time_start: float = 0
        self.runtime: float = 0
        self.max_mb: float = 0

    def start(self, filename: str, function: str = "") -> None:
        """Start logging."""
        self.filename = filename
        self.function = function
        self.time_start = time.time()
        tracemalloc.start()

    def stop(self) -> None:
        """Stop logging, store the values and log."""
        self.max_mb = round(tracemalloc.get_traced_memory()[0] / 1024 / 1024, 1)
        tracemalloc.stop()
        self.runtime = round(time.time() - self.time_start if self.time_start else 0, 1)
        self.log()

    def log(self) -> None:
        """Write line to logfile."""
        if self.logfile_handle.tell() == 0:
            self.csv_writer.writerow(("date", "file", "function", "runtime", "max_mb"))

        date_str = time.strftime("%Y-%m-%d %H:%M:%S")
        self.csv_writer.writerow(
            (date_str, self.filename, self.function, self.runtime, self.max_mb)
        )
