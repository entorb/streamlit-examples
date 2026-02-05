"""Test: Open all Pages/Reports."""

import sys
import warnings
from pathlib import Path

from streamlit.testing.v1 import AppTest

from helper_mem_logger import MemLogger

warnings.filterwarnings("ignore", message=".*streamlit.runtime.scriptrunner_utils.*")

sys.path.insert(0, (Path(__file__).parent.parent / "src").as_posix())
sys.path.insert(0, (Path(__file__).parent.parent / "src" / "reports").as_posix())

MEM_LOGGER = MemLogger(Path(__file__).parent / "mem_logger.tsv")


# helpers
def init_report(path: Path) -> AppTest:
    at = AppTest.from_file(path)
    # setup some session variables
    at.session_state["ENV"] = "DEV"
    return at


def run_and_assert_no_problems(at: AppTest, path: Path) -> None:
    at.run(timeout=60)
    assert not at.exception, path.stem
    assert not at.error, path.stem
    assert not at.warning, path.stem


def init_and_run(path: Path) -> AppTest:
    at = init_report(path)
    run_and_assert_no_problems(at, path)
    return at


# tests
def test_all_pages() -> None:
    """Open all pages and check for errors and warnings."""
    for p in sorted(Path("src/reports").glob("*.py")):
        f = p.stem
        if f.startswith("_"):
            continue
        t = f[4:]
        print(t)
        MEM_LOGGER.start(filename=f)
        _ = init_and_run(p)
        MEM_LOGGER.stop()


def test_single_page() -> None:
    """Open specific page and set input value."""
    p = Path("src/reports/r02_inputs.py")
    f = p.stem
    t = f[4:]
    print(t)
    MEM_LOGGER.start(filename=f)
    at = init_report(p)
    at.session_state["sel_year"] = 2020
    run_and_assert_no_problems(at, p)
    MEM_LOGGER.stop()
