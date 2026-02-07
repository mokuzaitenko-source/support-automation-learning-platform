import ast
import contextlib
import io
import os
import traceback
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk


CODE_TEMPLATES = {
    "Hello World": 'print("Hello, world!")\n',
    "For Loop": 'for i in range(5):\n    print(i)\n',
    "Function": 'def greet(name):\n    return f"Hello, {name}"\n\nprint(greet("Alvin"))\n',
}

BEGINNER_EXAMPLES = {
    "Variables": 'name = "Alvin"\nage = 33\nprint(name, age)\n',
    "If Statement": 'x = 10\nif x > 5:\n    print("x is greater than 5")\n',
}

PYTHON_EXAMPLES = {
    "List Comprehension": 'squares = [x * x for x in range(10)]\nprint(squares)\n',
    "Dictionary": 'user = {"name": "Alvin", "role": "IT Support"}\nprint(user)\n',
}

PYTHON_COURSE = {
    "Lesson 1 - Print": 'print("Welcome to Python")\n',
    "Lesson 2 - Variables": 'name = "Student"\nprint(f"Hello {name}")\n',
    "Lesson 3 - Loops": 'for i in range(3):\n    print("Loop", i)\n',
}

COURSE_LABS = {
    "Lab - Ticket Summary": (
        'tickets = [{"status": "open"}, {"status": "closed"}, {"status": "open"}]\n'
        'open_count = sum(1 for t in tickets if t["status"] == "open")\n'
        'print("Open tickets:", open_count)\n'
    ),
}

ROADMAP_EXAMPLES = {
    "Week 1 Plan": 'goals = ["Python basics", "Functions", "Debugging"]\nfor g in goals:\n    print("-", g)\n',
}


SANDBOX_DIR = os.path.join(os.path.expanduser("~"), "aca_data")
os.makedirs(SANDBOX_DIR, exist_ok=True)


def run_code(code: str, auto_confirm: bool = True) -> str:
    del auto_confirm
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec_globals = {"__builtins__": __builtins__}
            exec(code, exec_globals, {})
        out = stdout.getvalue()
        return out if out else "(no output)\n"
    except Exception:
        return traceback.format_exc()


def explain_code(code: str) -> str:
    lines = [ln for ln in code.splitlines() if ln.strip()]
    return f"Code has {len(lines)} non-empty lines."


def lint_code(code: str) -> str:
    try:
        ast.parse(code)
        return "No syntax issues detected."
    except SyntaxError as exc:
        return f"SyntaxError: {exc}"


def analyze_code(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return f"Parse failed: {exc}"

    funcs = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
    loops = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
    branches = sum(isinstance(node, ast.If) for node in ast.walk(tree))
    return f"Functions: {funcs}, Loops: {loops}, If statements: {branches}"


def suggest_improvements(code: str) -> str:
    suggestions = []
    if "print(" in code and "logging" not in code:
        suggestions.append("Consider structured logging for larger scripts.")
    if len(code.splitlines()) > 40:
        suggestions.append("Consider splitting logic into smaller functions.")
    if not suggestions:
        suggestions.append("Looks good. Add tests for long-term maintainability.")
    return "\n".join(f"- {s}" for s in suggestions)


class UnifiedAppGUI:
    """Base desktop app with helper methods for derived UIs."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.configure(bg="#f5f5f5")
        self.create_main_layout()

    def create_main_layout(self):
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(frame, text="Unified App", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.code_text = scrolledtext.ScrolledText(frame, font=("Consolas", 11), height=15)
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.output_text = scrolledtext.ScrolledText(frame, font=("Consolas", 10), height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        btn = tk.Button(frame, text="Run", command=self.execute_code)
        btn.pack(pady=8)

        self.status_label = tk.Label(frame, text="Ready", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=12, pady=6)

    def log_output(self, text: str):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def insert_tab(self, event):
        self.code_text.insert(tk.INSERT, "    ")
        return "break"

    def execute_code(self):
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("No code to run.\n")
            return
        self.log_output(run_code(code))

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def lint_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.log_output(lint_code(code) + "\n")

    def analyze_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.log_output(analyze_code(code) + "\n")

    def suggest_improvements(self):
        code = self.code_text.get("1.0", tk.END)
        self.log_output(suggest_improvements(code) + "\n")

    def explain_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.log_output(explain_code(code) + "\n")

    def open_roadmap(self):
        self.log_output("Roadmap: Python basics -> automation -> deployment.\n")

    def save_code(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
        if not filename:
            return
        with open(filename, "w", encoding="utf-8") as handle:
            handle.write(self.code_text.get("1.0", tk.END))
        self.log_output(f"Saved: {filename}\n")
