


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)
        print(f"Project '{project.title}' added to {self.name}.")


class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []
        self.completed = False

    def add_tasks(self, task):
        self.tasks.append(task)
        print(f"Task '{task.title}' added to {self.title}.")

    def complete_project(self):
        self.completed = True
        print(f"Project '{self.title}' completed.")


class Task:
    def __init__(self, title, status, assigned_to):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.completed = False

    def complete_task(self):
        self.completed = True
        print(f"Task '{self.title}' completed.")