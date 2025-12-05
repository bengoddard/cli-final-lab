import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
"""Class User is used to create users and to add projects to users"""
class User:
    all = {}
    _next_id = 1
    def __init__(self, name, email, user_id=None):
        self.id = user_id if user_id is not None else User._next_id
        if user_id is None:
            User._next_id += 1

        self._name = name
        self.email = email
        self.projects = []
        User.all[self.id] = self

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name or len(new_name) < 3:
            raise ValueError("Name must be at least 3 characters.")
        self._name = new_name

    def __str__(self):
        return f"User {self.id}: {self.name} ({self.email})"

    @classmethod
    def find_or_create(cls, name, email=None):
        """Finds user by name or creates a new one if not found."""
        if name not in cls.all:
            if email is None:
                raise ValueError(f"User '{name}' not found. Email is required for creation.")
            cls.all[name] = cls(name, email)
        return cls.all[name]

    def add_project(self, project):
        self.projects.append(project)
        print(f"Project '{project.title}' added to {self.name}.")

    def list_projects(self):
        print(f"Projects for {self.name}:")
        if not self.projects:
            print(" No projects found.")
            return
        for project in self.projects:
            status = " (Complete)" if project.completed else " (Active)"
            print(f"- {project.title}{status} | Due: {project.due_date}")

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'projects': [p.to_dict() for p in self.projects]
        }

"""Class Project is used to create projects, to add tasks to projects, and to mark projects as complete"""
class Project:
    _next_id = 1
    def __init__(self, title, description, due_date):
        self.id = Project._next_id
        Project._next_id += 1
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []
        self.completed = False

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.title}' added to {self.title}.")

    def list_tasks(self):
        print(f"Tasks for project '{self.title}':")
        if not self.tasks:
            print("  No tasks found.")
            return

        for task in self.tasks:
            status = "✅" if task.completed else "☐"
            print(f"{status} {task.title} (Assigned to: {task.assigned_to})")

    def complete_project(self):
        self.completed = True
        print(f"Project '{self.title}' completed.")

    def __str__(self):
        status = "✅" if self.completed else "⏳"
        return f"[{status}] {self.title} (Due: {self.due_date})"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'tasks': [t.to_dict() for t in self.tasks]
        }

"""Class Task is used to create tasks and to mark tasks as complete"""
class Task:
    def __init__(self, title, status, assigned_to):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.completed = False

    def complete_task(self):
        self.completed = True
        print(f"Task '{self.title}' completed.")

    def __str__(self):
        status = "✅" if self.completed else "☐"
        return f"{status} {self.title} (Status: {self.status}, Assigned: {self.assigned_to})"

    def to_dict(self):
        return {
            'title': self.title,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'completed': self.completed
        }