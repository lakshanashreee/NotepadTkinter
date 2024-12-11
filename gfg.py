import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox

class Notepad:

    def __init__(self):
        self.root = Tk()
        self.root.title("Advanced Notepad")
        self.root.geometry("800x600")

        self.notebooks = {}  # Dictionary to manage notebooks and their sections
        self.current_text_area = None
        self.init_ui()

    def init_ui(self):
        # Create menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Notebook", command=self.new_notebook)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: self.current_text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.current_text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.current_text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Find and Replace", command=self.find_and_replace)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Dark Mode", command=self.dark_mode)
        view_menu.add_command(label="Light Mode", command=self.light_mode)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Advanced Notepad\nDeveloped By Lakshana Shree S\nMail id- lakshanashree.s.2023.cse@ritchennai.edu.in"))
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Tab control for notebooks
        self.notebook_control = ttk.Notebook(self.root)
        self.notebook_control.pack(fill=BOTH, expand=1)
        self.new_notebook()  # Initialize with one notebook

        # Status bar
        self.status_bar = Label(self.root, text="Words: 0", anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

    def new_notebook(self):
        notebook_name = f"Notebook {len(self.notebooks) + 1}"
        notebook_frame = Frame(self.notebook_control)
        self.notebooks[notebook_name] = notebook_frame
        self.notebook_control.add(notebook_frame, text=notebook_name)
        self.add_section(notebook_frame, "Main Section")

    def add_section(self, notebook_frame, section_name):
        text_area = Text(notebook_frame, wrap=WORD)
        text_area.pack(fill=BOTH, expand=1)
        text_area.bind("<<Modified>>", self.update_status_bar)
        self.current_text_area = text_area

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.current_text_area.delete(1.0, END)
            self.current_text_area.insert(1.0, content)
            self.root.title(f"{file_path} - Notepad")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.current_text_area.get(1.0, END))
            self.root.title(f"{file_path} - Notepad")

    def save_as_file(self):
        self.save_file()

    def find_and_replace(self):
        find_replace_window = Toplevel(self.root)
        find_replace_window.title("Find and Replace")
        find_replace_window.geometry("300x150")

        Label(find_replace_window, text="Find:").grid(row=0, column=0, padx=10, pady=10)
        find_entry = Entry(find_replace_window, width=20)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(find_replace_window, text="Replace:").grid(row=1, column=0, padx=10, pady=10)
        replace_entry = Entry(find_replace_window, width=20)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        def replace_text():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.current_text_area.get(1.0, END)
            updated_content = content.replace(find_text, replace_text)
            self.current_text_area.delete(1.0, END)
            self.current_text_area.insert(1.0, updated_content)

        Button(find_replace_window, text="Replace", command=replace_text).grid(row=2, column=1, pady=10)

    def dark_mode(self):
        self.root.configure(bg="#2e2e2e")
        self.current_text_area.configure(bg="#1e1e1e", fg="white", insertbackground="white")
        self.status_bar.configure(bg="#2e2e2e", fg="white")

    def light_mode(self):
        self.root.configure(bg="white")
        self.current_text_area.configure(bg="white", fg="black", insertbackground="black")
        self.status_bar.configure(bg="white", fg="black")

    def update_status_bar(self, event=None):
        content = self.current_text_area.get(1.0, END)
        words = len(content.split())
        self.status_bar.config(text=f"Words: {words}")
        self.current_text_area.edit_modified(False)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Notepad()
    app.run()
