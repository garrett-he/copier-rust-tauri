"""Integration tests for package.json.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_package_json_generated(default_project_dir: Path, default_answers: dict[str, str]) -> None:
    """Test that package.json is generated with variable substitutions."""
    pkg = default_project_dir / 'package.json'
    assert pkg.exists()
    content = pkg.read_text()

    assert f'"name": "{default_answers["project_name"]}"' in content
    assert f'"version": "{default_answers["project_version"]}"' in content
    assert f'"description": "{default_answers["project_description"]}"' in content
    assert f'"name": "{default_answers["copyright_holder_name"]}"' in content
    assert f'"email": "{default_answers["copyright_holder_email"]}"' in content
    assert default_answers['vcs_github_path'] in content
    assert f'"license": "{default_answers["copyright_license"]}"' in content
