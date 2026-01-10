"""End-to-end tests for the generated Tauri project."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._helpers import cargo_check, cargo_test, pnpm_install, pnpm_lint, pnpm_typecheck

if TYPE_CHECKING:
    from pytest_copie.plugin import Result


def test_generated_project_builds_and_passes_checks(
    default_result: Result,
) -> None:
    """Generate a project and verify it installs, lints, typechecks, and compiles."""
    assert default_result.project_dir is not None
    pnpm_install(default_result.project_dir)
    pnpm_lint(default_result.project_dir)
    pnpm_typecheck(default_result.project_dir)
    cargo_check(default_result.project_dir)
    cargo_test(default_result.project_dir)
