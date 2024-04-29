#this file is the implementation of the CRUD operations for the Todo model. 
# It contains the functions to get, create, update, and delete todos. 
# The functions in this file are used by the API endpoints in apis/todo.py to interact with the database and perform CRUD operations on the todos.

from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging as logger

def get_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos  # Simply return the list, even if it's empty

def create_todo(db: Session, todo: TodoCreate):
    try:
        db_todo = Todo(title=todo.title, description=todo.description, completed=False)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        logger.error(f"Error creating todo: {e}")
        db.rollback()  # Rollback transaction in case of error
        raise HTTPException(status_code=400, detail=str(e))

def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo to update not found")
    try:
        update_data = todo.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        logger.error(f"Error updating todo: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo to delete not found")
    try:
        db.delete(db_todo)
        db.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting todo: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

0