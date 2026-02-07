import importlib.util
import json
import os
import re
from collections import Counter
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
from pathlib import Path

BASE = Path(__file__).resolve().parent
ACA_DIR = BASE / "aca-copilot"
RUNNER = ACA_DIR / "run.py"
RULEBOOK_PATH = ACA_DIR / "tools" / "rulebook.py"
LEARNING_PLAN = BASE / "deep_learning_learning_plan.ipynb"
ACA_GUI = ACA_DIR / "aca-gui.py"
ASSISTANT_PLAN = BASE / "deep_learning_assistant.py"
PROGRESS_PATH = BASE / "learning_progress.json"
NOTES_PATH = BASE / "learning_notes.txt"

STOPWORDS = {
    "the", "and", "a", "an", "to", "of", "in", "on", "for", "with", "that", "as",
    "is", "are", "was", "were", "be", "been", "it", "by", "or", "at", "from",
    "this", "these", "those", "their", "its", "into", "can", "will", "we", "our",
    "your", "you", "they", "them", "i", "he", "she", "his", "her", "what", "which",
    "who", "whom", "whose", "but", "if", "then", "else", "when", "while", "so", "do",
    "does", "did", "have", "has", "had", "not", "no", "yes", "up", "down", "out", "about",
    "over", "under"
}


NEXT_SUGGESTIONS = {
    "Phase 1": "Finish a math refresher video; derive d/dx for a simple chain rule; run a small tensor example.",
    "Phase 2": "Complete a PyTorch tutorial cell; tweak a hyperparameter; log the loss trend.",
    "Phase 3": "Implement one backprop step by hand or in code; compare with autograd.",
    "Phase 4": "Train a small CNN on a sample batch; visualize activations or filters.",
    "Phase 5": "Tokenize text; run a tiny transformer forward pass; inspect attention shapes.",
    "Phase 6": "Pick a specialization task; write a one-paragraph plan; start a small experiment.",
}



# ----------------- Data loaders -----------------

def load_aca_rulebook():
    spec = importlib.util.spec_from_file_location("acarb", RULEBOOK_PATH)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        rules = getattr(module, "RULES", None)
        if isinstance(rules, dict):
            return rules
    except Exception:
        return None
    return None


def load_assistant_module():
    if not ASSISTANT_PLAN.exists():
        return None
    spec = importlib.util.spec_from_file_location("dlassistant", ASSISTANT_PLAN)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


def build_learning_plan():
    module = load_assistant_module()
    if not module:
        return {}
    builder = getattr(module, "build_learning_plan", None)
    if callable(builder):
        return builder()
    return {}


def build_projects():
    module = load_assistant_module()
    if not module:
        return {}
    builder = getattr(module, "build_projects", None)
    if callable(builder):
        return builder()
    return {}


def build_rulebook_fallback():
    module = load_assistant_module()
    if not module:
        return {}
    builder = getattr(module, "build_rulebook", None)
    if callable(builder):
        return builder()
    return {}


