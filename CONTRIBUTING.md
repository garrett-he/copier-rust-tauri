# Contributing to copier-rust-tauri

Thanks for considering a contribution. This document outlines the conventions and
workflow for developing this Copier template.

## Getting started

Prerequisites: [uv](https://docs.astral.sh/uv/), [just](https://github.com/casey/just).

```sh
git clone https://github.com/garrett-he/copier-rust-tauri.git
cd copier-rust-tauri
just install
```

This installs all dev dependencies and sets up pre-commit hooks.

## Project structure

```text
copier-rust-tauri/
├── copier.yml                   # Copier entry-point (includes sub-configs)
├── copier/
│   ├── settings.yml             # Global settings, Jinja extensions, _tasks
│   ├── extensions/              # Custom context hooks
│   └── questions/               # Per-category interactive questions
├── template/                    # Jinja2 templates rendered into the output project
│   ├── package.json.jinja       # Frontend dependencies and scripts
│   ├── index.html.jinja         # HTML entry point
│   ├── README.md.jinja          # Generated project README
│   ├── src/                     # React + TypeScript frontend source
│   ├── src-tauri/               # Rust backend source
│   │   ├── Cargo.toml.jinja     # Rust dependencies
│   │   ├── tauri.conf.json.jinja # Tauri configuration
│   │   ├── build.rs.jinja       # Tauri build script
│   │   └── src/
│   │       ├── lib.rs           # Library code with tests
│   │       └── main.rs.jinja    # Binary entry point
│   └── public/                  # Static assets
└── tests/
    ├── conftest.py              # Shared fixtures (pytest-copie)
    ├── integration/             # Verify generated file contents
    └── e2e/                     # Verify generated projects build & pass checks
```

## Development workflow

| Command               | Purpose                                       |
|-----------------------|-----------------------------------------------|
| `just check`          | Run all linters and type-checkers             |
| `just format`         | Auto-format all sources                       |
| `just test`           | Run the full test suite                       |
| `just test-integration` | Run integration tests only                  |
| `just test-e2e`       | Run end-to-end tests (requires Node.js, pnpm, Rust) |

Always run `just check && just test` before opening a pull request.

## Testing

- **Integration tests** (`tests/`) — render the template with various answers
  and assert on file existence and content. Fast and deterministic.
- **End-to-end tests** (`tests/e2e/`) — generate a project, run `pnpm install`,
  `pnpm run lint`, `pnpm run typecheck`, and `cargo check` inside it. Slower
  but catches real-world breakage (missing dependencies, type errors, build
  failures).

Fixtures in `conftest.py` use [chance](https://pypi.org/project/chance/) for
randomised answer data. `project_package` is derived from `project_name` with a
`_lib` suffix.

## Adding a feature

1. If it needs new user input, add a question in `copier/questions/<category>.yml`.
2. If it changes the generated output, edit the relevant template under `template/`.
3. Add or update integration tests for file-level assertions.
4. If the change affects the generated project's ability to build or pass its own
   checks, add or update an e2e test.

## Pull request checklist

- [ ] `just check` passes with no errors.
- [ ] `just test` passes.
- [ ] New behaviour is covered by integration or e2e tests.
- [ ] Commit messages are in English, using imperative mood.
