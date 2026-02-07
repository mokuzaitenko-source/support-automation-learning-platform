# Legacy Sources Guide

This folder preserves additional source files discovered on this machine.

## Files and Purpose

- `UnifiedApp_desktop.py`
Desktop all-in-one app (Tkinter) with code execution, templates, and helper tools.

- `UnifiedApp_Modern_desktop.py`
Modernized UI variant of the desktop app. Updated to import `UnifiedApp_desktop.py` in this folder.

- `PyLearn_app.py`
Flask web app variant with learning paths and an `/execute` endpoint.

- `Launch_Python_Learning_desktop.bat`
Windows launcher script. Updated to use local folder paths and run `PyLearn_app.py`.

- `aca-unified-assistant.py`
Assistant/coach utility with ACA-copilot integrations and study helpers.

## How to Run

### 1) Legacy Flask app

```powershell
cd legacy_sources
python PyLearn_app.py
```

Open `http://127.0.0.1:5000`.

### 2) Legacy desktop app

```powershell
cd legacy_sources
python UnifiedApp_desktop.py
```

### 3) Legacy modern desktop UI

```powershell
cd legacy_sources
python UnifiedApp_Modern_desktop.py
```

### 4) Legacy launcher (Windows)

```powershell
cd legacy_sources
.\Launch_Python_Learning_desktop.bat
```

## Notes

- These files are preserved for traceability and portfolio history.
- Main active implementations remain at repo root (`UnifiedApp.py`, `ModernUnifiedApp.py`, `app.py`).
- `aca-unified-assistant.py` may require additional local files (`aca-copilot` folder) to use all features.

## Fixes Applied During Import

- `UnifiedApp_Modern_desktop.py`: fixed import to use `UnifiedApp_desktop.py` in this folder.
- `Launch_Python_Learning_desktop.bat`: removed hardcoded absolute path; now runs from local folder.
- `PyLearn_app.py`: added missing progress metadata expected by templates.
- `templates/learning_path.html` and `templates/lesson_view.html`: fixed endpoint references from `lesson_view` to `lesson`.
