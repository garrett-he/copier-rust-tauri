"""Integration tests for tauri.conf.json.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_tauri_conf_generated(default_project_dir: Path, default_answers: dict[str, str]) -> None:
    """Test that tauri.conf.json is generated with variable substitutions."""
    conf = default_project_dir / 'src-tauri' / 'tauri.conf.json'
    assert conf.exists()
    content = conf.read_text()

    assert f'"productName": "{default_answers["project_name"]}"' in content
    assert f'"version": "{default_answers["project_version"]}"' in content
    assert f'"identifier": "{default_answers["project_identifier"]}"' in content
    assert f'"title": "{default_answers["project_name"]}"' in content
