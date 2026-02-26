"""Integration tests for Cargo.toml.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_cargo_toml_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that Cargo.toml is generated with variable substitutions."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    cargo = result.project_dir / 'src-tauri' / 'Cargo.toml'
    assert cargo.exists()
    content = cargo.read_text()

    assert f'name = "{base_answers["project_name"]}"' in content
    assert f'version = "{base_answers["project_version"]}"' in content
    assert f'description = "{base_answers["project_description"]}"' in content
    assert f'authors = ["{base_answers["copyright_holder_name"]}"]' in content
    assert f'name = "{base_answers["project_package"]}"' in content


def test_cargo_toml_edition_is_year(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that edition field is rendered from copyright_year."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    cargo = result.project_dir / 'src-tauri' / 'Cargo.toml'
    content = cargo.read_text()
    # edition comes from copyright_year which is an int
    year = result.answers['copyright_year']
    assert f'edition = "{year}"' in content
