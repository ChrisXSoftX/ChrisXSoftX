import os
import tkinter as tk
from tkinter import filedialog, messagebox, font as tkFont
import ctypes
import platform

class ModernWindow:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # removes title bar
        self.root.geometry("700x450")
        self.root.config(bg="#e0e5ec")

        # Set window style for rounded corners (Windows 11)
        if platform.system() == "Windows":
            try:
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(1)), 4)
                margins = ctypes.wintypes.MARGINS(-1, -1, -1, -1)
                ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
            except:
                pass  # fallback if API fails

        self.offset_x = 0
        self.offset_y = 0

        # Title bar for dragging the window
        self.title_bar = tk.Frame(self.root, bg="#d1d9e6", relief='raised', height=30)
        self.title_bar.pack(fill=tk.X)
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        # Close button
        close_btn = tk.Button(self.title_bar, text="✖", bg="#d1d9e6", bd=0, fg="#333", font=("Segoe UI", 10),
                              activebackground="#f66", command=self.root.destroy)
        close_btn.pack(side="right", padx=5, pady=2)

        self.custom_font = tkFont.Font(family="Segoe UI", size=10)

        # Main app container (neumorphic styling)
        self.container = tk.Frame(self.root, bg="#e0e5ec", bd=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.current_theme = {
            "bg": "#e0e5ec",
            "fg": "#333333",
            "entry_bg": "#f0f0f3",
            "button_bg": "#e0e5ec",
            "shadow": "#a3b1c6"
        }

        # Base path input
        self.make_label("📁 Base Path:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.base_entry = self.make_entry()
        self.base_entry.grid(row=1, column=1, pady=5)
        self.make_button("🗂️", self.browse_base).grid(row=1, column=2, padx=5)

        # Target path input
        self.make_label("📄 Target Path:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.target_entry = self.make_entry()
        self.target_entry.grid(row=2, column=1, pady=5)
        self.make_button("🗂️", self.browse_target).grid(row=2, column=2, padx=5)

        # Convert button
        self.convert_btn = self.make_button("🚀 Convert Path", self.convert_path, width=20)
        self.convert_btn.grid(row=3, column=1, pady=15)

        # Result text area
        self.make_label("🔗 Relative Path:").grid(row=4, column=0, sticky='ne', padx=5)
        self.result_text = tk.Text(self.container, height=3, width=50, wrap='word', state='disabled',
                                   font=self.custom_font, relief='flat', bd=5)
        self.result_text.grid(row=4, column=1, pady=5)
        self.make_button("📋 Copy", self.copy_to_clipboard).grid(row=4, column=2, padx=5)

        # Theme toggle button
        self.toggle_btn = self.make_button("🌗 Toggle Theme", self.toggle_theme)
        self.toggle_btn.grid(row=0, column=1, pady=10)

        # Apply theme to all widgets
        self.apply_theme()

    def apply_theme(self):
        theme = self.current_theme
        self.root.configure(bg=theme["bg"])
        self.container.configure(bg=theme["bg"])

        for widget in self.container.winfo_children():
            cls = widget.__class__.__name__
            if cls == "Entry" or cls == "Text":
                widget.configure(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
            elif cls == "Label":
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            elif cls == "Button":
                widget.configure(bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["entry_bg"])

    def toggle_theme(self):
        # Toggle between light and dark theme
        if self.current_theme["bg"] == "#e0e5ec":
            self.current_theme = {
                "bg": "#2E2E2E",
                "fg": "#FFFFFF",
                "entry_bg": "#3A3A3A",
                "button_bg": "#2E2E2E",
                "shadow": "#1a1a1a"
            }
        else:
            self.current_theme = {
                "bg": "#e0e5ec",
                "fg": "#333333",
                "entry_bg": "#f0f0f3",
                "button_bg": "#e0e5ec",
                "shadow": "#a3b1c6"
            }
        self.apply_theme()

    def make_label(self, text):
        return tk.Label(self.container, text=text, font=self.custom_font, bg=self.current_theme["bg"])

    def make_entry(self):
        return tk.Entry(self.container, width=50, font=self.custom_font, relief='flat', bd=5)

    def make_button(self, text, command, width=None):
        button = tk.Button(self.container, text=text, command=command, font=self.custom_font,
                           relief='flat', bd=4, width=width)
        button.bind("<Enter>", self.on_hover)
        button.bind("<Leave>", self.on_leave)
        return button

    def on_hover(self, event):
        event.widget.config(bg="#f0f0f3")

    def on_leave(self, event):
        event.widget.config(bg=self.current_theme["button_bg"])

    def browse_base(self):
        path = filedialog.askdirectory(title="Select Base Directory")
        if path:
            self.base_entry.delete(0, tk.END)
            self.base_entry.insert(0, path)

    def browse_target(self):
        path = filedialog.askopenfilename(title="Select Target File")
        if path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, path)

    def convert_path(self):
        base = self.base_entry.get().strip()
        target = self.target_entry.get().strip()
        try:
            relative_path = os.path.relpath(target, base)
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, relative_path)
            self.result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        result = self.result_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_append(result)
            messagebox.showinfo("Copied", "✅ Relative path copied to clipboard.")
        else:
            messagebox.showwarning("Empty", "⚠️ No path to copy.")

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.offset_x
        y = self.root.winfo_pointery() - self.offset_y
        self.root.geometry(f'+{x}+{y}')


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernWindow(root)
    root.mainloop()
