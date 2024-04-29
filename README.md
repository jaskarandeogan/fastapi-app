# fastapi-app

FastAPI Todo App
This is a simple Todo application built with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

Features
Create Todo: Add new tasks to your list with title and description.
Read Todo: View individual tasks by their ID or get a list of all tasks.
Update Todo: Update existing tasks to mark them as completed or modify their details.
Delete Todo: Remove tasks from your list when they are no longer needed.

Installation
Clone this repository to your local machine:
    git clone <repository_url>

Navigate to the project directory:
    cd fastapi-todo-app

Install the required dependencies using pip:
    pip install -r requirements.txt

Usage
    Start the FastAPI server:
        uvicorn main:app --reload

Open your web browser and navigate to http://localhost:8000/docs to access the interactive API documentation (Swagger UI) for testing the endpoints.