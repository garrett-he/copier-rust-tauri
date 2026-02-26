"""Integration tests for static file generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_copie.plugin import Copie

STATIC_FILES = [
    # Root config files
    '.editorconfig',
    '.gitattributes',
    '.gitignore',
    'biome.json',
    'justfile',
    'pnpm-workspace.yaml',
    'tsconfig.json',
    'vite.config.ts',
    'vitest.config.ts',
    # Public assets
    'public/tauri.svg',
    'public/vite.svg',
    # Src directory
    'src/App.vue',
    'src/assets/vue.svg',
    'src/main.ts',
    'src/router/index.ts',
    'src/types/env.d.ts',
    'src/types/tauri.d.ts',
    'src/views/HomeView.vue',
    # Tests
    'tests/App.test.ts',
    'tests/HomeView.test.ts',
    'tests/__mocks__/fileMock.ts',
    'tests/router.test.ts',
    # Tauri backend
    'src-tauri/.gitignore',
    'src-tauri/capabilities/default.json',
    'src-tauri/rustfmt.toml',
    'src-tauri/src/lib.rs',
    'src-tauri/tarpaulin.toml',
]


def test_static_files_generated(copie: Copie, base_answers: dict[str, str]) -> None:
    """Test that all static files are generated."""
    result = copie.copy(extra_answers=base_answers)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_dir is not None

    for filename in STATIC_FILES:
        filepath = result.project_dir / filename
        assert filepath.exists(), f'Static file {filename} not found'
