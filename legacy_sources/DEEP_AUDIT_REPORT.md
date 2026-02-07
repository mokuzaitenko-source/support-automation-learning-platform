# Deep Audit Report

Date: 2026-02-07
Scope: `aca-learning-platform` plus imported `legacy_sources`

## What was audited

- Syntax/compile checks for active and legacy Python modules
- Import checks for all primary modules
- HTTP smoke tests for both apps:
  - Main app (`app.py`)
  - Legacy app (`legacy_sources/PyLearn_app.py`)
- Legacy launcher behavior and path safety
- Template endpoint compatibility across main + legacy apps

## Findings and fixes

1. Legacy Flask app route/template mismatch
- Issue: shared templates expected endpoint names that did not match legacy route setup.
- Fix: added endpoint alias in `legacy_sources/PyLearn_app.py`:
  - `lesson_view` now resolves to legacy lesson handler.

2. Legacy app missing progress metadata
- Issue: template expected `path.progress.*` and failed with 500.
- Fix: injected default progress metadata in legacy index/path routes.

3. Legacy launcher hardcoded absolute path
- Issue: `legacy_sources/Launch_Python_Learning_desktop.bat` pointed to a machine-specific path.
- Fix: switched to script-relative `%~dp0` path and local target app.

4. Legacy modern UI import fragility
- Issue: `UnifiedApp_Modern_desktop.py` imported `UnifiedApp` only.
- Fix: import now prefers local `UnifiedApp_desktop.py` with fallback behavior.

5. Cross-app template compatibility
- Issue: endpoint name changes could break the main app while fixing legacy.
- Fix: templates standardized on `lesson_view`; legacy app now exposes that alias.

## Validation results

- Main app routes:
  - `GET /` => 200
  - `GET /path/fundamentals` => 200
  - `GET /lesson/fundamentals/hello_world` => 200
  - `GET /playground` => 200
  - `POST /execute` => 200

- Legacy app routes:
  - `GET /` => 200
  - `GET /path/fundamentals` => 200
  - `GET /lesson/fundamentals/hello_world` => 200
  - `GET /playground` => 200
  - `POST /execute` => 200

- Existing integrated test suite:
  - `python test_all_features.py` => pass

## New tooling added

- `legacy_sources/deep_audit_checks.py`
  - Runs compile checks, import checks, and main + legacy endpoint smoke tests.

Run it with:

```powershell
python legacy_sources/deep_audit_checks.py
```

Exit code `0` means all deep checks passed.

## Operational note

- `legacy_sources/aca-unified-assistant.py` imports successfully, but advanced features may require an external `aca-copilot` directory and related assets to be present.
