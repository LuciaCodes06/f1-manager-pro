import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("f1.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    team TEXT,
    points INTEGER
)
""")
conn.commit()

def add_driver():
    name = name_entry.get().strip()
    team = team_entry.get().strip()
    points = points_entry.get().strip()

    if not name or name == "Driver Name":
        messagebox.showerror("Error", "Enter a valid driver name")
        return
    if not team or team == "Team":
        messagebox.showerror("Error", "Enter a valid team")
        return
    if not points.isdigit():
        messagebox.showerror("Error", "Points must be a number")
        return

    cursor.execute(
        "INSERT INTO drivers (name, team, points) VALUES (?, ?, ?)",
        (name, team, int(points))
    )
    conn.commit()
    clear_inputs()
    load_drivers()


def load_drivers():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM drivers ORDER BY points DESC")
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"{row[1]} | {row[2]} | {row[3]} pts")


def delete_driver():
    try:
        index = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Warning", "Select a driver first")
        return

    cursor.execute("SELECT id FROM drivers ORDER BY points DESC")
    driver_id = cursor.fetchall()[index][0]

    cursor.execute("DELETE FROM drivers WHERE id=?", (driver_id,))
    conn.commit()
    load_drivers()


def add_points():
    try:
        index = listbox.curselection()[0]
    except IndexError:
        messagebox.showwarning("Warning", "Select a driver first")
        return

    cursor.execute("SELECT id, points FROM drivers ORDER BY points DESC")
    driver = cursor.fetchall()[index]

    new_points = driver[1] + 10

    cursor.execute(
        "UPDATE drivers SET points=? WHERE id=?",
        (new_points, driver[0])
    )
    conn.commit()
    load_drivers()


def search_driver():
    keyword = search_entry.get().strip()

    listbox.delete(0, tk.END)

    cursor.execute(
        "SELECT * FROM drivers WHERE name LIKE ? ORDER BY points DESC",
        ('%' + keyword + '%',)
    )

    results = cursor.fetchall()

    if not results:
        messagebox.showinfo("Info", "No drivers found")

    for row in results:
        listbox.insert(tk.END, f"{row[1]} | {row[2]} | {row[3]} pts")


def clear_inputs():
    name_entry.delete(0, tk.END)
    team_entry.delete(0, tk.END)
    points_entry.delete(0, tk.END)


def on_closing():
    conn.close()
    root.destroy()


root = tk.Tk()
root.title("F1 Manager PRO")
root.geometry("400x500")

tk.Label(root, text="F1 Manager", font=("Arial", 16)).pack(pady=10)

name_entry = tk.Entry(root)
name_entry.pack(pady=3)
name_entry.insert(0, "Driver Name")

team_entry = tk.Entry(root)
team_entry.pack(pady=3)
team_entry.insert(0, "Team")

points_entry = tk.Entry(root)
points_entry.pack(pady=3)
points_entry.insert(0, "Points")

def clear_placeholder(entry, text):
    if entry.get() == text:
        entry.delete(0, tk.END)

name_entry.bind("<FocusIn>", lambda e: clear_placeholder(name_entry, "Driver Name"))
team_entry.bind("<FocusIn>", lambda e: clear_placeholder(team_entry, "Team"))
points_entry.bind("<FocusIn>", lambda e: clear_placeholder(points_entry, "Points"))

tk.Button(root, text="Add Driver", command=add_driver).pack(pady=5)

search_entry = tk.Entry(root)
search_entry.pack(pady=3)
search_entry.insert(0, "Search Driver")

search_entry.bind("<FocusIn>", lambda e: clear_placeholder(search_entry, "Search Driver"))

tk.Button(root, text="Search", command=search_driver).pack(pady=5)
tk.Button(root, text="Show All", command=load_drivers).pack(pady=5)

listbox = tk.Listbox(root, width=45, font=("Consolas", 10))
listbox.pack(pady=10)

tk.Button(root, text="+10 Points", command=add_points).pack(pady=3)
tk.Button(root, text="Delete Driver", command=delete_driver).pack(pady=3)

load_drivers()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()