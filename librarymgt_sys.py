import tkinter as tk
from datetime import date, timedelta

library = {}

def issue_book():
    name = entry_name.get()
    book = entry_book.get()
    author = entry_author.get()

    if name == "" or book == "" or author == "":
        result_label.config(text="❌ Please fill all fields", fg="red")
        return

    issue_date = date.today()
    return_date = issue_date + timedelta(days=7)

    library[book] = {
        "Name": name,
        "Author": author,
        "Issue Date": issue_date,
        "Return Date": return_date
    }

    result_label.config(
        text=f"✅ Book Issued!\nIssue: {issue_date}\nReturn: {return_date}",
        fg="green"
    )

    entry_name.delete(0, tk.END)
    entry_book.delete(0, tk.END)
    entry_author.delete(0, tk.END)

def view_books():
    text_area.delete("1.0", tk.END)
    if not library:
        text_area.insert(tk.END, "No books issued yet.")
    else:
        for book, details in library.items():
            text_area.insert(
                tk.END,
                f"Book Name: {book}\n"
                f"Author Name: {details['Author']}\n"
                f"Student Name: {details['Name']}\n"
                f"Issue Date: {details['Issue Date']}\n"
                f"Return Date: {details['Return Date']}\n"
                "-----------------------------\n"
            )

# Main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("420x500")

# Title
tk.Label(root, text="📚 Library Management System", font=("Arial", 16, "bold")).pack(pady=10)

# Student Name
tk.Label(root, text="Student Name").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

# Book Name
tk.Label(root, text="Book Name").pack()
entry_book = tk.Entry(root, width=30)
entry_book.pack(pady=5)

# Author Name
tk.Label(root, text="Author Name").pack()
entry_author = tk.Entry(root, width=30)
entry_author.pack(pady=5)

# Buttons
tk.Button(root, text="Issue Book", command=issue_book, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="View Issued Books", command=view_books, bg="blue", fg="white").pack(pady=5)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 10))
result_label.pack(pady=10)

# Text area
text_area = tk.Text(root, width=48, height=10)
text_area.pack(pady=10)

root.mainloop()
