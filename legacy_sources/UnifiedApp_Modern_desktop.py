# Import everything from legacy base app
try:
    from UnifiedApp_desktop import *
except ImportError:
    # Fallback when this file is copied back next to UnifiedApp.py
    from UnifiedApp import *

class ModernUnifiedAppGUI(UnifiedAppGUI):
    """Modern, smooth UI version of UnifiedApp"""
    
    def create_main_layout(self):
        """Create modern, smooth application layout."""
        # Modern color scheme
        bg_color = "#f5f5f5"
        panel_color = "#ffffff"
        accent_color = "#2196F3"
        
        # Top toolbar
        toolbar = tk.Frame(self.root, bg=accent_color, height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Title with icon
        title_label = tk.Label(toolbar, text="🎓 Python Learning Platform", 
                              font=("Segoe UI", 18, "bold"), 
                              bg=accent_color, fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Quick action buttons in toolbar
        quick_run_btn = tk.Button(toolbar, text="▶ Run (Ctrl+Enter)", 
                                 command=self.execute_code,
                                 bg="#4CAF50", fg="white", 
                                 font=("Segoe UI", 10, "bold"),
                                 relief=tk.FLAT, padx=15, pady=8,
                                 cursor="hand2")
        quick_run_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        quick_clear_btn = tk.Button(toolbar, text="🗑 Clear (Ctrl+L)", 
                                   command=self.clear_output,
                                   bg="#FF5722", fg="white", 
                                   font=("Segoe UI", 10),
                                   relief=tk.FLAT, padx=15, pady=8,
                                   cursor="hand2")
        quick_clear_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Main content area with 3 panels
        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # LEFT PANEL: Learning Resources & Templates
        left_panel = tk.Frame(main_container, bg=panel_color, width=300, relief=tk.FLAT, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        # Learning resources header
        resource_header = tk.Label(left_panel, text="📚 Learning Resources", 
                                  font=("Segoe UI", 14, "bold"), 
                                  bg=panel_color, fg="#333")
        resource_header.pack(pady=(15, 10), padx=10, anchor=tk.W)
        
        # Category selector with modern style
        category_frame = tk.Frame(left_panel, bg=panel_color)
        category_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(category_frame, text="Choose Category:", 
                font=("Segoe UI", 10, "bold"), bg=panel_color, fg="#666").pack(anchor=tk.W, pady=5)
        
        self.template_category = tk.StringVar(value="📘 Python Course")
        
        category_dropdown = ttk.Combobox(category_frame, textvariable=self.template_category,
                                        values=["📘 Python Course", "🔰 Beginner", "⚡ Quick Examples", 
                                               "📚 Python Library", "🎯 Course Labs", "🤖 DL Roadmap"], 
                                        font=("Segoe UI", 10), state="readonly", width=28)
        category_dropdown.pack(fill=tk.X, pady=5)
        category_dropdown.bind("<<ComboboxSelected>>", self.update_template_list)
        
        # Template selector
        template_frame = tk.Frame(left_panel, bg=panel_color)
        template_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(template_frame, text="Select Lesson/Example:", 
                font=("Segoe UI", 10, "bold"), bg=panel_color, fg="#666").pack(anchor=tk.W, pady=5)
        
        # Template listbox with scrollbar (better than dropdown for many items)
        list_container = tk.Frame(template_frame, bg=panel_color)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.template_listbox = tk.Listbox(list_container, 
                                          font=("Segoe UI", 9),
                                          bg="white", fg="#333",
                                          selectbackground=accent_color,
                                          selectforeground="white",
                                          relief=tk.FLAT, bd=1,
                                          highlightthickness=1,
                                          highlightcolor=accent_color,
                                          yscrollcommand=scrollbar.set)
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.template_listbox.yview)
        
        # Load template button
        load_btn = tk.Button(template_frame, text="📖 Load Selected", 
                           command=self.load_selected_template,
                           bg=accent_color, fg="white", 
                           font=("Segoe UI", 10, "bold"),
                           relief=tk.FLAT, pady=10,
                           cursor="hand2")
        load_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Quick help panel
        help_frame = tk.Frame(left_panel, bg="#E3F2FD", relief=tk.FLAT, bd=1)
        help_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(help_frame, text="⌨️ Shortcuts", 
                font=("Segoe UI", 9, "bold"), 
                bg="#E3F2FD", fg="#1976D2").pack(anchor=tk.W, padx=10, pady=(8, 5))
        
        shortcuts_text = """Ctrl+Enter = Run Code
Ctrl+L = Clear Output
Tab = Indent (4 spaces)
Ctrl+S = Save Code"""
        tk.Label(help_frame, text=shortcuts_text, 
                font=("Segoe UI", 8), 
                bg="#E3F2FD", fg="#333", justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 8))
        
        # CENTER PANEL: Code Editor
        center_panel = tk.Frame(main_container, bg=panel_color, relief=tk.FLAT, bd=1)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        
        # Editor header
        editor_header_frame = tk.Frame(center_panel, bg="#37474F", height=40)
        editor_header_frame.pack(fill=tk.X)
        editor_header_frame.pack_propagate(False)
        
        tk.Label(editor_header_frame, text="💻 Code Editor", 
                font=("Segoe UI", 12, "bold"), 
                bg="#37474F", fg="white").pack(side=tk.LEFT, padx=15, pady=8)
        
        # Line numbers indicator
        self.line_indicator = tk.Label(editor_header_frame, text="Line 1, Col 1", 
                                      font=("Segoe UI", 9), 
                                      bg="#37474F", fg="#B0BEC5")
        self.line_indicator.pack(side=tk.RIGHT, padx=15, pady=8)
        
        # Code editor
        self.code_text = scrolledtext.ScrolledText(center_panel, 
                                                    font=("Consolas", 11),
                                                    wrap=tk.NONE,
                                                    bg="#263238", fg="#FFFFFF",
                                                    insertbackground="white",
                                                    selectbackground="#455A64",
                                                    relief=tk.FLAT, bd=0,
                                                    padx=10, pady=10)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder text
        placeholder = """# 🎯 Welcome to Python Learning Platform!
# 
# Quick Start:
#   1. Select a category from the left (Python Course, Beginner, etc.)
#   2. Choose a lesson or example
#   3. Click "Load Selected" or write your own code here
#   4. Press Ctrl+Enter to run!
#
# Your code appears here after loading a template.
# Or start writing your own Python code now!

print("Hello, Python! 🐍")
"""
        self.code_text.insert("1.0", placeholder)
        
        # Keyboard bindings
        self.code_text.bind('<Control-Return>', lambda e: self.execute_code())
        self.code_text.bind('<Control-l>', lambda e: self.clear_output())
        self.code_text.bind('<Control-s>', lambda e: self.save_code())
        self.code_text.bind('<Tab>', self.insert_tab)
        self.code_text.bind('<KeyRelease>', self.update_cursor_position)
        
        # RIGHT PANEL: Output & Tools
        right_panel = tk.Frame(main_container, bg=panel_color, width=450, relief=tk.FLAT, bd=1)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=10)
        right_panel.pack_propagate(False)
        
        # Output header
        output_header = tk.Frame(right_panel, bg="#2E7D32", height=40)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)
        
        tk.Label(output_header, text="📟 Output Console", 
                font=("Segoe UI", 12, "bold"), 
                bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=15, pady=8)
        
        # Output console
        self.output_text = scrolledtext.ScrolledText(right_panel, 
                                                      bg="#1B1B1B", fg="#00E676",
                                                      font=("Consolas", 10),
                                                      relief=tk.FLAT, bd=0,
                                                      padx=10, pady=10,
                                                      height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Tools section
        tools_header = tk.Label(right_panel, text="🛠️ Code Tools", 
                               font=("Segoe UI", 11, "bold"), 
                               bg=panel_color, fg="#333")
        tools_header.pack(pady=(15, 10), padx=15, anchor=tk.W)
        
        # Tools grid
        tools_frame = tk.Frame(right_panel, bg=panel_color)
        tools_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Tool buttons in grid layout
        tools_config = [
            ("🔍 Lint", self.lint_code, "#9C27B0"),
            ("📊 Analyze", self.analyze_code, "#FF9800"),
            ("💡 Suggest", self.suggest_improvements, "#FF5722"),
            ("📝 Explain", self.explain_code, "#00BCD4"),
            ("📚 Roadmap", self.open_roadmap, "#2196F3"),
            ("💾 Save", self.save_code, "#4CAF50")
        ]
        
        for i, (text, command, color) in enumerate(tools_config):
            row = i // 2
            col = i % 2
            btn = tk.Button(tools_frame, text=text, command=command,
                          bg=color, fg="white", 
                          font=("Segoe UI", 9, "bold"),
                          relief=tk.FLAT, pady=8,
                          cursor="hand2", width=12)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        tools_frame.columnconfigure(0, weight=1)
        tools_frame.columnconfigure(1, weight=1)
        
        # Status bar
        self.status_bar = tk.Frame(self.root, bg="#263238", height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, text="✓ Ready", 
                                     font=("Segoe UI", 9), 
                                     bg="#263238", fg="#B0BEC5", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.stats_label = tk.Label(self.status_bar, text="Lines: 0 | Chars: 0", 
                                   font=("Segoe UI", 9), 
                                   bg="#263238", fg="#B0BEC5")
        self.stats_label.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Initialize template list
        self.update_template_list()
        
        # Welcome message
        self.show_welcome_message()
    
    def update_template_list(self, event=None):
        """Update template listbox based on selected category."""
        category = self.template_category.get().replace("📘 ", "").replace("🔰 ", "").replace("⚡ ", "").replace("📚 ", "").replace("🎯 ", "").replace("🤖 ", "")
        
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
        
        # Update listbox
        self.template_listbox.delete(0, tk.END)
        for template in templates:
            self.template_listbox.insert(tk.END, template)
        
        if templates:
            self.template_listbox.select_set(0)
    
    def load_selected_template(self):
        """Load the selected template from listbox."""
        selection = self.template_listbox.curselection()
        if not selection:
            self.log_output("⚠️ Please select a lesson or example first!\n")
            return
        
        template_name = self.template_listbox.get(selection[0])
        category = self.template_category.get().replace("📘 ", "").replace("🔰 ", "").replace("⚡ ", "").replace("📚 ", "").replace("🎯 ", "").replace("🤖 ", "")
        
        # Clear editor
        self.code_text.delete("1.0", tk.END)
        
        # Load based on category
        if category == "Python Course":
            if template_name in PYTHON_COURSE:
                self.code_text.insert("1.0", PYTHON_COURSE[template_name])
                self.log_output(f"📚 Loaded: {template_name}\n")
                self.log_output(f"💡 Read the lesson comments, then run the code!\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Beginner":
            if template_name in BEGINNER_EXAMPLES:
                self.code_text.insert("1.0", BEGINNER_EXAMPLES[template_name])
                self.log_output(f"✅ Loaded: {template_name}\n")
                self.log_output(f"💡 Press Ctrl+Enter to run!\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Quick Examples":
            if template_name in CODE_TEMPLATES:
                self.code_text.insert("1.0", CODE_TEMPLATES[template_name])
                self.log_output(f"✓ Loaded: {template_name}\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Python Library":
            if template_name in PYTHON_EXAMPLES:
                self.code_text.insert("1.0", PYTHON_EXAMPLES[template_name])
                self.log_output(f"✓ Loaded: {template_name}\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "Course Labs":
            if template_name in COURSE_LABS:
                self.code_text.insert("1.0", COURSE_LABS[template_name])
                self.log_output(f"✓ Loaded Lab: {template_name}\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        elif category == "DL Roadmap":
            if template_name in ROADMAP_EXAMPLES:
                self.code_text.insert("1.0", ROADMAP_EXAMPLES[template_name])
                self.log_output(f"✓ Loaded Roadmap: {template_name}\n")
                self.status_label.config(text=f"✓ Loaded: {template_name}")
            else:
                self.log_output(f"❌ Template not found: {template_name}\n")
        
        # Update stats
        self.update_cursor_position()
    
    def update_cursor_position(self, event=None):
        """Update cursor position and stats in status bar."""
        # Get cursor position
        cursor_pos = self.code_text.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.line_indicator.config(text=f"Line {line}, Col {int(col)+1}")
        
        # Update stats
        content = self.code_text.get("1.0", tk.END)
        lines = content.count('\n')
        chars = len(content) - 1
        self.stats_label.config(text=f"Lines: {lines} | Chars: {chars}")
    
    def save_code(self):
        """Save current code to file."""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            code = self.code_text.get("1.0", tk.END)
            with open(filename, 'w') as f:
                f.write(code)
            self.log_output(f"💾 Code saved to: {filename}\n")
            self.status_label.config(text=f"✓ Saved: {os.path.basename(filename)}")
    
    def show_welcome_message(self):
        """Display welcome message in output console."""
        self.log_output("=" * 60)
        self.log_output("🎓 PYTHON LEARNING PLATFORM")
        self.log_output("=" * 60)
        self.log_output("")
        self.log_output("Welcome! Here's how to get started:")
        self.log_output("")
        self.log_output("1️⃣  Choose a category (left panel)")
        self.log_output("   📘 Python Course = Complete 14-lesson course")
        self.log_output("   🔰 Beginner = Quick start examples")
        self.log_output("   📚 Python Library = Reference examples")
        self.log_output("   🎯 Course Labs = Hands-on projects")
        self.log_output("")
        self.log_output("2️⃣  Select a lesson/example from the list")
        self.log_output("")
        self.log_output("3️⃣  Click 'Load Selected' or double-click")
        self.log_output("")
        self.log_output("4️⃣  Press Ctrl+Enter or click '▶ Run' to execute!")
        self.log_output("")
        self.log_output("=" * 60)
        self.log_output("")
        self.status_label.config(text="✓ Welcome! Select a lesson to begin")
    
    def execute_code(self):
        """Execute code with better feedback."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            self.log_output("❌ No code to execute\n")
            self.status_label.config(text="❌ No code to run")
            return
        
        self.log_output(f"\n{'='*60}\n")
        self.log_output(f"▶ Executing code...\n")
        self.log_output(f"{'='*60}\n")
        self.status_label.config(text="⏳ Running code...")
        self.root.update()
        
        result = run_code(code, auto_confirm=True)
        self.log_output(result)
        
        # Better feedback
        if "Error" not in result and "Traceback" not in result:
            self.log_output(f"\n{'='*60}\n")
            self.log_output("✅ Success! Your code ran without errors!\n")
            self.log_output(f"{'='*60}\n")
            self.status_label.config(text="✅ Code executed successfully!")
        else:
            self.log_output(f"\n{'='*60}\n")
            self.log_output("⚠️ There was an error. Check the output above.\n")
            self.log_output(f"{'='*60}\n")
            self.status_label.config(text="⚠️ Error occurred")
    
    def clear_output(self):
        """Clear output console."""
        self.output_text.delete("1.0", tk.END)
        self.log_output("✓ Output cleared.\n")
        self.status_label.config(text="✓ Output cleared")

# Run the modern version
if __name__ == "__main__":
    root = tk.Tk()
    root.title("🎓 Python Learning Platform - Modern UI")
    root.geometry("1400x900")
    root.minsize(1200, 700)
    app = ModernUnifiedAppGUI(root)
    root.mainloop()
