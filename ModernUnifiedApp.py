from UnifiedApp import *


class ModernUnifiedAppGUI(UnifiedAppGUI):
    """Modern, smooth UI version of UnifiedApp"""

    def create_main_layout(self):
        bg_color = "#f5f5f5"
        panel_color = "#ffffff"
        accent_color = "#2196F3"

        toolbar = tk.Frame(self.root, bg=accent_color, height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        title_label = tk.Label(
            toolbar,
            text="Python Learning Platform",
            font=("Segoe UI", 18, "bold"),
            bg=accent_color,
            fg="white",
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        quick_run_btn = tk.Button(
            toolbar,
            text="Run (Ctrl+Enter)",
            command=self.execute_code,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
        )
        quick_run_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        quick_clear_btn = tk.Button(
            toolbar,
            text="Clear (Ctrl+L)",
            command=self.clear_output,
            bg="#FF5722",
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
        )
        quick_clear_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        left_panel = tk.Frame(main_container, bg=panel_color, width=300, relief=tk.FLAT, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        left_panel.pack_propagate(False)

        resource_header = tk.Label(
            left_panel,
            text="Learning Resources",
            font=("Segoe UI", 14, "bold"),
            bg=panel_color,
            fg="#333",
        )
        resource_header.pack(pady=(15, 10), padx=10, anchor=tk.W)

        category_frame = tk.Frame(left_panel, bg=panel_color)
        category_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(
            category_frame,
            text="Choose Category:",
            font=("Segoe UI", 10, "bold"),
            bg=panel_color,
            fg="#666",
        ).pack(anchor=tk.W, pady=5)

        self.template_category = tk.StringVar(value="Python Course")

        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.template_category,
            values=[
                "Python Course",
                "Beginner",
                "Quick Examples",
                "Python Library",
                "Course Labs",
                "DL Roadmap",
            ],
            font=("Segoe UI", 10),
            state="readonly",
            width=28,
        )
        category_dropdown.pack(fill=tk.X, pady=5)
        category_dropdown.bind("<<ComboboxSelected>>", self.update_template_list)

        template_frame = tk.Frame(left_panel, bg=panel_color)
        template_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(
            template_frame,
            text="Select Lesson/Example:",
            font=("Segoe UI", 10, "bold"),
            bg=panel_color,
            fg="#666",
        ).pack(anchor=tk.W, pady=5)

        list_container = tk.Frame(template_frame, bg=panel_color)
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.template_listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 9),
            bg="white",
            fg="#333",
            selectbackground=accent_color,
            selectforeground="white",
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor=accent_color,
            yscrollcommand=scrollbar.set,
        )
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.template_listbox.bind("<Double-1>", lambda _e: self.load_selected_template())
        scrollbar.config(command=self.template_listbox.yview)

        load_btn = tk.Button(
            template_frame,
            text="Load Selected",
            command=self.load_selected_template,
            bg=accent_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=10,
            cursor="hand2",
        )
        load_btn.pack(fill=tk.X, pady=(10, 0))

        help_frame = tk.Frame(left_panel, bg="#E3F2FD", relief=tk.FLAT, bd=1)
        help_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            help_frame,
            text="Shortcuts",
            font=("Segoe UI", 9, "bold"),
            bg="#E3F2FD",
            fg="#1976D2",
        ).pack(anchor=tk.W, padx=10, pady=(8, 5))

        shortcuts_text = """Ctrl+Enter = Run Code
Ctrl+L = Clear Output
Tab = Indent (4 spaces)
Ctrl+S = Save Code"""
        tk.Label(
            help_frame,
            text=shortcuts_text,
            font=("Segoe UI", 8),
            bg="#E3F2FD",
            fg="#333",
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=10, pady=(0, 8))

        center_panel = tk.Frame(main_container, bg=panel_color, relief=tk.FLAT, bd=1)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        editor_header_frame = tk.Frame(center_panel, bg="#37474F", height=40)
        editor_header_frame.pack(fill=tk.X)
        editor_header_frame.pack_propagate(False)

        tk.Label(
            editor_header_frame,
            text="Code Editor",
            font=("Segoe UI", 12, "bold"),
            bg="#37474F",
            fg="white",
        ).pack(side=tk.LEFT, padx=15, pady=8)

        self.line_indicator = tk.Label(
            editor_header_frame,
            text="Line 1, Col 1",
            font=("Segoe UI", 9),
            bg="#37474F",
            fg="#B0BEC5",
        )
        self.line_indicator.pack(side=tk.RIGHT, padx=15, pady=8)

        self.code_text = scrolledtext.ScrolledText(
            center_panel,
            font=("Consolas", 11),
            wrap=tk.NONE,
            bg="#263238",
            fg="#FFFFFF",
            insertbackground="white",
            selectbackground="#455A64",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10,
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)

        placeholder = """# Welcome to Python Learning Platform!
#
# Quick Start:
#   1. Select a category from the left
#   2. Choose a lesson or example
#   3. Click \"Load Selected\" or write code
#   4. Press Ctrl+Enter to run

print(\"Hello, Python!\")
"""
        self.code_text.insert("1.0", placeholder)

        self.code_text.bind("<Control-Return>", lambda e: self.execute_code())
        self.code_text.bind("<Control-l>", lambda e: self.clear_output())
        self.code_text.bind("<Control-s>", lambda e: self.save_code())
        self.code_text.bind("<Tab>", self.insert_tab)
        self.code_text.bind("<KeyRelease>", self.update_cursor_position)

        right_panel = tk.Frame(main_container, bg=panel_color, width=450, relief=tk.FLAT, bd=1)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=10)
        right_panel.pack_propagate(False)

        output_header = tk.Frame(right_panel, bg="#2E7D32", height=40)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)

        tk.Label(
            output_header,
            text="Output Console",
            font=("Segoe UI", 12, "bold"),
            bg="#2E7D32",
            fg="white",
        ).pack(side=tk.LEFT, padx=15, pady=8)

        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            bg="#1B1B1B",
            fg="#00E676",
            font=("Consolas", 10),
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10,
            height=20,
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        tools_header = tk.Label(
            right_panel,
            text="Code Tools",
            font=("Segoe UI", 11, "bold"),
            bg=panel_color,
            fg="#333",
        )
        tools_header.pack(pady=(15, 10), padx=15, anchor=tk.W)

        tools_frame = tk.Frame(right_panel, bg=panel_color)
        tools_frame.pack(fill=tk.X, padx=15, pady=5)

        tools_config = [
            ("Lint", self.lint_code, "#9C27B0"),
            ("Analyze", self.analyze_code, "#FF9800"),
            ("Suggest", self.suggest_improvements, "#FF5722"),
            ("Explain", self.explain_code, "#00BCD4"),
            ("Roadmap", self.open_roadmap, "#2196F3"),
            ("Save", self.save_code, "#4CAF50"),
        ]

        for i, (text, command, color) in enumerate(tools_config):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                tools_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                pady=8,
                cursor="hand2",
                width=12,
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        tools_frame.columnconfigure(0, weight=1)
        tools_frame.columnconfigure(1, weight=1)

        self.status_bar = tk.Frame(self.root, bg="#263238", height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            self.status_bar,
            text="Ready",
            font=("Segoe UI", 9),
            bg="#263238",
            fg="#B0BEC5",
            anchor=tk.W,
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)

        self.stats_label = tk.Label(
            self.status_bar,
            text="Lines: 0 | Chars: 0",
            font=("Segoe UI", 9),
            bg="#263238",
            fg="#B0BEC5",
        )
        self.stats_label.pack(side=tk.RIGHT, padx=15, pady=5)

        self.update_template_list()
        self.show_welcome_message()

    def update_template_list(self, event=None):
        del event
        category = self.template_category.get()

        if category == "Python Course":
            templates = list(PYTHON_COURSE.keys())
        elif category == "Beginner":
            templates = list(BEGINNER_EXAMPLES.keys())
        elif category == "Quick Examples":
            templates = list(CODE_TEMPLATES.keys())
        elif category == "Python Library":
            templates = list(PYTHON_EXAMPLES.keys())
        elif category == "Course Labs":
            templates = list(COURSE_LABS.keys())
        elif category == "DL Roadmap":
            templates = list(ROADMAP_EXAMPLES.keys())
        else:
            templates = list(CODE_TEMPLATES.keys())

        self.template_listbox.delete(0, tk.END)
        for template in templates:
            self.template_listbox.insert(tk.END, template)

        if templates:
            self.template_listbox.select_set(0)

    def load_selected_template(self):
        selection = self.template_listbox.curselection()
        if not selection:
            self.log_output("Please select a lesson or example first.\n")
            return

        template_name = self.template_listbox.get(selection[0])
        category = self.template_category.get()

        self.code_text.delete("1.0", tk.END)

        source = {
            "Python Course": PYTHON_COURSE,
            "Beginner": BEGINNER_EXAMPLES,
            "Quick Examples": CODE_TEMPLATES,
            "Python Library": PYTHON_EXAMPLES,
            "Course Labs": COURSE_LABS,
            "DL Roadmap": ROADMAP_EXAMPLES,
        }.get(category, CODE_TEMPLATES)

        if template_name in source:
            self.code_text.insert("1.0", source[template_name])
            self.log_output(f"Loaded: {template_name}\n")
            self.status_label.config(text=f"Loaded: {template_name}")
        else:
            self.log_output(f"Template not found: {template_name}\n")

        self.update_cursor_position()

    def update_cursor_position(self, event=None):
        del event
        cursor_pos = self.code_text.index(tk.INSERT)
        line, col = cursor_pos.split(".")
        self.line_indicator.config(text=f"Line {line}, Col {int(col)+1}")

        content = self.code_text.get("1.0", tk.END)
        lines = content.count("\n")
        chars = len(content) - 1
        self.stats_label.config(text=f"Lines: {lines} | Chars: {chars}")

    def show_welcome_message(self):
        self.log_output("=" * 60 + "\n")
        self.log_output("PYTHON LEARNING PLATFORM\n")
        self.log_output("=" * 60 + "\n\n")
        self.log_output("1) Choose a category (left panel)\n")
        self.log_output("2) Select a lesson/example from the list\n")
        self.log_output("3) Click 'Load Selected'\n")
        self.log_output("4) Press Ctrl+Enter or click Run\n\n")
        self.status_label.config(text="Welcome - select a lesson to begin")

    def execute_code(self):
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("No code to execute\n")
            self.status_label.config(text="No code to run")
            return

        self.log_output("\n" + "=" * 60 + "\n")
        self.log_output("Executing code...\n")
        self.log_output("=" * 60 + "\n")
        self.status_label.config(text="Running code...")
        self.root.update()

        result = run_code(code, auto_confirm=True)
        self.log_output(result + ("\n" if not result.endswith("\n") else ""))

        if "Traceback" not in result and "Error" not in result:
            self.log_output("\n" + "=" * 60 + "\n")
            self.log_output("Success: code ran without errors.\n")
            self.log_output("=" * 60 + "\n")
            self.status_label.config(text="Code executed successfully")
        else:
            self.log_output("\n" + "=" * 60 + "\n")
            self.log_output("An error occurred. Check output above.\n")
            self.log_output("=" * 60 + "\n")
            self.status_label.config(text="Error occurred")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.log_output("Output cleared.\n")
        self.status_label.config(text="Output cleared")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python Learning Platform - Modern UI")
    root.geometry("1400x900")
    root.minsize(1200, 700)
    app = ModernUnifiedAppGUI(root)
    root.mainloop()
