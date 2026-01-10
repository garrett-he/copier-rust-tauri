"""Integration tests for static file generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Result

STATIC_FILES = [
    '.editorconfig',
    '.gitattributes',
    '.gitignore',
]


def test_static_files_generated(default_result: Result) -> None:
    """Test that all static files are generated."""
    assert default_result.project_dir is not None
    for filename in STATIC_FILES:
        filepath = default_result.project_dir / filename
        assert filepath.exists(), f'Static file {filename} not found'
