"""Helper functions for app.py."""

from logging import Logger
from pathlib import Path

import streamlit as st
from streamlit.logger import get_logger


def create_navigation_menu() -> None:
    """Create and populate navigation menu."""
    lst = []
    for p in sorted(Path("src/reports").glob("*.py")):
        f = p.stem
        if f.startswith("_"):
            continue
        t = f[4:]
        lst.append(st.Page(page=f"reports/{f}.py", title=t))
    pg = st.navigation(lst, expanded=True)
    pg.run()


def get_logger_from_filename(file: str) -> Logger:
    """Return logger using filename name."""
    return get_logger(Path(file).stem)


def include_javascript() -> None:
    """Include a custom JavaScript."""
    import streamlit.components.v1 as components

    components.html(
        """
<script>
</script>
    """,
        height=0,
    )