def load_runner_module():
    runner_path = ACA_DIR / "tools" / "runner.py"
    if not runner_path.exists():
        return None
    spec = importlib.util.spec_from_file_location("acrunner", runner_path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception:
        return None


# ----------------- ACA calls -----------------

def call_run(cmd: str) -> str:

    if not RUNNER.exists():
        return "run.py not found."
    try:
        res = subprocess.run(
            [sys.executable, str(RUNNER), cmd],
            capture_output=True,
            text=True,
            timeout=10,
        )
        out = res.stdout or ""
        err = res.stderr or ""
        return (out + ("\n" + err if err else "")).strip()
    except Exception as exc:
        return f"Error: {exc}"


def cuda_warning_for_code(code: str) -> str:
    if "torch.cuda.is_available" not in code:
        return ""
    try:
        import torch  # type: ignore
    except Exception:
        return "Note: torch is not available here, so CUDA checks will fail."
    try:
        if not torch.cuda.is_available():
            return "Note: CUDA is not available on this machine."
    except Exception:
        return "Note: CUDA check failed on this machine."
    return ""




def run_code_snippet(code: str) -> str:
    runner = load_runner_module()
    if not runner:
        return "Runner not found."
    run_cell = getattr(runner, "run_cell", None)
    if not callable(run_cell):
        return "Runner unavailable."
    result = run_cell(code, 5)
    out = result.get("stdout", "")
    err = result.get("stderr", "")
    elapsed = result.get("elapsed_ms", None)
    parts = []
    if out:
        parts.append(out.strip())
    if err:
        parts.append(err.strip())
    if elapsed is not None:
        parts.append(f"[t={elapsed}ms]")
    warn = cuda_warning_for_code(code)
    if warn:
        parts.append(warn)
    return "\n".join(parts) if parts else "(no output)"


def open_file(path: Path):
    if not path.exists():
        return
    code_bin = "code.cmd" if sys.platform.startswith("win") else "code"
    try:
        subprocess.run([code_bin, "--reuse-window", str(path)], check=False)
        return
    except Exception:
        pass
    if sys.platform.startswith("win"):
        try:
            subprocess.Popen(["notepad.exe", str(path)])
            return
        except Exception:
            pass
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["open", str(path)])
    except Exception:
        pass


def open_aca_gui():
    if not ACA_GUI.exists():
        return "ACA GUI not found."
    try:
        subprocess.Popen([sys.executable, str(ACA_GUI)], cwd=str(ACA_DIR))
        return "Opened ACA GUI."
    except Exception as exc:
        return f"Error: {exc}"


def summarize_text(text: str, num_sentences: int = 3) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= num_sentences:
        return text.strip()
    words = re.findall(r"\b\w+\b", text.lower())
    freq = Counter(w for w in words if w not in STOPWORDS)
    scores = {}
    for sent in sentences:
        tokens = re.findall(r"\b\w+\b", sent.lower())
        score = sum(freq.get(tok, 0) for tok in tokens if tok not in STOPWORDS)
        scores[sent] = score
    top_sents = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    ordered = [s for s in sentences if s in top_sents]
    return " ".join(ordered)


def open_and_summarize_file() -> str:
    path = filedialog.askopenfilename(
        title="Select a text or PDF file",
        filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf"), ("All files", "*.*")],
    )
    if not path:
        return "No file selected."
    try:
        text = ""
        if path.lower().endswith(".pdf"):
            try:
                import PyPDF2  # type: ignore
            except Exception:
                return "PDF support requires PyPDF2. Install it or choose a text file."
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        if not text.strip():
            return "The selected file appears to be empty."
        return summarize_text(text)
    except Exception as exc:
        return f"Could not summarize the file: {exc}"


# ----------------- GUI -----------------

class UnifiedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ACA Unified Assistant")
        self.geometry("900x650")
        self.resizable(True, True)

        self.history = []
        self._notes_after_id = None

        aca_rules = load_aca_rulebook()
        if aca_rules:
            self.rulebook = aca_rules
            self.rulebook_source = "ACA rulebook"
        else:
            self.rulebook = build_rulebook_fallback() or {}
            self.rulebook_source = "Assistant plan"

        self.learning_plan = build_learning_plan()
        self.projects = build_projects()

        self._init_menu()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self._init_dashboard_tab()
        self._init_rulebook_tab()
        self._init_learning_tab()
        self._init_projects_tab()
        self._init_progress_tab()
        self._init_notes_tab()
        self._init_code_tab()
        self._init_summarize_tab()

    # Dashboard: quick actions
    def _init_dashboard_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")

        btn_frame = ttk.LabelFrame(frame, text="Quick Why")
        btn_frame.pack(fill=tk.X, padx=8, pady=6)
        quick_keys = ["loss", "matmul", "optimizer.step()", "zero_grad()", "model.eval()", "relu"]
        for idx, key in enumerate(quick_keys):
            ttk.Button(btn_frame, text=key, command=lambda k=key: self._run_why(k)).grid(
                row=idx // 3, column=idx % 3, padx=4, pady=4, sticky="w"
            )


        mode_frame = ttk.LabelFrame(frame, text="Modes")
        mode_frame.pack(fill=tk.X, padx=8, pady=6)
        for idx, mode in enumerate(["Study", "Build", "Debug", "Interview"]):
            ttk.Button(mode_frame, text=mode, command=lambda m=mode: self._enter_mode(m)).grid(row=0, column=idx, padx=4, pady=4)

        cmd_frame = ttk.LabelFrame(frame, text="ACA Command")
        cmd_frame.pack(fill=tk.X, padx=8, pady=6)
        self.cmd_var = tk.StringVar()
        cmd_entry = ttk.Entry(cmd_frame, textvariable=self.cmd_var)
        cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 4), pady=4)
        cmd_entry.bind("<Return>", lambda _e: self._run_cmd())
        ttk.Button(cmd_frame, text="Run", command=self._run_cmd).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(cmd_frame, text="Clear", command=self._clear_output).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(cmd_frame, text="Copy Output", command=self._copy_output).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(cmd_frame, text="Next Step", command=self._next_step).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(cmd_frame, text="Help", command=self._show_help).pack(side=tk.LEFT, padx=4, pady=4)

        link_frame = ttk.LabelFrame(frame, text="Open Files")
        link_frame.pack(fill=tk.X, padx=8, pady=6)
        ttk.Button(link_frame, text="Open ACA GUI", command=self._open_aca_gui).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(link_frame, text="Open Rulebook", command=lambda: open_file(RULEBOOK_PATH)).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(link_frame, text="Open Learning Plan", command=lambda: open_file(LEARNING_PLAN)).pack(side=tk.LEFT, padx=4, pady=4)

        self.status_var = tk.StringVar(value=f"Ready. Rulebook: {self.rulebook_source}.")
        status = ttk.Label(frame, textvariable=self.status_var, anchor="w")
        status.pack(fill=tk.X, padx=8, pady=(0, 4))

        body = ttk.Frame(frame)
        body.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        history_frame = ttk.LabelFrame(body, text="History")
        history_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        self.history_list = tk.Listbox(history_frame, height=12)
        self.history_list.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)
        self.history_list.bind("<Double-Button-1>", self._run_from_history)

        output_frame = ttk.Frame(body)
        output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scroll = ttk.Scrollbar(output_frame)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output = tk.Text(output_frame, wrap=tk.WORD, height=14, yscrollcommand=output_scroll.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scroll.config(command=self.output.yview)
        self.output.config(state=tk.DISABLED)

    def _init_rulebook_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Rulebook")

        search_frame = ttk.Frame(frame)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="Look up a term:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind("<Return>", lambda _e: self._lookup_rule())
        ttk.Button(search_frame, text="Search", command=self._lookup_rule).pack(side=tk.LEFT, padx=(5, 0))

        result_text = tk.Text(frame, wrap=tk.WORD)
        result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        result_text.config(state=tk.DISABLED)
        self.result_text = result_text
        self._populate_rulebook()

    def _init_learning_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Learning Path")
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)
        for phase, desc in self.learning_plan.items():
            text.insert(tk.END, f"{phase}\n", "heading")
            text.insert(tk.END, f"{desc}\n\n")
        text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
        text.config(state=tk.DISABLED)

    def _init_projects_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Projects")
        listbox = tk.Listbox(frame, exportselection=False)
        listbox.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=5)
        for name in sorted(self.projects.keys()):
            listbox.insert(tk.END, name)
        project_text = tk.Text(frame, wrap=tk.WORD)
        project_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        project_text.config(state=tk.DISABLED)

        def show_project(_e=None):
            selection = listbox.curselection()
            if selection:
                name = listbox.get(selection[0])
                description = self.projects[name]
                project_text.config(state=tk.NORMAL)
                project_text.delete("1.0", tk.END)
                project_text.insert(tk.END, f"{name}\n", "heading")
                project_text.insert(tk.END, description)
                project_text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
                project_text.config(state=tk.DISABLED)

        listbox.bind("<<ListboxSelect>>", show_project)

    def _init_progress_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Progress")

        header = ttk.Label(frame, text="Mark each phase as complete to track progress.")
        header.pack(anchor="w", padx=8, pady=(8, 4))

        self.progress_vars = {}
        self.progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(padx=8, pady=(0, 8), fill=tk.X)

        phases = list(self.learning_plan.keys())
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        for phase in phases:
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(list_frame, text=phase, variable=var, command=self._update_progress)
            chk.pack(anchor="w", pady=2)
            self.progress_vars[phase] = var

        self._load_progress()
        self._update_progress()

    def _init_notes_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Notes")

        header = ttk.Label(frame, text="Jot down insights as you learn.")
        header.pack(anchor="w", padx=8, pady=(8, 4))

        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, padx=8, pady=(0, 4))
        ttk.Button(toolbar, text="Save", command=self._save_notes).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Load", command=self._load_notes).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Clear", command=self._clear_notes).pack(side=tk.LEFT, padx=4)

        self.notes_text = tk.Text(frame, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.notes_text.bind("<KeyRelease>", lambda _e: self._schedule_notes_save())
        self._load_notes()

    def _init_code_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Code Tools")

        ttk.Label(frame, text="Enter Python code:").pack(anchor="w", padx=8, pady=(8, 4))
        code_input = scrolledtext.ScrolledText(frame, height=10)
        code_input.pack(fill=tk.BOTH, expand=True, padx=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=6)

        ttk.Label(frame, text="Result / Explanation:").pack(anchor="w", padx=8)
        code_output = scrolledtext.ScrolledText(frame, height=10)
        code_output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        def run_code_action():
            code = code_input.get("1.0", tk.END).strip()
            if not code:
                code_output.delete("1.0", tk.END)
                code_output.insert(tk.END, "Please enter Python code to run.")
                return
            result = run_code_snippet(code)
            code_output.delete("1.0", tk.END)
            code_output.insert(tk.END, result)

        def explain_code_action():
            code = code_input.get("1.0", tk.END).strip()
            if not code:
                code_output.delete("1.0", tk.END)
                code_output.insert(tk.END, "Please enter Python code to explain.")
                return
            explanation = self._explain_code_snippet(code)
            code_output.delete("1.0", tk.END)
            code_output.insert(tk.END, explanation)

        ttk.Button(btn_frame, text="Run Code", command=run_code_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Explain Code", command=explain_code_action).pack(side=tk.LEFT, padx=5)

    def _init_summarize_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Summarize File")

        ttk.Label(frame, text="Summary:").pack(anchor="w", padx=8, pady=(8, 4))
        summary_box = scrolledtext.ScrolledText(frame, height=15)
        summary_box.pack(fill=tk.BOTH, expand=True, padx=8)

        def handle_summarize():
            summary = open_and_summarize_file()
            summary_box.delete("1.0", tk.END)
            summary_box.insert(tk.END, summary)

        ttk.Button(frame, text="Open and Summarize File", command=handle_summarize).pack(pady=10)

    # Helpers
    def _write_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text + ("\n" if not text.endswith("\n") else ""))
        self.output.config(state=tk.DISABLED)
        self.output.see(tk.END)

    def _inspect_tensor(self, expr: str) -> str:
        snippet = (
            "import torch\n"
            f"obj = {expr}\n"
            "info = []\n"
            "info.append(f'type: {type(obj).__name__}')\n"
            "if isinstance(obj, torch.Tensor):\n"
            "    info.append(f'shape: {tuple(obj.shape)}')\n"
            "    info.append(f'dtype: {obj.dtype}')\n"
            "    info.append(f'device: {obj.device}')\n"
            "    info.append(f'requires_grad: {obj.requires_grad}')\n"
            "    try: info.append(f'mean: {obj.float().mean().item():.6f}')\n"
            "    except Exception: pass\n"
            "    try: info.append(f'std: {obj.float().std().item():.6f}')\n"
            "    except Exception: pass\n"
            "    try: info.append(f'min: {obj.min().item():.6f}')\n"
            "    except Exception: pass\n"
            "    try: info.append(f'max: {obj.max().item():.6f}')\n"
            "    except Exception: pass\n"
            "else:\n"
            "    info.append(f'value: {obj}')\n"
            "print('\\n'.join(info))\n"
        )
        return run_code_snippet(snippet)

    def _next_step(self) -> str:
        phases = list(self.learning_plan.keys())
        for phase in phases:
            done = getattr(self, "progress_vars", {}).get(phase)
            if done is None or not done.get():
                for key, suggestion in NEXT_SUGGESTIONS.items():
                    if key.lower() in phase.lower():
                        return f"Next: {phase} -> {suggestion}"
                return f"Next: {phase} -> take one concrete action today."
        return "All phases marked complete. Start a capstone or a review."

    def _enter_mode(self, mode: str):
        if mode == "Study":
            self._ask_mode_followup(mode, ["Summary", "Quiz", "Step-by-step solution"])
        elif mode == "Build":
            self._ask_mode_followup(mode, ["List tasks", "Next commit", "Explain design"])
        elif mode == "Debug":
            self._ask_mode_followup(mode, ["Traceback help", "Likely cause", "Fix options"])
        elif mode == "Interview":
            self._ask_mode_followup(mode, ["Explain concept", "Ask me questions", "Grade my answer"])
        else:
            self._write_output(f"Unknown mode: {mode}")

    def _ask_mode_followup(self, mode: str, options):
        from tkinter import simpledialog
        choice = simpledialog.askstring(f"{mode} mode", f"What do you want? Options: {', '.join(options)}")
        if not choice:
            self._write_output(f"[{mode}] No choice provided.")
            return
        self._write_output(f"[{mode}] You chose: {choice}")
        self._push_history(f"{mode}:{choice}")



    def _run_why(self, key):
        result = call_run(f"why {key}")
        self.status_var.set(f"Last: why {key}")
        self._push_history(f"why {key}")
        self._write_output(result)

    def _run_cmd(self):
        cmd = self.cmd_var.get().strip()
        if not cmd:
            return
        lower = cmd.lower()
        if lower.startswith('inspect '):
            expr = cmd.split(' ', 1)[1]
            result = self._inspect_tensor(expr)
            self.status_var.set(f"Inspect: {expr}")
            self._push_history(cmd)
            self._write_output(result)
            return
        if lower.startswith('next'):
            self._push_history(cmd)
            self._write_output(self._next_step())
            return
        if lower.startswith(('study', 'build', 'debug', 'interview')):
            parts = lower.split(' ', 1)
            mode = parts[0].capitalize()
            self._enter_mode(mode)
            return
        result = call_run(cmd)
        self.status_var.set(f"Last: {cmd}")
        self._push_history(cmd)
        self._write_output(result)

    def _open_aca_gui(self):
        result = open_aca_gui()
        if result:
            self.status_var.set(result)
            self._write_output(result)

    def _clear_output(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)
        self.status_var.set(f"Ready. Rulebook: {self.rulebook_source}.")
        self.output.see(tk.END)

    def _copy_output(self):
        text = self.output.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_var.set("Output copied to clipboard.")


    def _show_help(self):
        help_text = """Quick commands:
  why <term>
  run <python>

Examples:
  why loss
  why model.eval()
  run print(3*3)

Tips:
  Double-click a history item to re-run it.
  Update aca-copilot/tools/rulebook.py to change the metaphors."""
        win = tk.Toplevel(self)
        win.title("Help")
        tk.Label(win, text=help_text, justify=tk.LEFT).pack(padx=12, pady=12)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 12))


    def _push_history(self, cmd):
        if not cmd:
            return
        self.history.append(cmd)
        self.history_list.insert(tk.END, cmd)

    def _run_from_history(self, _event):
        selection = self.history_list.curselection()
        if not selection:
            return
        cmd = self.history_list.get(selection[0])
        self.cmd_var.set(cmd)
        self._run_cmd()

    def _populate_rulebook(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        for term, desc in sorted(self.rulebook.items()):
            self.result_text.insert(tk.END, f"{term}\n", "heading")
            self.result_text.insert(tk.END, f"{desc}\n\n")
        self.result_text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
        self.result_text.config(state=tk.DISABLED)

    def _lookup_rule(self):
        term = self.search_var.get().strip()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        if term:
            key_norm = term.lower().rstrip("()")
            match = None
            if term in self.rulebook:
                match = term
            elif key_norm in self.rulebook:
                match = key_norm
            else:
                for k in self.rulebook:
                    if key_norm == k.lower():
                        match = k
                        break
            if match:
                desc = self.rulebook[match]
                self.result_text.insert(tk.END, f"{match}\n", "heading")
                self.result_text.insert(tk.END, desc)
                self.result_text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
            else:
                self.result_text.insert(tk.END, "I don't know that term yet. Add it to the rulebook.")
        else:
            self._populate_rulebook()
        self.result_text.config(state=tk.DISABLED)


    def _update_progress(self):
        total = max(len(self.progress_vars), 1)
        done = sum(1 for v in self.progress_vars.values() if v.get())
        percent = int((done / total) * 100)
        self.progress_bar["value"] = percent
        self.status_var.set(f"Progress: {percent}% complete. Rulebook: {self.rulebook_source}.")
        self._save_progress()

    def _save_progress(self):
        data = {phase: var.get() for phase, var in self.progress_vars.items()}
        try:
            with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _load_progress(self):
        if not PROGRESS_PATH.exists():
            return
        try:
            with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            for phase, value in data.items():
                if phase in self.progress_vars:
                    self.progress_vars[phase].set(bool(value))
        except Exception:
            return

    def _save_notes(self, silent=False):
        content = self.notes_text.get("1.0", tk.END)
        try:
            with open(NOTES_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            if not silent:
                self.status_var.set("Notes saved.")
        except Exception:
            if not silent:
                self.status_var.set("Failed to save notes.")

    def _load_notes(self):
        if not NOTES_PATH.exists():
            return
        try:
            with open(NOTES_PATH, "r", encoding="utf-8") as f:
                content = f.read()
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert(tk.END, content)
        except Exception:
            pass

    def _clear_notes(self):
        self.notes_text.delete("1.0", tk.END)
        self.status_var.set("Notes cleared.")

    def _schedule_notes_save(self):
        if self._notes_after_id is not None:
            self.after_cancel(self._notes_after_id)
        self._notes_after_id = self.after(5000, lambda: self._save_notes(silent=True))

    def _explain_code_snippet(self, code: str) -> str:
        lower = code.lower()
        matches = []
        for key, desc in self.rulebook.items():
            if key.lower() in lower:
                matches.append(f"{key}: {desc}")
        if matches:
            return "\n".join(matches)
        return "No specific explanations found. Add it to the rulebook."

    def _init_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open ACA GUI", command=self._open_aca_gui)
        file_menu.add_command(label="Open Rulebook", command=lambda: open_file(RULEBOOK_PATH))
        file_menu.add_command(label="Open Learning Plan", command=lambda: open_file(LEARNING_PLAN))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Copy Output", command=self._copy_output)
        edit_menu.add_command(label="Clear Output", command=self._clear_output)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)


def main():
    app = UnifiedApp()
    app.mainloop()


if __name__ == "__main__":
    main()
