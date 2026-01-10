"""Test fixtures and configuration."""

from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

import pytest
from chance import chance

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_copie.plugin import Copie, Result


@pytest.fixture(scope='session')
def default_answers() -> dict[str, str]:
    """Session-scoped default answers."""
    project_name = f'{chance.word().lower()}-{chance.word().lower()}'

    return {
        'copyright_license': chance.pickone(
            [
                'Apache-2.0',
                'BSD-3-Clause',
                'GPL-3.0-or-later',
                'LGPL-3.0-or-later',
                'MIT',
                'MPL-2.0',
                'Proprietary',
                'Unlicense',
            ]
        ),
        'copyright_year': str(randint(2000, 2025)),
        'copyright_holder_name': chance.name(),
        'copyright_holder_email': chance.email(),
        'project_name': project_name,
        'project_description': chance.sentence(words=5),
        'project_version': f'{randint(0, 9)}.{randint(0, 9)}.{randint(0, 9)}',
        'project_keywords': f'{chance.word()},{chance.word()},{chance.word()}',
        'project_package': f'{project_name.replace("-", "_")}_lib',
        'project_identifier': f'com.{project_name}.app',
        'vcs_github_path': f'{chance.word().lower()}/{chance.word().lower()}',
    }


@pytest.fixture(scope='session')
def default_result(
    copie_session: Copie,
    default_answers: dict[str, str],
) -> Result:
    """Generate the project once per session with default answers."""
    result = copie_session.copy(extra_answers=default_answers)
    assert result.exit_code == 0, f'Project generation failed: {result.exception}'
    assert result.exception is None
    assert result.project_dir is not None
    assert result.project_dir.is_dir()
    return result


@pytest.fixture(scope='session')
def default_project_dir(
    default_result: Result,
) -> Path:
    """Return the project directory of the default result."""
    assert default_result.project_dir is not None
    return default_result.project_dir
