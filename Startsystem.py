import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
import time

class ProgressBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading...")
        self.root.geometry("300x100")
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=20, padx=20)
        self.label = tk.Label(self.root, text="Starting...")
        self.label.pack()
        self.process = None
        self.start_progress()

    def start_progress(self):
        self.process = subprocess.Popen(
            [r"runtime\python.exe", "mainpage.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )
        threading.Thread(target=self.monitor_output).start()
        self.update_progress()

    def monitor_output(self):
        try:
            current_directory = os.getcwd()
            print(f"Current directory: {current_directory}")
            flag_path = os.path.join(current_directory, "loading_complete.flag")
            while self.process.poll() is None:
                if os.path.exists(flag_path):
                    self.root.after(0, self.close_progress)
                    break
                time.sleep(0.5)
            self.process.stdout.close()
        except Exception as e:
            print(f"Error reading process output: {e}")
            self.label.config(text="Error reading output!")

    def update_progress(self):
        current_progress = self.progress_var.get()
        if current_progress < 100:
            self.progress_var.set(current_progress + 0.4)
            self.root.after(50, self.update_progress)
        else:
            self.label.config(text="Almost done...")

    def close_progress(self):
        self.progress_var.set(100)
        self.label.config(text="Done!")
        self.root.after(500, self.root.destroy)
        if os.path.exists("loading_complete.flag"):
            os.remove("loading_complete.flag")  # 删除标志文件

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressBarApp(root)
    root.mainloop()
