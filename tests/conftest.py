"""Test fixtures and configuration."""

from __future__ import annotations

import pytest
from chance import chance


@pytest.fixture
def base_answers() -> dict[str, str]:
    """Return random project answers generated via chance."""
    holder = chance.name()
    return {
        'project_name': 'test-project',
        'project_description': f'A test project by {holder}.',
        'vcs_github_path': f'{holder.lower().replace(" ", "-")}/test-project',
        'copyright_holder_name': holder,
        'copyright_holder_email': chance.email(),
        'project_version': '0.1.0',
        'project_keywords': 'cli, tool, rust',
        'project_package': 'test_project_lib',
        'project_identifier': 'com.test-project.app',
    }
