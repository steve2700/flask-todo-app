# Project Title

Flask Todo App

## Description

The Flask Todo App is a web application that allows users to manage their tasks and keep track of their to-do lists. It provides a user-friendly interface for adding, updating, and deleting tasks, as well as categorizing tasks and adding notes.
## Motivation
My name is Stewart Nyaruwata student at alx africa software engineering it might look easy but lot of work was done 
The motivation behind creating the Flask Todo App was to develop a simple yet powerful task management tool that would help individuals and teams stay organized and productive. We recognized the need for a lightweight and customizable solution that can be easily deployed and used by anyone.

With the Flask Todo App, we aimed to provide a streamlined user experience that focuses on essential task management features while keeping the interface clean and intuitive. We wanted to create a tool that helps users prioritize their tasks, categorize them based on different contexts, and easily update or delete tasks as needed.

By developing this app, we wanted to empower users to take control of their daily tasks, boost their productivity, and achieve their goals more effectively. We believe that an organized and structured approach to task management can significantly improve efficiency and reduce stress in both personal and professional settings.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Documentation](#documentation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Future Development](#future-development)

## Installation

1. Clone the repository:
git clone https://github.com/steve2700/flask-todo-app/

2. Navigate to the project directory:
 
3. Install the dependencies:
   # pip install -r requirements.txt

5. Open your web browser and visit `http://localhost:5000` to access the Flask Todo App.

## Usage

1. Add a new task:
- Enter the task content in the input field.
- Select the category from the dropdown menu.
- Optionally, add notes in the notes section.
- Click the "Add task" button to add the task to the list.

2. Update a task:
- Click the "Update" button next to the task you want to update.
- Modify the task content in the input field.
- Click the "Update task" button to save the changes.

3. Delete a task:
- Click the "Delete" button next to the task you want to delete.
- Confirm the deletion when prompted.

4. View tasks:
- The tasks are displayed in a table.
- Each task shows the task content, date created, category, and notes (if any).

## Features

- Add, update, and delete tasks.
- Categorize tasks for better organization.
- Add optional notes to tasks.
- User-friendly interface.
- Responsive design for mobile and desktop.

## Screenshots



Here is a screenshot of the Flask Todo App:

![Flask Todo App](https://github.com/steve2700/flask-todo-app/blob/main/screenshots/Screenshot%20(4).png)

The User Enters ThE TASK 
![Flask Todo App](https://github.com/steve2700/flask-todo-app/blob/main/screenshots/Screenshot%20(5).png)



## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit for Python
## Algorithm BEHIND THIS 
The algorithm used in TaskBuddy revolves around the basic CRUD operations (Create, Read, Update, Delete) for managing tasks. Here's a breakdown of the algorithm:

-Create Task:

When a user submits a task through the interface, the algorithm creates a new task object.
The task object is populated with the provided task content, category, and optional notes.
The task object is then added to the database, storing the task details.
-Read Tasks:

The algorithm retrieves all tasks from the database.
The tasks are sorted based on the publication date, ensuring the latest tasks appear first.
The algorithm then presents the tasks to the user, displaying the task content, publication date, category, and notes (if any).
-Update Task:

When a user requests to update a specific task, the algorithm retrieves the task from the database based on its unique identifier.
The task object is then updated with the new task content provided by the user.
The updated task object is saved back to the database, reflecting the changes made by the user.
-Delete Task:

If a user chooses to delete a task, the algorithm identifies the task to be deleted based on its unique identifier.
The task object is removed from the database, permanently deleting the task from the system.
Overall, the algorithm ensures smooth interaction between the user interface and the database, allowing users to perform essential task management operations effectively. It leverages the capabilities of Flask, SQLAlchemy, and the underlying database to provide a seamless user experience in managing tasks within the TaskBuddy application.

## Future Development

In the future, we plan to implement the following features:
- Task prioritization and sorting
- User authentication and accounts
- Task sharing and collaboration
- Reminders and notifications
If you have any good ideas for features, please contact Stewart through LinkedIn. For deployment ideas and adding new designs at twitter and Linkedin 


We are open to suggestions and contributions for further enhancements!






