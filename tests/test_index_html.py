"""Integration tests for index.html.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_index_html_generated(default_project_dir: Path, default_answers: dict[str, str]) -> None:
    """Test that index.html is generated with project_name in title."""
    index = default_project_dir / 'index.html'
    assert index.exists()
    content = index.read_text()
    assert f'<title>{default_answers["project_name"]}</title>' in content
    assert '<div id="root"></div>' in content
    assert '<script type="module" src="/src/main.tsx"></script>' in content
