import json
import os
import datetime


class ToDo():
    """
    Main ToDo app class
    The makeup of the tasks.json shall be:
    {
        task_id:{
            task_name: string,
            task_description: string,
            time_of_creation: string from datetime in style: "%m/%d/%Y:%H:%M:%S",
            priority: string [low, medium, high]
        },
        ...
    }
    Args:
    """
    def __init__(self,
                 autosave = True):
        self.autosave = autosave
        self.tasks = None
        self.set_tasks()
        self.priority = {}
        self.set_priorities()

    def toggle_autosave(self):
        """
        A function to toggle weather the app autosaves the tasks json
        """
        if self.autosave:
            self.autosave = False
        else:
            self.autosave = True

    def set_tasks(self) -> None:
        if 'tasks.json' in os.listdir():
            with open('tasks.json') as f:
                self.tasks = json.load(f)
                f.close()
        else:
            self.tasks = {}
            self.save_tasks()

    def save_tasks(self) -> None:
        """
        Saves the self.tasks dictionary to a json named tasks.json
        """
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f, indent=4)
            f.close()
        print('Saving tasks to tasks.json')

    def set_priorities(self):
        """
        Adds tasks based on their priority into the correct task priority list
        """
        self.priority = {
            'high': [],
            'medium': [],
            'low': []
        }
        for key in self.tasks:
            x = self.tasks[key]['priority']
            if x == 'high':
                self.priority['high'].append(key)
            elif x == 'medium':
                self.priority['medium'].append(key)
            elif x == 'low':
                self.priority['low'].append(key)

    def add_task(self, task_params: dict) -> None:
        """
        Adds a new task to the tasks list
        Args:
            = task_params (dict):  a dict with the values given in the class string
        """
        x = list(self.tasks.keys())
        print(x)
        if x:
            self.tasks[str(max([int(i) for i in x])+1)] = task_params
        else:
            self.tasks['0'] = task_params
        if self.autosave:
            self.save_tasks()

    def delete_task(self, task_id: int) -> None:
        """
        Deletes a task from the self.tasks dictionary
        Args:
            - task_id (int): The id of the task to remove, within the gui the tasks will have their id assigned
        """
        self.tasks.pop(task_id)


if __name__ == '__main__':
    todoApp = ToDo()

    example_task = {
            'name': 'My Test Task!',
            'description': 'This is an example of adding a task to the json',
            'creation_time': datetime.datetime.now().strftime("%m/%d/%Y:%H:%M:%S"),
            'priority': 'high'  # string [low, medium, high]
        }
    todoApp.add_task(example_task)
    todoApp.set_priorities()
    print(todoApp.tasks)
    print(todoApp.priority)
