"""Shared helpers for end-to-end tests."""

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

E2E_TIMEOUT = 300  # seconds; pnpm install can be slow on first run


def _check_tool(name: str) -> bool:
    """Check whether a CLI tool is available in PATH."""
    return shutil.which(name) is not None


def pnpm_install(project_dir: Path) -> None:
    """Run `pnpm install` in the generated project.

    Requires Node.js and pnpm to be installed.
    """
    if not _check_tool('pnpm'):
        raise AssertionError('pnpm is not available in PATH; skipping e2e test')
    result = subprocess.run(
        ['pnpm', 'install'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'pnpm install failed:\n{result.stderr}\n{result.stdout}'


def pnpm_lint(project_dir: Path) -> None:
    """Run `pnpm run lint` in the generated project."""
    if not _check_tool('pnpm'):
        raise AssertionError('pnpm is not available in PATH; skipping e2e test')
    result = subprocess.run(
        ['pnpm', 'run', 'lint'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'pnpm lint failed:\n{result.stderr}\n{result.stdout}'


def pnpm_typecheck(project_dir: Path) -> None:
    """Run `pnpm run typecheck` in the generated project."""
    if not _check_tool('pnpm'):
        raise AssertionError('pnpm is not available in PATH; skipping e2e test')
    result = subprocess.run(
        ['pnpm', 'run', 'typecheck'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'pnpm typecheck failed:\n{result.stderr}\n{result.stdout}'


def cargo_check(project_dir: Path) -> None:
    """Run `cargo check` in the generated project's src-tauri directory."""
    if not _check_tool('cargo'):
        raise AssertionError('cargo is not available in PATH; skipping e2e test')
    result = subprocess.run(
        ['cargo', 'check', '--manifest-path', 'src-tauri/Cargo.toml'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo check failed:\n{result.stderr}\n{result.stdout}'


def cargo_test(project_dir: Path) -> None:
    """Run `cargo test` in the generated project's src-tauri directory."""
    if not _check_tool('cargo'):
        raise AssertionError('cargo is not available in PATH; skipping e2e test')
    result = subprocess.run(
        ['cargo', 'test', '--manifest-path', 'src-tauri/Cargo.toml'],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        timeout=E2E_TIMEOUT,
    )
    assert result.returncode == 0, f'cargo test failed:\n{result.stderr}\n{result.stdout}'
