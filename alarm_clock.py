import tkinter as tk
import time
import winsound
from threading import Thread
from datetime import datetime, timedelta

alarm_time = None
alarm_running = False

# Update digital clock (AM/PM)
def update_clock():
    current_time = time.strftime("%I:%M:%S %p")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

# Alarm checker
def check_alarm():
    global alarm_running
    while alarm_running:
        time.sleep(1)
        if time.strftime("%I:%M %p") == alarm_time:
            status_label.config(text="⏰ Wake Up!", fg="red")
            winsound.Beep(1000, 5000)
            alarm_running = False

# Set alarm
def set_alarm():
    global alarm_time, alarm_running
    alarm_time = alarm_entry.get()
    alarm_running = True
    status_label.config(text="Alarm Set", fg="green")
    Thread(target=check_alarm, daemon=True).start()

# Stop alarm
def stop_alarm():
    global alarm_running
    alarm_running = False
    status_label.config(text="Alarm Stopped", fg="black")

# Snooze alarm (5 minutes)
def snooze_alarm():
    global alarm_time, alarm_running
    now = datetime.now() + timedelta(minutes=5)
    alarm_time = now.strftime("%I:%M %p")
    alarm_running = True
    status_label.config(text="Snoozed for 5 minutes", fg="orange")
    Thread(target=check_alarm, daemon=True).start()

# Tkinter window
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("380x320")
root.resizable(False, False)

# Clock display
clock_label = tk.Label(root, font=("Arial", 36), fg="blue")
clock_label.pack(pady=20)

# Alarm input
alarm_entry = tk.Entry(root, font=("Arial", 14), justify="center")
alarm_entry.pack()
alarm_entry.insert(0, "07:00 AM")

# Buttons
set_btn = tk.Button(root, text="Set Alarm", font=("Arial", 12), width=15, command=set_alarm)
set_btn.pack(pady=5)

snooze_btn = tk.Button(root, text="Snooze (5 min)", font=("Arial", 12), width=15, command=snooze_alarm)
snooze_btn.pack(pady=5)

stop_btn = tk.Button(root, text="Stop Alarm", font=("Arial", 12), width=15, command=stop_alarm)
stop_btn.pack(pady=5)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

update_clock()
root.mainloop()
