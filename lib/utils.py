from .models import User, Project, Task

users = {}
all_projects = User.projects
all_tasks = Project.tasks

def add_user(args):
    username = args.name
    useremail = args.email
    if username in users:
        print(f"User '{username}' already exists.")
        return
    new_user = User(username, useremail)
    users = new_user
    print(f"User '{username}' added successfully with email '{useremail}'.")

def add_project(args):
    user = users.get(args.user) or User(args.user)
    users[args.user] = user
    title = args.title
    description = args.description
    due_date = args.due_date
    project = Project(title, description, due_date)
    user.add_project(project)

def add_task(args):
    project = project.get(args.project) or Project(args.project)
    title = args.title
    status = args.status
    assigned_to = args.assigned_to
    task = Task(title, status, assigned_to)
    project.add_task(task)

def list_projects(args):
    user = users.get(args.user)
    print(f"These are all of {user}'s projects: ")
    for project in user:
        if user.name == args.user:
            print(f"{project}")

def list_tasks(args):
    project = project.get(args.project)
    print(f"These are all of {project}'s tasks: ")
    for task in project:
        if project.title == args.project:
            print(f"{task}")

def complete_project(args):
    user = users.get(args.user)
    if user:
        for project in user.projects:
            if project.title == args.title:
                project.complete_project()
                return
        print("❌ Project not found.")
    else:
        print("❌ User not found.")

def complete_task(args):
    project = project.get(args.project)
    if project:
        for task in project.tasks:
            if task.title == args.title:
                task.complete_task()
                return
        print("❌ Task not found.")
    else:
        print("❌ Project not found.")