"""
ACA Package - Now redirects to UnifiedApp.py
All functionality consolidated in the main UnifiedApp.
"""
import sys
import os

# Add parent directory to path to import UnifiedApp
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from UnifiedApp import (
        SANDBOX_DIR,
        safe_exec,
        save_manifest,
        run_code,
        read_file,
        explain_code,
        lint_code,
        analyze_code,
        suggest_improvements,
        CODE_TEMPLATES,
        DL_TEMPLATES,
    )
    
    __all__ = [
        "SANDBOX_DIR",
        "safe_exec", 
        "save_manifest",
        "run_code",
        "read_file",
        "explain_code",
        "lint_code",
        "analyze_code",
        "suggest_improvements",
        "CODE_TEMPLATES",
        "DL_TEMPLATES",
    ]
except ImportError:
    # Fallback if UnifiedApp not available
    SANDBOX_DIR = os.path.join(os.path.expanduser("~"), "aca_data")
    __all__ = []
