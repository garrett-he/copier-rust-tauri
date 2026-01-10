"""Integration tests for main.rs.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_main_rs_generated(default_project_dir: Path, default_answers: dict[str, str]) -> None:
    """Test that main.rs is generated with project_package call."""
    main_rs = default_project_dir / 'src-tauri' / 'src' / 'main.rs'
    assert main_rs.exists()
    content = main_rs.read_text()
    assert f'{default_answers["project_package"]}::run(name)' in content
    assert 'fn main()' in content
