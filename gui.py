import tkinter as tk
from todo import *
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
                 width=int(WIDTH/6) - 4*PADX,
                 height=int(HEIGHT/10),
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
        task_frame = tk.Frame(master=self.root_window, name='taskdetails', width=int(self.width/6),
                              height=self.height - 2*PADY, bg='dark grey')
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


class ToDoGui:
    def __init__(self,
                 todo_autosave=AUTOSAVE,
                 width=WIDTH,
                 height=HEIGHT):
        self.root = None
        self.height = height
        self.width = width
        self.todo = ToDo(autosave=todo_autosave)
        self.setup_root()

    def setup_root(self):
        self.root = tk.Tk()
        self.root.maxsize(self.width, self.height)
        self.root.minsize(self.width, self.height)
        self.root.title()

    def place_settings_menu(self):
        settings_frame = tk.Frame(self.root, width=int(self.width/6), height=self.height - 2*PADY, bg='dark grey')
        settings_frame.place(x=600, y=100)

        def close_settings():
            settings_frame.destroy()

        close_button = tk.Button(settings_frame, text='Close Settings',
                                 command=close_settings, fg='black', bg="light grey")

        def enter(event):
            close_button.config(bg='#990000')

        def leave(event):
            close_button.config(bg='light grey')
        close_button.bind("<Enter>", enter)
        close_button.bind("<Leave>", leave)
        close_button.grid(row=0, column=1, padx=100, pady=300, sticky='ne')

    def place_create_task(self):
        create_frame = tk.Frame(self.root, width=int(self.width / 6), height=self.height - 2 * PADY, bg='dark grey')
        create_frame.place(x=600, y=100)

        tk.Label(create_frame, text='Add a name for the task:').grid(row=0, column=0, padx=PADX, pady=PADY)
        name_entry = tk.Entry(create_frame, bg='white')
        name_entry.grid(row=0, column=1, padx=PADX, pady=PADY)

        tk.Label(create_frame, text='Add a description for the task').grid(row=1, column=0, padx=PADX, pady=PADY)
        description_entry = tk.Entry(create_frame, bg='white')
        description_entry.grid(row=1, column=1, padx=PADX, pady=PADY)

        options = ['high', 'medium', 'low']
        priority_var = tk.StringVar(create_frame)
        tk.Label(create_frame, text='Select the priority for the task').grid(row=2, column=0, padx=PADX, pady=PADY)
        priority_entry = tk.OptionMenu(create_frame, priority_var, *options)
        priority_entry.grid(row=2, column=1, padx=PADX, pady=PADY)

        def add_task():
            self.todo.add_task({
                'name': name_entry.get(),
                'description': description_entry.get(),
                'creation_time': datetime.datetime.now().strftime("%m/%d/%Y:%H:%M:%S"),
                'priority': priority_var.get()
            })
            create_frame.destroy()
            self.update_tasksbar()
            self.root.children['leftbar'].children['tasksbar'].update_idletasks()
            if self.todo.autosave:
                self.todo.save_tasks()
            print(self.root.children['leftbar'].children['tasksbar'].children)
        add_button = tk.Button(create_frame, text='Add Task', command=add_task, fg='lightblue', bg='black')
        add_button.grid(row=10, column=0, padx=50, pady=100, sticky='ne')

        def close_create():
            create_frame.destroy()
        close_button = tk.Button(create_frame, text='Close Task Adder',
                                 command=close_create, fg='black', bg="light grey")

        def enter(event):
            close_button.config(bg='#990000')

        def leave(event):
            close_button.config(bg='light grey')
        close_button.bind("<Enter>", enter)
        close_button.bind("<Leave>", leave)
        close_button.grid(row=0, column=10, padx=50, pady=10, sticky='ne')

    def setup_elements(self):
        left_bar = tk.Frame(self.root, name='leftbar', width=int(self.width/6),
                            height=self.height - 10*PADY, bg='dark grey')
        left_bar.grid(row=0, column=0, padx=PADX, pady=PADY)

        # Adds the text for the current tasks frame
        tk.Label(left_bar, text='Current Tasks').grid(row=1, column=0, padx=PADX, pady=PADY, sticky="nsew")

        # Creates the task bar that holds the task elements on the left of the window
        tasks_bar = tk.Frame(left_bar, name='tasksbar', width=int(self.width/6) - 2*PADX, height=self.height - 20*PADY)
        tasks_bar.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="nsew")

        # Creates the task elements within the task bar on the left
        x = list(self.todo.tasks.keys())
        for i in range(len(x)):
            TaskButton(master=tasks_bar,
                       text=self.todo.tasks[x[i]]['name'],
                       fg='black',
                       bg='dark grey',
                       task_name=self.todo.tasks[x[i]]['name'],
                       task_description=self.todo.tasks[x[i]]['description'],
                       creation_time=self.todo.tasks[x[i]]['creation_time'],
                       priority=self.todo.tasks[x[i]]['priority'],
                       root_window=self.root).grid(row=i+1, column=0, padx=PADX, pady=PADY, sticky="nsew")

        save_button = tk.Button(self.root, text='Save Tasks',
                                command=self.todo.save_tasks, fg='lightblue', bg='black')
        save_button.grid(row=10, column=0, padx=PADX, pady=PADY, sticky="sw")

        create_button = tk.Button(self.root, text='Create New',
                                  command=self.place_create_task, fg='lightblue', bg='black')
        create_button.grid(row=10, column=1, padx=PADX, pady=PADY, sticky="se")

        settings_button = tk.Button(self.root, text='Settings',
                                    command=self.place_settings_menu, fg='lightblue', bg='black')
        settings_button.grid(row=0, column=10, padx=PADX, pady=PADY, sticky='ne')

    def update_tasksbar(self):
        """
        Runs on clicking the Add task button
        """
        x = self.todo.tasks[list(self.todo.tasks.keys())[-1]]
        new_button = TaskButton(master=self.root.children['leftbar'].children['tasksbar'],
                                text=x['name'],
                                fg='black',
                                bg='dark grey',
                                task_name=x['name'],
                                task_description=x['description'],
                                creation_time=x['creation_time'],
                                priority=x['priority'],
                                root_window=self.root)
        new_button.grid(row=len(self.root.children['leftbar'].children['tasksbar'].children),
                        column=0, padx=PADX, pady=PADY)

    def draw_app(self):
        self.setup_elements()
        print(self.root.children['leftbar'].children['tasksbar'].children)
        self.root.mainloop()


if __name__ == '__main__':
    app = ToDoGui()
    app.draw_app()
