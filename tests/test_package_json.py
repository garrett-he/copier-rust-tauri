"""Integration tests for package.json.jinja rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie


def test_package_json_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that package.json is generated with variable substitutions."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    pkg = result.project_dir / 'package.json'
    assert pkg.exists()
    content = pkg.read_text()

    assert f'"name": "{base_answers["project_name"]}"' in content
    assert f'"version": "{base_answers["project_version"]}"' in content
    assert f'"description": "{base_answers["project_description"]}"' in content
    assert f'"name": "{base_answers["copyright_holder_name"]}"' in content
    assert f'"email": "{base_answers["copyright_holder_email"]}"' in content
    assert base_answers['vcs_github_path'] in content
    assert f'"license": "{base_answers.get("copyright_license", "MIT")}"' in content


def test_package_json_keywords_rendered(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that keywords are split and rendered as JSON array."""
    answers = {**base_answers, 'project_keywords': 'cli,tool,rust'}
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.project_dir is not None

    pkg = result.project_dir / 'package.json'
    content = pkg.read_text()
    assert '"cli",' in content
    assert '"tool",' in content
    assert '"rust"' in content
