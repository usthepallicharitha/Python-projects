import tkinter as tk
import time

# ================= DATA =================
TEXT = (
    "Leadership is not about a title or position. "
    "It is about influence inspiration and impact. "
    "Great leaders create more leaders not followers."
)

leaderboard = []
start_time = 0
timer_running = False

# ================= FUNCTIONS =================
def start_test():
    global start_time, timer_running

    name = name_entry.get().strip()
    if name == "":
        result_label.config(text="❗ Please enter your name")
        return

    entry.delete("1.0", tk.END)
    result_label.config(text="")
    start_time = time.time()
    timer_running = True
    update_timer()

def update_timer():
    if not timer_running:
        return

    elapsed = time.time() - start_time
    remaining = 30 - int(elapsed)

    timer_label.config(text=f"⏱ Time Left: {remaining} sec")

    if remaining <= 0:
        stop_test()
    else:
        root.after(1000, update_timer)

def stop_test():
    global timer_running
    timer_running = False

    typed_text = entry.get("1.0", tk.END).strip()
    name = name_entry.get().strip()

    words = len(typed_text.split())
    wpm = round((words / 30) * 60, 2)

    leaderboard.append((name, wpm))
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    show_leaderboard()

def show_leaderboard():
    board = "🏆 LEADERBOARD (Badges for Everyone)\n\n"

    badges = {
        0: "🥇 GOLD",
        1: "🥈 SILVER",
        2: "🥉 BRONZE",
        3: "🟦 PLATINUM",
        4: "🟩 DIAMOND"
    }

    for i, (name, score) in enumerate(leaderboard):
        badge = badges.get(i, "🟨 PARTICIPANT")
        board += f"{i+1}. {badge} - {name} ({score} WPM)\n"

    result_label.config(text=board)

# ================= GUI =================
root = tk.Tk()
root.title("Typing Master – 30 Seconds Challenge")
root.geometry("800x520")

tk.Label(root, text="Typing Master Championship",
         font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text="Enter Your Name:",
         font=("Arial", 11)).pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Label(root, text=TEXT, wraplength=760,
         font=("Arial", 12)).pack(pady=10)

timer_label = tk.Label(root, text="⏱ Time Left: 30 sec",
                       font=("Arial", 14, "bold"))
timer_label.pack(pady=5)

entry = tk.Text(root, height=5, width=90)
entry.pack(pady=10)

tk.Button(root, text="START TEST", font=("Arial", 11, "bold"),
          command=start_test).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12),
                        justify="left")
result_label.pack(pady=10)

root.mainloop()
