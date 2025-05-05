import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import sqlite3

# === Database Setup ===
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        is_completed INTEGER DEFAULT 0
    )
''')
conn.commit()

# === Main App ===
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌊 Todo App")
        self.root.geometry("600x550")
        self.root.configure(bg="#f7f9fc")
        self.custom_font = ("Segoe UI", 11)

        self.draw_background()
        self.setup_ui()
        self.load_tasks()

    def draw_background(self):
        canvas = tk.Canvas(self.root, width=600, height=160, highlightthickness=0)
        canvas.pack(fill="x")
        canvas.create_rectangle(0, 0, 600, 160, fill="#6C63FF", outline="")
        canvas.create_arc(-100, 40, 700, 300, start=0, extent=180, fill="#7B72FF", outline="#7B72FF")
        canvas.create_arc(-150, 90, 750, 360, start=0, extent=180, fill="#857DFF", outline="#857DFF")

    def setup_ui(self):
        frame = tk.Frame(self.root, bg="#ffffff", bd=0)
        frame.place(x=20, y=120, width=560, height=400)

        # Task entry
        tk.Label(frame, text="Task", bg="#ffffff", font=self.custom_font).grid(row=0, column=0, sticky="w", padx=10)
        self.task_entry = tk.Entry(frame, width=30, font=self.custom_font)
        self.task_entry.grid(row=1, column=0, padx=10, pady=5)

        # Date entry
        tk.Label(frame, text="Due Date (YYYY-MM-DD)", bg="#ffffff", font=self.custom_font).grid(row=0, column=1, sticky="w", padx=10)
        self.date_entry = tk.Entry(frame, width=20, font=self.custom_font)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)

        # Priority selector
        tk.Label(frame, text="Priority", bg="#ffffff", font=self.custom_font).grid(row=2, column=0, sticky="w", padx=10)
        self.priority = ttk.Combobox(frame, values=["Low", "Medium", "High"], state="readonly", font=self.custom_font)
        self.priority.grid(row=3, column=0, padx=10, pady=5)
        self.priority.set("Medium")

        # Buttons
        self.add_btn = tk.Button(frame, text="➕ Add Task", command=self.add_task, bg="#6C63FF", fg="white", font=self.custom_font, bd=0)
        self.add_btn.grid(row=3, column=1, padx=10)

        self.task_listbox = tk.Listbox(frame, font=self.custom_font, width=70, height=12)
        self.task_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.delete_btn = tk.Button(frame, text="🗑️ Delete", command=self.delete_task, bg="#ff4d4d", fg="white", font=self.custom_font, bd=0)
        self.delete_btn.grid(row=5, column=0, pady=10)

        self.complete_btn = tk.Button(frame, text="✅ Complete", command=self.complete_task, bg="#2ecc71", fg="white", font=self.custom_font, bd=0)
        self.complete_btn.grid(row=5, column=1)

    def add_task(self):
        task = self.task_entry.get().strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority.get()

        if not task or not due_date:
            messagebox.showwarning("Input Error", "Please fill in both task and date.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Date Error", "Use YYYY-MM-DD format.")
            return

        cursor.execute("INSERT INTO tasks (task, due_date, priority) VALUES (?, ?, ?)",
                       (task, due_date, priority))
        conn.commit()
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, task, due_date, priority, is_completed FROM tasks")
        for row in cursor.fetchall():
            task_id, task, due, prio, done = row
            status = "✅ " if done else ""
            color = {"Low": "#2ecc71", "Medium": "#f1c40f", "High": "#e74c3c"}[prio]
            display = f"{status}[{prio}] {task} (Due: {due})"
            self.task_listbox.insert(tk.END, display)
            self.task_listbox.itemconfig(tk.END, fg=color)

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            cursor.execute("SELECT id FROM tasks")
            task_id = cursor.fetchall()[index][0]
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Select Task", "Select a task to delete.")

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            cursor.execute("SELECT id FROM tasks")
            task_id = cursor.fetchall()[index][0]
            cursor.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
            conn.commit()
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Select Task", "Select a task to mark as complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
