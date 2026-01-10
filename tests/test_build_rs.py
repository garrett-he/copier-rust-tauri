"""Integration tests for build.rs.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_build_rs_generated(default_project_dir: Path) -> None:
    """Test that build.rs is generated with tauri_build call."""
    build = default_project_dir / 'src-tauri' / 'build.rs'
    assert build.exists()
    content = build.read_text()
    assert 'tauri_build::build()' in content
