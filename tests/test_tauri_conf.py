"""Integration tests for tauri.conf.json.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_tauri_conf_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that tauri.conf.json is generated with variable substitutions."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    conf = result.project_dir / 'src-tauri' / 'tauri.conf.json'
    assert conf.exists()
    content = conf.read_text()

    assert f'"productName": "{base_answers["project_name"]}"' in content
    assert f'"version": "{base_answers["project_version"]}"' in content
    assert f'"identifier": "{base_answers["project_identifier"]}"' in content
    assert f'"title": "{base_answers["project_name"]}"' in content
