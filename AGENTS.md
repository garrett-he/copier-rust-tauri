# AGENTS.md — copier-rust-tauri Project Context for AI Coding Assistants

## Identity

copier-rust-tauri is a [Copier](https://copier.readthedocs.io/) template that
scaffolds modern Rust + Tauri desktop applications. It collects user input
through interactive questions, then renders a complete project via Jinja2
templates.

## Architecture

```text
User answers ──► copier.yml + copier/questions/*.yml
                         │
                         ▼
              Jinja2 context (answers + extensions)
                         │
                         ▼
              template/*.jinja ──► generated project on disk
```

- **Questions** (`copier/questions/`) define what the user is asked. Copier
  aggregates them when processing `copier.yml`.
- **Extensions** (`copier/extensions/`) inject extra context (`ContextUpdater`
  reads git config).
- **Template** (`template/`) is the output skeleton. `_subdirectory: template`
  in settings tells Copier where it lives. Conditional files use
  `{% if copyright_license == 'MIT' %}LICENSE{% endif %}.jinja` naming.

## Key conventions

- Line width: 120 (code & Markdown via rumdl). Indent: 4 spaces. Quotes:
  single. Line endings: LF.
- Type annotations everywhere — pyrefly runs in `strict` preset.
- Docstring style: Google (`lint.pydocstyle.convention = "google"`).
- Imports: `from __future__ import annotations` in every Python file.
- `TYPE_CHECKING` guard for imports only needed by static analysis.

## File map (non-obvious paths)

| Path | Role |
|------|------|
| `copier.yml` | Root config; `!include` directives pull in sub-configs |
| `copier/settings.yml` | `_min_copier_version`, `_subdirectory`, `_jinja_extensions`, `_tasks` |
| `copier/extensions/context.py` | `ContextHook` subclass → injects `git_user_name`, `git_user_email` |
| `copier/questions/project.yml` | Project metadata: name, package, identifier, version, description, keywords |
| `copier/questions/copyright.yml` | License selection and copyright holder info |
| `copier/questions/vcs.yml` | GitHub repository path |
| `template/package.json.jinja` | Frontend config; uses `project_keywords` split for keywords array |
| `template/src-tauri/Cargo.toml.jinja` | Rust backend config; `project_package` as lib name |
| `template/src-tauri/tauri.conf.json.jinja` | Tauri app config; `project_identifier` for bundle ID |
| `template/src-tauri/src/main.rs.jinja` | Rust entrypoint; calls `{{ project_package }}::run(name)` |
| `tests/conftest.py` | `default_answers` (session-scoped random data), `default_result`, `default_project_dir` |
| `tests/e2e/_helpers.py` | Shared `pnpm install` / `pnpm lint` / `cargo check` runners for e2e tests |

## Common commands (via just)

```text
just check            # ruff + ruff format --check + pyrefly + pyproject-fmt + rumdl
just format           # auto-fix all formatters
just test             # all tests (integration + e2e)
just test-integration # integration only
just test-e2e         # e2e only (requires Node.js, pnpm, and Rust toolchains)
```

## Testing patterns

- **Integration** — call `copie.copy(extra_answers=...)`, assert on
  `result.project_dir / 'some_file'`. Never shell out.
- **E2E** — call `copie.copy()`, then `subprocess.run(['pnpm', 'install', ...],
  cwd=project_dir)`, then `pnpm run lint`, then `pnpm run typecheck`, then
  `cargo check`. Use helpers from `tests/e2e/_helpers.py`.
- Fixtures live in `tests/conftest.py`. `default_answers` uses `chance`
  library; `project_package` MUST derive from `project_name.replace('-', '_')`
  with `_lib` suffix.
- When adding a new question, add the corresponding key to
  `default_answers` in conftest.py.

## Constraints

- `_tasks` commands are rendered as Jinja2 strings, NOT as YAML structures.
  YAML is parsed first; use inline `{% if var %}cmd{% else %}true{% endif %}`
  for conditionals — never `{% if %}` around YAML list items.
- `_envops.undefined: jinja2.StrictUndefined` is set — missing template
  variables will raise errors rather than silently rendering as empty strings.
- External tools: this project assumes `uv` and `just` are available in PATH
  (both in dev and CI).

## When adding a feature

1. Question in `copier/questions/<category>.yml` (with validator if needed).
2. Template logic in `template/` (Jinja2 conditionals).
3. Integration test: assert generated file content.
4. E2E test: if the change affects the generated project's ability to
   `pnpm install`, `pnpm run lint`, `pnpm run typecheck`, or `cargo check`.
5. Update `default_answers` fixture if a new question was added.
6. Run `just check && just test`.
