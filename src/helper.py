"""Helper functions for app.py."""

from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st
from streamlit.logger import get_logger

if TYPE_CHECKING:
    from logging import Logger

    from streamlit.navigation.page import StreamlitPage


def filename_to_title(path: Path | str) -> str:
    """
    Convert filename to title.

    remove leading "rxx_" and replace "_"
    """
    if isinstance(path, str):
        path = Path(path)
    name = path.stem[4:].replace("_", " ").title()
    return name


def create_navigation_menu() -> str:
    """Create and populate navigation menu."""
    lst: list[StreamlitPage] = []
    for p in sorted(Path("src/reports").glob("*.py")):
        f = p.stem
        if f.startswith("_"):
            continue
        t = filename_to_title(p)
        lst.append(st.Page(page=f"reports/{f}.py", title=t))  # type: ignore
    pg = st.navigation(lst, expanded=True)  # type: ignore
    pg.run()
    return pg.url_path


def get_logger_from_filename(file: str) -> Logger:
    """Return logger using filename name."""
    return get_logger(Path(file).stem)


def include_javascript() -> None:
    """Include a custom JavaScript."""
    import streamlit.components.v1 as components  # noqa: PLC0415

    components.html(
        """
<script>
</script>
    """,
        height=0,
    )
