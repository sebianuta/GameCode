import tkinter as tk
from autoclicker import AutoClicker
import threading
import pyautogui
import time

class AutoclickerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Autoclicker")
        self.clicker = AutoClicker()
        self.running = False

        # Number of clicks
        tk.Label(master, text="Number of Clicks:").pack()
        self.click_count_var = tk.IntVar(value=10)
        self.click_count_spinbox = tk.Spinbox(master, from_=1, to=999999999, textvariable=self.click_count_var, width=10)
        self.click_count_spinbox.pack(pady=5)
        self.infinite_clicks_var = tk.BooleanVar(value=False)
        self.infinite_clicks_check = tk.Checkbutton(master, text="Infinite clicks", variable=self.infinite_clicks_var, command=self.toggle_infinite_clicks)
        self.infinite_clicks_check.pack()

        # Click rate (always clicks per second)
        tk.Label(master, text="Rate (clicks per second):").pack()
        self.rate_var = tk.DoubleVar(value=5)
        self.rate_entry = tk.Entry(master, textvariable=self.rate_var, width=5)
        self.rate_entry.pack(pady=5)

        # Time limit
        time_frame = tk.Frame(master)
        tk.Label(time_frame, text="Time Limit (seconds):").pack(side=tk.LEFT)
        self.time_limit_var = tk.IntVar(value=10)
        self.time_limit_spinbox = tk.Spinbox(time_frame, from_=1, to=9999, textvariable=self.time_limit_var, width=5)
        self.time_limit_spinbox.pack(side=tk.LEFT)
        self.never_stop_var = tk.BooleanVar(value=False)
        self.never_stop_check = tk.Checkbutton(time_frame, text="Never stop", variable=self.never_stop_var, command=self.toggle_time_limit)
        self.never_stop_check.pack(side=tk.LEFT, padx=5)
        time_frame.pack(pady=5)

        # Start/Stop buttons
        self.start_button = tk.Button(master, text="Start", command=self.start_clicking)
        self.start_button.pack(pady=10)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def toggle_time_limit(self):
        if self.never_stop_var.get():
            self.time_limit_spinbox.config(state=tk.DISABLED)
        else:
            self.time_limit_spinbox.config(state=tk.NORMAL)

    def toggle_infinite_clicks(self):
        if self.infinite_clicks_var.get():
            self.click_count_spinbox.config(state=tk.DISABLED)
        else:
            self.click_count_spinbox.config(state=tk.NORMAL)

    def click_loop(self, clicks, interval, time_limit):
        start_time = time.time()
        i = 0
        next_click = start_time
        while self.clicker.is_clicking():
            now = time.time()
            if not self.infinite_clicks_var.get() and i >= clicks:
                break
            if time_limit is not None and (now - start_time) >= time_limit:
                break
            pyautogui.click()
            i += 1
            next_click += interval
            sleep_time = next_click - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_click = time.time()  # If we're behind, reset next_click
        self.stop_clicking()

    def start_clicking(self):
        if not self.clicker.is_clicking():
            clicks = self.click_count_var.get()
            try:
                rate = float(self.rate_var.get())
            except Exception:
                tk.messagebox.showerror("Invalid Rate", "Rate must be a number.")
                return
            if rate <= 0:
                tk.messagebox.showerror("Invalid Rate", "Rate must be greater than 0.")
                return
            interval = 1.0 / rate  # Always clicks per second
            time_limit = None if self.never_stop_var.get() else self.time_limit_var.get()
            self.clicker.start_clicking()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            threading.Thread(target=self.click_loop, args=(clicks, interval, time_limit), daemon=True).start()

    def stop_clicking(self):
        if self.clicker.is_clicking():
            self.clicker.stop_clicking()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    gui = AutoclickerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
