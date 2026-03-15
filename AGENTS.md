# Repository Guidelines

## Project Structure & Module Organization
`src/` contains the playable application and core game logic: `start.py` launches the Tkinter desktop game, `dash_intro_launcher.py` starts the Dash-based flow, and modules such as `backend_game.py`, `country.py`, and `setup_data.py` hold shared rules and data loading. `data/` stores the CSV datasets consumed at runtime, including `data/for_testing_only/` for test fixtures. UI assets live in `assets/`, `map/`, and `pictures/`. `tests/` contains pytest-based regression tests. `build/`, `logs/`, and `backenddata/` hold generated artifacts or cached data and should only be updated when the change requires it.

## Build, Test, and Development Commands
Work from the repository root so file paths like `data/...` resolve correctly.

- `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` installs the Python dependencies.
- `.\.venv\Scripts\python.exe src\start.py` runs the main desktop game.
- `.\.venv\Scripts\python.exe src\dash_intro_launcher.py` runs the Dash launcher.
- `.\.venv\Scripts\python.exe -m pytest tests` runs the automated tests.
- `pyinstaller start.spec` builds the packaged desktop executable when a release build is needed.

## Coding Style & Naming Conventions
Use 4-space indentation and keep imports, type hints, and short docstrings consistent with the existing Python files. Follow `snake_case` for modules, functions, variables, and CSV-backed attribute names; use `PascalCase` for classes such as `Country` and `MainWindow`. Prefer small, focused helpers in `src/` over embedding data logic in UI files. Keep file access rooted under `data/` because loaders such as `setup_data()` expect repository-relative paths.

## Testing Guidelines
Add tests under `tests/` using `test_*.py` names and pytest fixtures. Favor isolated tests that reset mutable globals from `global_definitions` before and after each run. Place small fixture CSVs in `data/for_testing_only/`. Current baseline: `.\.venv\Scripts\python.exe -m pytest tests\test_setup_data.py` fails because `Country` now requires additional constructor arguments, so update or extend tests alongside related code changes.

## Commit & Pull Request Guidelines
Recent history mostly follows Conventional Commit prefixes such as `feat:`, `fix:`, `chore:`, and `refactor:`; continue that pattern with short imperative subjects. Pull requests should describe gameplay or data impact, list touched datasets, and include screenshots for UI, map, or Dash changes. Link the relevant issue or bug report when one exists, and call out any large generated files intentionally included in the diff.

## Documentation
We use mainly dash-mantine components v2. You can find the documentation under:
https://www.dash-mantine-components.com/assets/llms.txt
