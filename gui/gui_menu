import tkinter as tk
from tkinter import Menu, Text, Frame, Button, messagebox, filedialog


class SearchReplaceDialog(tk.Toplevel):
    def __init__(self, parent, text_widget):
        super().__init__(parent)
        self.title("搜尋與取代")
        self.geometry("350x120")
        self.text_widget = text_widget
        self.transient(parent)
        self.resizable(False, False)

        tk.Label(self, text="搜尋:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.search_entry = tk.Entry(self, width=25)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        tk.Label(self, text="取代為:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.replace_entry = tk.Entry(self, width=25)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        btn_frame = Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="搜尋下一個", command=self.search_next).pack(side=tk.TOP, padx=5)
        tk.Button(btn_frame, text="全部取代", command=self.replace_all).pack(side=tk.TOP, padx=5)
        tk.Button(btn_frame, text="關閉", command=self.destroy).pack(side=tk.LEFT, padx=5)

        self.search_entry.focus_set()

    def search_next(self):
        target = self.search_entry.get()
        if not target:
            return
        start_pos = self.text_widget.index(tk.INSERT)
        idx = self.text_widget.search(target, start_pos, tk.END)
        if not idx:
            messagebox.showinfo("搜尋", "找不到更多符合項目。")
            return
        end_idx = f"{idx}+{len(target)}c"
        self.text_widget.tag_remove("search_highlight", "1.0", tk.END)
        self.text_widget.tag_add("search_highlight", idx, end_idx)
        self.text_widget.tag_config("search_highlight", background="yellow")
        self.text_widget.mark_set(tk.INSERT, end_idx)
        self.text_widget.see(idx)

    def replace_all(self):
        target = self.search_entry.get()
        replacement = self.replace_entry.get()
        if not target:
            return
        content = self.text_widget.get("1.0", tk.END)
        new_content = content.replace(target, replacement)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", new_content)
        self.text_widget.tag_remove("search_highlight", "1.0", tk.END)
        messagebox.showinfo("取代", "全部取代完成。")


