"""Integration tests for build.rs.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_build_rs_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that build.rs is generated with tauri_build call."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    build = result.project_dir / 'src-tauri' / 'build.rs'
    assert build.exists()
    content = build.read_text()
    assert 'tauri_build::build()' in content
