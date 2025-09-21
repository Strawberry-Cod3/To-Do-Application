#Bascic GUI To-DO List
#Import required Data
import json
import os
import tkinter as tk
from tkinter import messagebox, Scrollbar
from colorama import init, Fore, Style

#Initalizes Colorama (for console fallback if needed)
init(autoreset=True)

FILENAME = "tasks.json"

#Load tasks
if os.path.exists(FILENAME):
    with open(FILENAME) as f:
        try:
            tasks = json.load(f)
        except json.decoder.JSONDecodeError:
            tasks = []
else:
    tasks = []

#Save Tasks
def save_tasks():
    with open(FILENAME, 'w') as f:
        json.dump(tasks, f, indent=4)

def update_listbox():
    listbox.delete(0, tk.END)
    for t in tasks:
        status = "✔️" if t["done"] else "❌"
        # Color-coded display: green for done, white for pending
        color_tag = "done" if t["done"] else "pending"
        listbox.insert(tk.END, f"{t['task']} {status}")
        listbox.itemconfig(tk.END, {'fg': "green" if t["done"] else "white"})

def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append({"task": task_text, "done": False})
        task_entry.delete(0, tk.END)
        save_tasks()
        update_listbox()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def mark_done():
    try:
        idx = listbox.curselection()[0]
        tasks[idx]["done"] = True
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task fist!")

def delete_task():
    try:
        idx = listbox.curselection()[0]
        tasks.pop(idx)
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task fist!")

#Tkinter GUI Setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")
root.configure(bg="black")

task_entry = tk.Entry(root, width=40, bg="black", fg="white")
task_entry.pack(pady=10)

#Add Buttons
add_btn = tk.Button(root, text="Add Task", width=20, command=add_task, bg="black", fg="white")
add_btn.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=15, bg="black", fg="white", selectbackground="#61AFEF")
listbox.pack(pady=10)

done_btn = tk.Button(root, text="Mark Done", width=20, command=mark_done, bg="black", fg="white")
done_btn.pack(side=tk.LEFT, padx=20)

delete_btn = tk.Button(root, text="Delete Task", width=20, command=delete_task, bg="black", fg="white")
delete_btn.pack(side=tk.LEFT, padx=20)

update_listbox()
root.mainloop()