class App(tk.Tk):
    PY_KEYWORDS = [
        'False', 'class', 'finally', 'is', 'return', 'None', 'continue', 'for',
        'lambda', 'try', 'True', 'def', 'from', 'nonlocal', 'while', 'and', 'del',
        'global', 'not', 'with', 'as', 'elif', 'if', 'or', 'yield', 'assert',
        'else', 'import', 'pass', 'break', 'except', 'in', 'raise'
    ]

    def __init__(self):
        super().__init__()

        self.title("GUI 範例")
        self.geometry("700x550")
        self.current_file = None
        self.toolbar_visible = True
        self.wrap_enabled = False
        self.current_lang = "Python"
        self.LANGUAGES = ["Python", "JavaScript", "Markdown"]
        self.lang_var = tk.StringVar(value=self.current_lang)

        self.PY_KEYWORDS = [
            'False','class','finally','is','return','None','continue','for',
            'lambda','try','True','def','from','nonlocal','while','and','del',
            'global','not','with','as','elif','if','or','yield','assert',
            'else','import','pass','break','except','in','raise'
        ]
        self.JS_KEYWORDS = [
            'break','case','catch','class','const','continue','debugger','default',
            'delete','do','else','export','extends','finally','for','function','if',
            'import','in','instanceof','new','return','super','switch','this','throw',
            'try','typeof','var','void','while','with','yield','let'
        ]

        self._create_menu()
        self._create_toolbar()
        self._create_main_ui()
        self._bind_shortcuts()

    def _create_menu(self):
        menubar = Menu(self)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="開啟", command=self.open_file)
        file_menu.add_command(label="儲存", command=self.save_file)
        file_menu.add_command(label="另存新檔", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="離開", command=self.quit)
        menubar.add_cascade(label="檔案", menu=file_menu)

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="剪下", command=self.cut_text)
        edit_menu.add_command(label="複製", command=self.copy_text)
        edit_menu.add_command(label="貼上", command=self.paste_text)
        edit_menu.add_command(label="全選", command=self.select_all)
        edit_menu.add_command(label="清除", command=self.clear_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="搜尋與取代", command=self.open_search_replace)
        menubar.add_cascade(label="編輯", menu=edit_menu)

        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_command(label="收合/展開工具列", command=self.toggle_toolbar)
        view_menu.add_command(label="切換自動換行", command=self.toggle_wrap)
        menubar.add_cascade(label="檢視", menu=view_menu)

        lang_menu = Menu(menubar, tearoff=0)
        for lang in self.LANGUAGES:
            lang_menu.add_radiobutton(
                label=lang,
                variable=self.lang_var,
                value=lang,
                command=lambda l=lang: self.set_language(l)
            )
        menubar.add_cascade(label="語言", menu=lang_menu)

        self.config(menu=menubar)

    def _create_toolbar(self):
        self.toolbar = Frame(self, bd=1, relief=tk.RAISED)

        Button(self.toolbar, text="✂️ 剪下", command=self.cut_text).pack(side=tk.LEFT, padx=2, pady=2)
        Button(self.toolbar, text="📄 複製", command=self.copy_text).pack(side=tk.LEFT, padx=2, pady=2)
        Button(self.toolbar, text="📋 貼上", command=self.paste_text).pack(side=tk.LEFT, padx=2, pady=2)
        Button(self.toolbar, text="🔍 全選", command=self.select_all).pack(side=tk.LEFT, padx=2, pady=2)
        Button(self.toolbar, text="🧹 清除", command=self.clear_text).pack(side=tk.LEFT, padx=2, pady=2)
        Button(self.toolbar, text="👁️ 輸出", command=self.toggle_output).pack(side=tk.LEFT, padx=10, pady=2)
        Button(self.toolbar, text="📌 收合工具列", command=self.toggle_toolbar).pack(side=tk.RIGHT, padx=10, pady=2)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def _create_main_ui(self):
        # 主框架用 pack 放工具列上方
        self.main_frame = Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # 編輯區 + 捲軸
        editor_frame = Frame(self.main_frame)
        editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.editor_text = Text(editor_frame, height=15, wrap='none', undo=True)
        self.editor_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.editor_scroll_y = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.editor_text.yview)
        self.editor_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor_text.configure(yscrollcommand=self.editor_scroll_y.set)

        self.editor_scroll_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.editor_text.xview)
        self.editor_scroll_x.pack(side=tk.TOP, fill=tk.X)
        self.editor_text.configure(xscrollcommand=self.editor_scroll_x.set)

        # 執行按鈕
        self.action_btn = Button(self.main_frame, text="執行", command=self.perform_action)
        self.action_btn.pack(side=tk.BOTTOM, pady=5)

        # 輸出區 + 捲軸
        output_frame = Frame(self.main_frame)
        output_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.output_text = Text(output_frame, height=8, bg="#f0f0f0", wrap='none')
        self.output_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.output_scroll_y = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=self.output_scroll_y.set)

        self.output_scroll_x = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        self.output_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.output_text.configure(xscrollcommand=self.output_scroll_x.set)

        self.output_visible = True

        # 監聽文字變化，更新語法著色
        self.editor_text.bind("<<Modified>>", self.on_text_changed)

        # 設定語法高亮 tag
        self.editor_text.tag_configure("keyword", foreground="blue")
        self.editor_text.tag_configure("string", foreground="green")
        self.editor_text.tag_configure("comment", foreground="grey")

    def toggle_wrap(self):
        self.wrap_enabled = not self.wrap_enabled
        wrap_mode = 'word' if self.wrap_enabled else 'none'
        self.editor_text.config(wrap=wrap_mode)

    def set_language(self, lang):
        self.current_lang = lang
        self.highlight_syntax()

    def _bind_shortcuts(self):
        self.bind_all("<Control-x>", lambda e: self.cut_text())
        self.bind_all("<Control-c>", lambda e: self.copy_text())
        self.bind_all("<Control-v>", lambda e: self.paste_text())
        self.bind_all("<Control-a>", lambda e: self.select_all())
        self.bind_all("<Control-l>", lambda e: self.clear_text())
        self.bind_all("<Control-f>", lambda e: self.open_search_replace())

    def toggle_output(self):
        if self.output_visible:
            self.output_text.master.pack_forget()
        else:
            self.output_text.master.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        self.output_visible = not self.output_visible

    def toggle_toolbar(self):
        if self.toolbar_visible:
            self.toolbar.pack_forget()
        else:
            self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_visible = not self.toolbar_visible

    def perform_action(self):
        self.output_text.insert(tk.END, "你按下了執行按鈕\n")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor_text.delete(1.0, tk.END)
                self.editor_text.insert(tk.END, content)
                self.current_file = file_path
                self.title(f"GUI 範例 - {file_path}")
                self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("錯誤", f"無法開啟檔案：\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                content = self.editor_text.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("儲存成功", f"檔案已儲存：\n{self.current_file}")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法儲存檔案：\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                content = self.editor_text.get(1.0, tk.END)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.current_file = file_path
                self.title(f"GUI 範例 - {file_path}")
                messagebox.showinfo("儲存成功", f"檔案已儲存：\n{file_path}")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法儲存檔案：\n{e}")

    def cut_text(self):
        try:
            self.copy_text()
            self.editor_text.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def copy_text(self):
        try:
            selected_text = self.editor_text.get("sel.first", "sel.last")
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            clipboard_text = self.clipboard_get()
            self.editor_text.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            pass

    def select_all(self):
        self.editor_text.tag_add(tk.SEL, "1.0", tk.END)
        self.editor_text.mark_set(tk.INSERT, "1.0")
        self.editor_text.see(tk.INSERT)

    def clear_text(self):
        self.editor_text.delete("1.0", tk.END)

    def open_search_replace(self):
        SearchReplaceDialog(self, self.editor_text)

    def on_text_changed(self, event=None):
        self.editor_text.after(100, self.highlight_syntax)
        self.editor_text.edit_modified(0)

    def highlight_syntax(self):
        # 移除先前標記
        self.editor_text.tag_remove("keyword", "1.0", tk.END)
        self.editor_text.tag_remove("string", "1.0", tk.END)
        self.editor_text.tag_remove("comment", "1.0", tk.END)

        content = self.editor_text.get("1.0", tk.END)
        lines = content.split('\n')

        for i, line in enumerate(lines):
            index_start = f"{i+1}.0"
            # 簡易處理：找註解 #
            comment_pos = line.find("#")
            if comment_pos >= 0:
                start_idx = f"{i+1}.{comment_pos}"
                end_idx = f"{i+1}.end"
                self.editor_text.tag_add("comment", start_idx, end_idx)
                line = line[:comment_pos]

            # 簡易處理：字串
            # 只簡單搜尋 ' 和 " 包住的字串
            idx = 0
            while idx < len(line):
                if line[idx] in ("'", '"'):
                    quote = line[idx]
                    start_idx = idx
                    idx += 1
                    while idx < len(line) and line[idx] != quote:
                        # 跳過跳脫字元
                        if line[idx] == "\\":
                            idx += 2
                        else:
                            idx += 1
                    end_idx = idx
                    if end_idx < len(line):
                        end_idx += 1
                    start_tag = f"{i+1}.{start_idx}"
                    end_tag = f"{i+1}.{end_idx}"
                    self.editor_text.tag_add("string", start_tag, end_tag)
                    idx = end_idx
                else:
                    idx += 1

            # 簡易處理：關鍵字
            words = line.split()
            idx = 0
            for word in words:
                start_idx = line.find(word, idx)
                end_idx = start_idx + len(word)
                idx = end_idx
                if self.current_lang == "Python" and word in self.PY_KEYWORDS:
                    start_tag = f"{i+1}.{start_idx}"
                    end_tag = f"{i+1}.{end_idx}"
                    self.editor_text.tag_add("keyword", start_tag, end_tag)
                elif self.current_lang == "JavaScript" and word in self.JS_KEYWORDS:
                    start_tag = f"{i+1}.{start_idx}"
                    end_tag = f"{i+1}.{end_idx}"
                    self.editor_text.tag_add("keyword", start_tag, end_tag)
                # Markdown 語法高亮可以自己擴充

if __name__ == "__main__":
    app = App()
    app.mainloop()
