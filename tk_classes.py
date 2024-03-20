import tkinter as tk
from config import *


class HoverButton(tk.Button):
    def __init__(self,
                 *args,
                 bg1,
                 bg2,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.config(bg=bg1)
        self.bg1 = bg1
        self.bg2 = bg2
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def enter(self, event):
        self.config(bg=self.bg2)

    def leave(self, event):
        self.config(bg=self.bg1)


class TaskButton(tk.Button):
    def __init__(self,
                 *args,
                 task_name,
                 task_description,
                 creation_time,
                 priority,
                 root_window,
                 width=int(WIDTH / 6) - 4 * PADX,
                 height=int(HEIGHT / 10),
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.task_name = task_name
        self.text = task_name
        self.task_description = task_description
        self.creation_time = creation_time
        self.priority = priority
        self.width = width
        self.height = height
        self.root_window = root_window
        self.configure(command=self.place_task_details)

    def place_task_details(self):
        task_frame = tk.Frame(master=self.root_window, name='taskdetails', width=int(self.width / 6),
                              height=self.height - 2 * PADY, bg='dark grey')
        task_frame.place(x=600, y=100)

        tk.Label(task_frame, text=self.task_name).grid(row=1, column=0, padx=PADX, pady=PADY)
        tk.Label(task_frame, text=self.task_description).grid(row=2, column=0, padx=PADX, pady=PADY)
        tk.Label(task_frame, text=self.creation_time).grid(row=3, column=0, padx=PADX, pady=PADY)
        tk.Label(task_frame, text=self.priority).grid(row=4, column=0, padx=PADX, pady=PADY)

        def close_task():
            task_frame.destroy()

        close_button = tk.Button(task_frame, text='Close Task',
                                 command=close_task, fg='black',
                                 bg="light grey")

        def enter(event):
            close_button.config(bg='#990000')

        def leave(event):
            close_button.config(bg='light grey')

        close_button.bind("<Enter>", enter)
        close_button.bind("<Leave>", leave)
        close_button.grid(row=0, column=2, padx=PADX, pady=PADY, sticky='ne')
