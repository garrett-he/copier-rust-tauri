"""Integration tests for index.html.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_index_html_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that index.html is generated with project_name in title."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    index = result.project_dir / 'index.html'
    assert index.exists()
    content = index.read_text()
    assert f'<title>{base_answers["project_name"]}</title>' in content
    assert '<div id="app"></div>' in content
    assert '<script type="module" src="/src/main.ts"></script>' in content
