"""Integration tests for license generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie, Result

LICENSE_TYPES = [
    'Apache-2.0',
    'BSD-3-Clause',
    'GPL-3.0-or-later',
    'LGPL-3.0-or-later',
    'MIT',
    'MPL-2.0',
    'Proprietary',
    'Unlicense',
]

# Licenses that are static files (not Jinja2 templates) and don't include copyright information
STATIC_LICENSES = {
    'Apache-2.0',
    'GPL-3.0-or-later',
    'LGPL-3.0-or-later',
    'MPL-2.0',
    'Unlicense',
}

LICENSE_SIGNATURES: dict[str, str] = {
    'MIT': 'MIT License',
    'Apache-2.0': 'Apache License',
    'BSD-3-Clause': 'BSD 3-Clause License',
    'GPL-3.0-or-later': 'GNU GENERAL PUBLIC LICENSE',
    'LGPL-3.0-or-later': 'GNU LESSER GENERAL PUBLIC LICENSE',
    'MPL-2.0': 'Mozilla Public License Version 2.0',
    'Proprietary': 'Proprietary Software License',
    'Unlicense': 'This is free and unencumbered software released into the public domain.',
}

LICENSE_README: dict[str, str] = {
    'MIT': 'MIT License',
    'Apache-2.0': 'Apache License',
    'BSD-3-Clause': 'BSD 3-Clause License',
    'GPL-3.0-or-later': 'GNU General Public License',
    'LGPL-3.0-or-later': 'GNU Lesser General Public License',
    'MPL-2.0': 'Mozilla Public License 2.0',
    'Proprietary': 'Proprietary Software License',
    'Unlicense': 'This is free and unencumbered software released into the public domain',
}


def verify_license(result: Result, answers: dict[str, str]) -> None:
    """Verify the license file was generated correctly."""
    license_type = answers['copyright_license']
    assert result.project_dir

    # Find LICENSE file (may have different names)
    license_files = list(result.project_dir.glob('LICENSE*')) + list(result.project_dir.glob('UNLICENSE*'))
    assert len(license_files) > 0
    license_path = license_files[0]

    # Verify correct license type was generated
    assert license_path.exists()
    content = license_path.read_text()
    signature = LICENSE_SIGNATURES[license_type]
    assert signature in content

    # Verify LICENSE file contains expected copyright information.
    if license_type not in STATIC_LICENSES:
        year = answers['copyright_year']
        holder_name = answers['copyright_holder_name']
        holder_email = answers['copyright_holder_email']
        assert year in content
        assert holder_name in content
        assert holder_email in content
    else:
        assert content.strip()


def verify_readme(result: Result, answers: dict[str, str]) -> None:
    """Verify the README file was generated correctly."""
    license_type = answers['copyright_license']
    assert result.project_dir

    # Find README.md file
    readme_path = result.project_dir / 'README.md'
    assert readme_path.exists()
    readme = readme_path.read_text()

    assert readme.startswith(f'# {answers["project_name"]}\n')
    assert answers['project_description'] in readme
    assert LICENSE_README[license_type] in readme

    if license_type != 'Unlicense':
        assert f'img.shields.io/badge/license-{license_type}-blue' in readme
        assert 'Copyright (C)' in readme
        assert answers['copyright_holder_name'] in readme
        assert answers['copyright_holder_email'] in readme
        assert answers['copyright_year'] in readme


@pytest.mark.parametrize('license_type', LICENSE_TYPES)
def test_license_generation(
    copie: Copie,
    default_answers: dict[str, str],
    license_type: str,
) -> None:
    """Test that project generates correct LICENSE for each license type."""
    answers = default_answers.copy()
    answers['copyright_license'] = license_type
    result = copie.copy(extra_answers=answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None
    assert result.project_dir.is_dir()

    verify_license(result, answers)
    verify_readme(result, answers)
