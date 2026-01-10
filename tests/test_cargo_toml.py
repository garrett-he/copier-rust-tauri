"""Integration tests for Cargo.toml.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


def test_cargo_toml_generated(default_answers: dict[str, Any], default_project_dir: Path) -> None:
    """Test that Cargo.toml is generated with variable substitutions."""
    cargo = default_project_dir / 'src-tauri' / 'Cargo.toml'
    assert cargo.exists()
    content = cargo.read_text()

    assert f'name = "{default_answers["project_name"]}"' in content
    assert f'version = "{default_answers["project_version"]}"' in content
    assert f'description = "{default_answers["project_description"]}"' in content
    assert f'authors = ["{default_answers["copyright_holder_name"]}"]' in content
    assert f'name = "{default_answers["project_package"]}"' in content
    assert 'edition = "2021"' in content
