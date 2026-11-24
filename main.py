import time
import tkinter as tk
from tkinter import messagebox

tasks = []  # list of (text, deadline)


def add_task(event=None):
    text = todo_entry.get().strip()
    try:
        seconds = int(seconds_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Time must be a whole number of seconds.")
        return
    if not text or not (0 < seconds < 999):
        messagebox.showerror("Invalid input", "Enter a task and a time between 1 and 998 seconds.")
        return

    tasks.append((text, time.time() + seconds))
    todo_entry.delete(0, tk.END)
    seconds_entry.delete(0, tk.END)
    todo_entry.focus_set()
    refresh_list()


def refresh_list():
    todolist.delete(0, tk.END)
    for text, deadline in tasks:
        remaining = max(0, int(deadline - time.time()))
        todolist.insert(tk.END, f"[{text}] Time left: {remaining} seconds")


def tick():
    now = time.time()
    due = [t for t in tasks if t[1] <= now]
    tasks[:] = [t for t in tasks if t[1] > now]
    refresh_list()
    for text, _ in due:
        messagebox.showinfo("Notification", f"Time for: {text}")
    app.after(1000, tick)


app = tk.Tk()
app.geometry("480x480")
app.title("Todolist Reminder")

tk.Label(app, text="Enter work to do:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
tk.Label(app, text="Time (seconds):").grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

todo_entry = tk.Entry(app, width=30)
seconds_entry = tk.Entry(app, width=12)
todo_entry.grid(row=1, column=0, padx=10, sticky="w")
seconds_entry.grid(row=1, column=1, padx=10, sticky="w")

tk.Button(app, text="Add task", fg="#fff", bg="#6186AC", command=add_task).grid(row=2, column=0, padx=10, pady=10, sticky="ew")
tk.Button(app, text="Exit", fg="#fff", bg="#EB6464", command=app.destroy).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

todolist = tk.Listbox(app)
todolist.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
app.rowconfigure(3, weight=1)
app.columnconfigure(0, weight=1)

app.bind("<Return>", add_task)
tick()
app.mainloop()