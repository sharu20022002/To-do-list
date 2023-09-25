
from datetime import datetime, timedelta


class Task:
    def __init__(self, description, due_date=None):
        # attributes of Task
        self.description = description
        self.completed = False
        self.due_date = due_date

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f"Due: {self.due_date}" if self.due_date else "No due date"
        return f"{self.description} ({status}, {due_date_str})"

# TaskBuilder class is useful in creation of valid tasks


class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, date_string):
        # Try catch block to handle error where user entered date in past.
        try:
            # Attempt to parse the input as a valid date
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            # Check if the parsed date is valid (e.g., not in the past)
            current_date = datetime.today() - timedelta(days=1)

            if date_obj >= current_date:
                self.task.due_date = date_string
                return True
            else:
                print("The date should be today or later. Date Not Added")
                return False

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return False

    # returns the valid task to caller
    def build(self):
        return self.task


# ------------------------------------ToDoListManager Class handles operations of application------------------------------------------------ #

# this class contains all the appropriate actions of Todo list application
class ToDoListManager:
    def __init__(self):

        self.tasks = []  # emtpy tasks list to store tasks
        # emtpy memento_stack to store list of actions performed, helpful to perform undo
        self.memento_stack = []
        # emtpy redo_stack used to store undo actions performed, htlpful to perform redo a
        self.redo_stack = []

    # function to save the task action into memento_stack
    def save_memento(self, action, task):
        task_copy = Task(task.description, task.due_date)
        task_copy.completed = task.completed
        self.memento_stack.append((action, task_copy))

    # function to add new task into Todo list
    def add_task(self, task):
        self.tasks.append(task)
        self.save_memento("add", task)

    # Marks the item as completed by taking index of the list as input
    def mark_completed(self, index):
        # try catch block to handle out of bound entry by user
        try:
            task = self.tasks[index]
            task.mark_completed()
            self.save_memento("mark_completed", task)
            return task.description

        except IndexError:
            print("Task index out of bounds")
            return False

    # Deletes task from the list by taking index as input from the user
    def delete_task(self, index):
        # try catch block to handle out of bound entry by user
        try:
            if len(self.tasks) == 0:
                print("TO-DO list is empty. Please first add items to delete!")
                return False
            else:
                # pop remove the element from the list and that value is stored in task
                task = self.tasks.pop(index)
                self.save_memento("delete", task)
                return task.description

        except IndexError:
            print("Task index out of bounds")
            return False

    # function to perfrom undo operation
    def undo(self):
        if self.memento_stack:
            action, task = self.memento_stack.pop()  # get hold of recent action performed
            index = 0
            if action == "add":  # performes opposite of recent action
                value = self.tasks.pop(-1)
                print(f"{value.description} removed")  # add ---> remove

            elif action == "mark_completed":
                for i in range(0, len(self.tasks)):
                    if self.tasks[i].description == task:
                        index = i
                self.tasks[index].completed = False
                print(
                    f" '{self.tasks[index].description}' is marked as pending")  # completed --->  pending

            elif action == "delete":
                self.tasks.append(task)
                # delete ---> add
                print(f"'{task.description}' is added back to list")
            self.redo_stack.append((action, task))
            return True
        else:
            print("Nothing to undo.")
            return False

    def redo(self):
        if self.redo_stack:
            action, task = self.redo_stack.pop()  # get hold of recent undo action
            if action == "add":  # Performs opposite action
                self.tasks.append(task)
                # add ---> remove
                print(f"'{task.description}' is added back to list")
            elif action == "mark_completed":
                task.mark_completed()
                # completed ---> pending
                print(f"'{task.description}' marked as complete")

            elif action == "delete":
                self.tasks.remove(task)
                # deleted ---> add
                print(f"'{task.description}' is removed from the list")
            self.memento_stack.append((action, task))
            return True
        else:
            print("Nothing to Redo !")
            return False

    # function to view the elements in the Todo list
    def view_tasks(self, status=None):
        if len(self.tasks) == 0:  # If no items yet, display appropriate message
            print("No tasks in list")
            return None
        if status == "completed":
            return [task for task in self.tasks if task.completed]
        elif status == "pending":
            return [task for task in self.tasks if not task.completed]
        else:
            return self.tasks


# ------------------------------------------------Main Method------------------------------------------------ #
# main method to run the program and accept choices from user
def main():
    todo_manager = ToDoListManager()
    while True:  # loop till user wishes to quit (7)
        print("\nTo-Do List Manager Menu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")  # options display to user
        print("4. View Tasks")
        print("5. Undo")
        print("6. Redo")
        print("7. Quit")

        choice = input("Enter your choice: ")  # accepting user choice

        # appropriate if condition get activiated as per user choice and action is performed (like a switch block)
        # Also note error is also handled where and when needed using try catch block

        if choice == "1":  # Adds new task (inputs duedate(optional) also)
            description = input("Enter task description: ")
            due_date = input("Enter due date (optional, format: YYYY-MM-DD): ")
            task_builder = TaskBuilder(description)
            if due_date:
                value = task_builder.set_due_date(due_date)
                if value:
                    task = task_builder.build()
                    todo_manager.add_task(task)
                    print(f"Task '{description}' added.")
            else:
                task = task_builder.build()
                todo_manager.add_task(task)
                print(f"Task '{description}' added.")

        elif choice == "2":  # marks the task as completed as per index number entered by user
            try:
                index = int(
                    input("Enter the index (starting from 0) of the task to mark as completed: "))
                description = todo_manager.mark_completed(index)
                if description:
                    print(f"Task '{description}' marked as completed.")

            except ValueError:
                print("Invalid input. Please enter a valid integer index.")

        elif choice == "3":             # deletes the task at index entered by user
            try:
                index = int(input("Enter the index of the task to delete: "))
                description = todo_manager.delete_task(index)
                if description:
                    print(f"Task '{description}' deleted successfully")

            except ValueError:
                print("Invalid input. Please enter a valid integer index.")

        elif choice == "4":  # displays the task as per filter of all/completed/pending
            status = input("Enter status (all/completed/pending): ")
            tasks = todo_manager.view_tasks(status)
            if tasks:
                print("\nTasks:")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

        elif choice == "5":  # performs undo operation and displays appropriate message
            status = todo_manager.undo()
            if status:
                print("Undo action performed.")

        elif choice == "6":  # performs redo operation and displays appropriate message
            status = todo_manager.redo()
            if status:
                print("Redo action performed.")

        elif choice == "7":  # breaks the while loop and exits the program
            print("Goodbye!")
            break
        else:  # default case: incase user inputs a wrong choice
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":  # calling main method.
    main()


