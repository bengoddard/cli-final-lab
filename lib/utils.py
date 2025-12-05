from .models import User, Project, Task, DATA_FILE
import json
import os
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

console = Console()

def save_state():
    """Saves current state of User.all to JSON file."""
    try:
        data_to_save = {name: user.to_dict() for name, user in User.all.items()}
        with open(DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        console.print(f"❌ [bold red]Error saving state:[/bold red] {e}")

def load_state():
    """Loads state from JSON file and recreates objects."""
    if not os.path.exists(DATA_FILE):
        console.print("💾 [dim]New session. Data file not found.[/dim]")
        return

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        for name, user_data in data.items():
            user = User.find_or_create(user_data['name'], user_data['email'])
            for project_data in user_data['projects']:
                project = Project(
                    project_data['title'],
                    project_data['description'],
                    project_data['due_date']
                )
                project._completed = project_data['completed']
                user.add_project(project)
                for task_data in project_data['tasks']:
                    task = Task(
                        task_data['title'],
                        task_data['status'],
                        task_data['assigned_to']
                    )
                    task.completed = task_data['completed']
                    project.add_task(task)
        console.print(f"💾 [green]State loaded from {DATA_FILE}[/green]")

    except json.JSONDecodeError:
        console.print("❌ [bold red]Error:[/bold red] Data file is malformed (invalid JSON). Starting fresh.")
    except Exception as e:
        console.print(f"❌ [bold red]An error occurred while loading data:[/bold red] {e}. Starting fresh.")

def add_user(args):
    try:
        User.find_or_create(args.name, args.email)
        console.print(f"👤 [green]User '{args.name}' added successfully[/green] with email '{args.email}'.")
        save_state()
    except ValueError as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")

def add_project(args):
    user = User.all.get(args.user)
    if user:
        title = args.title
        description = args.description
        due_date = args.due_date
        new_project = Project(title, description, due_date)
        user.add_project(new_project)
        console.print(f"📌 [green]Project '{args.title}' added to {args.user}.[/green]")
        save_state()
    else:
        console.print(f"❌ [bold red]User '{args.user}' not found.[/bold red]")

def add_task(args):
    user = User.all.get(args.user)
    if user:
        project_instance = next((p for p in user.projects if p.title == args.project), None)
        if project_instance:
            title = args.title
            status = args.status
            assigned_to = args.assigned_to
            task = Task(title, status, assigned_to)
            project_instance.add_task(task)
            console.print(f"📋 [green]Task '{args.title}' added to Project '{args.project}'.[/green]")
            save_state()
        else:
            console.print(f"❌ [bold red]Project '{args.project}' not found for user '{args.user}'.[/bold red]")
    else:
        console.print(f"❌ [bold red]User '{args.user}' not found.[/bold red]")

def list_projects(args):
    user = User.all.get(args.user)
    if user:
        table = Table(title=f"{user.name}'s Projects", style="bold magenta")
        table.add_column("ID", style="dim", justify="center")
        table.add_column("Title", style="cyan")
        table.add_column("Due Date")
        table.add_column("Status", style="bold")
        table.add_column("Tasks", justify="center")

        for project in user.projects:
            status = "[green]COMPLETE[/green] ✅" if project.completed else "[yellow]ACTIVE[/yellow] ⏳"
            table.add_row(
                str(project.id),
                project.title,
                project.due_date,
                status,
                str(len(project.tasks))
            )
        console.print(table)
    else:
        console.print(f"❌ [bold red]User '{args.user}' not found.[/bold red]")

def list_tasks(args):
    user = User.all.get(args.user)

    if user:
        project_instance = next((p for p in user.projects if p.title == args.project), None)
        if project_instance:
            table = Table(title=f"Tasks in '{project_instance.title}'", style="bold blue")
            table.add_column("Status", style="bold", justify="center")
            table.add_column("Title", style="white")
            table.add_column("Assigned To", style="magenta")

            for task in project_instance.tasks:
                status = "✅" if task.completed else "☐"
                table.add_row(
                    status,
                    task.title,
                    task.assigned_to
                )
            console.print(table)
        else:
            console.print(f"❌ [bold red]Project '{args.project}' not found for user '{args.user}'.[/bold red]")
    else:
        console.print(f"❌ [bold red]User '{args.user}' not found.[/bold red]")

def complete_project(args):
    user = User.all.get(args.user)
    if user:
        for project in user.projects:
            if project.title == args.title:
                project.complete_project()
                console.print(f"✅ [green]Project '{project.title}' completed for {args.user}.[/green]")
                save_state()
                return
        console.print("❌ [bold red]Project not found.[/bold red]")
    else:
        console.print("❌ [bold red]User not found.[/bold red]")

def complete_task(args):
    user = User.all.get(args.user)
    if user:
        project_instance = next((p for p in user.projects if p.title == args.project), None)
        if project_instance:
            for task in project_instance.tasks:
                if task.title == args.title:
                    task.complete_task()
                    console.print(f"✅ [green]Task '{task.title}' completed in '{args.project}'.[/green]")
                    save_state()
                    return
                console.print("❌ [bold red]Task not found.[/bold red]")
        else:
            console.print("❌ [bold red]Project not found.[/bold red]")
    else:
        console.print("❌ [bold red]User not found.[/bold red]")