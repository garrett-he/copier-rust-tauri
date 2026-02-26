"""Integration tests for main.rs.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_main_rs_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that main.rs is generated with project_package call."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    main_rs = result.project_dir / 'src-tauri' / 'src' / 'main.rs'
    assert main_rs.exists()
    content = main_rs.read_text()
    assert f'{base_answers["project_package"]}::run()' in content
    assert 'fn main()' in content
