import argparse
from lib.utils import add_user, add_project, add_task, list_projects, list_tasks, complete_project, complete_task, load_state

def main():
    load_state()
    parser = argparse.ArgumentParser(description="Project Manager CLI")
    subparsers = parser.add_subparsers()

    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("name")
    add_user_parser.add_argument("email")
    add_user_parser.set_defaults(func=add_user)

    add_project_parser = subparsers.add_parser("add-project", help="Add a new project to a user")
    add_project_parser.add_argument("user")
    add_project_parser.add_argument("title")
    add_project_parser.add_argument("description")
    add_project_parser.add_argument("due_date")
    add_project_parser.set_defaults(func=add_project)

    add_task_parser = subparsers.add_parser("add-task", help="Add a new task to a project")
    add_task_parser.add_argument("user")
    add_task_parser.add_argument("project")
    add_task_parser.add_argument("title")
    add_task_parser.add_argument("status")
    add_task_parser.add_argument("assigned_to")
    add_task_parser.set_defaults(func=add_task)

    list_project_parser = subparsers.add_parser("list-projects", help="List all projects of a user")
    list_project_parser.add_argument("user")
    list_project_parser.set_defaults(func=list_projects)

    list_task_parser = subparsers.add_parser("list-tasks", help="List all tasks in a project")
    list_task_parser.add_argument("user")
    list_task_parser.add_argument("project")
    list_task_parser.set_defaults(func=list_tasks)

    complete_project_parser = subparsers.add_parser("complete-project", help="Complete a project")
    complete_project_parser.add_argument("user")
    complete_project_parser.add_argument("title")
    complete_project_parser.set_defaults(func=complete_project)

    complete_task_parser = subparsers.add_parser("complete-task", help="Complete a task")
    complete_task_parser.add_argument("user")
    complete_task_parser.add_argument("project")
    complete_task_parser.add_argument("title")
    complete_task_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()