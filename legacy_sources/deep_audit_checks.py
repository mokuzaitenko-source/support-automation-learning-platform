"""Deep audit checks for aca-learning-platform and legacy sources."""
import importlib.util
from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FILES_TO_COMPILE = [
    ROOT / "UnifiedApp.py",
    ROOT / "ModernUnifiedApp.py",
    ROOT / "app.py",
    ROOT / "legacy_sources" / "UnifiedApp_desktop.py",
    ROOT / "legacy_sources" / "UnifiedApp_Modern_desktop.py",
    ROOT / "legacy_sources" / "PyLearn_app.py",
    ROOT / "legacy_sources" / "aca-unified-assistant.py",
]


def import_module(path: Path, mod_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_compile():
    for path in FILES_TO_COMPILE:
        py_compile.compile(str(path), doraise=True)


def check_imports():
    for i, path in enumerate(FILES_TO_COMPILE, start=1):
        import_module(path, f"audit_mod_{i}")


def check_main_routes():
    app_mod = import_module(ROOT / "app.py", "main_app")
    c = app_mod.app.test_client()
    assert c.get("/").status_code == 200
    assert c.get("/path/fundamentals").status_code == 200
    assert c.get("/lesson/fundamentals/hello_world").status_code == 200
    assert c.get("/playground").status_code == 200
    assert c.post("/execute", json={"code": "print(6*7)"}).status_code == 200


def check_legacy_routes():
    legacy_mod = import_module(ROOT / "legacy_sources" / "PyLearn_app.py", "legacy_app")
    c = legacy_mod.app.test_client()
    assert c.get("/").status_code == 200
    assert c.get("/path/fundamentals").status_code == 200
    assert c.get("/lesson/fundamentals/hello_world").status_code == 200
    assert c.get("/playground").status_code == 200
    assert c.post("/execute", json={"code": "print(6*7)"}).status_code == 200


def main():
    check_compile()
    check_imports()
    check_main_routes()
    check_legacy_routes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
