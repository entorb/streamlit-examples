"""Test: Open all Pages/Reports."""

# ruff: noqa: D100 D103 E402 F841 INP001 N802 PLR2004 S101

import sys
import warnings
from pathlib import Path

from streamlit.testing.v1 import AppTest

warnings.filterwarnings("ignore", message=".*streamlit.runtime.scriptrunner_utils.*")

sys.path.insert(0, (Path(__file__).parent.parent / "src").as_posix())
sys.path.insert(0, (Path(__file__).parent.parent / "src" / "reports").as_posix())


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
        t = f[4:]
        print(t)
        _ = init_and_run(p)


def test_single_page() -> None:
    """Open specific page and set input value."""
    p = Path("src/reports/r02_inputs.py")
    f = p.stem
    t = f[4:]
    print(t)
    at = init_report(p)
    at.session_state["sel_year"] = 2020
    run_and_assert_no_problems(at, p)
