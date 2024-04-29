# This file contains the API endpoints for the Todo model.
# It defines the routes for creating, reading, updating, and deleting todos.

from fastapi import APIRouter, Depends, HTTPException
# Importing the Session class from the sqlalchemy.orm module
from sqlalchemy.orm import Session
# Importing the List module from the typing library
from typing import List

# Importing the database session
from database import SessionLocal
# Importing the functions from the crud.py file
from controllers.crud import get_todo, create_todo, update_todo, get_todos, delete_todo
# Importing the Pydantic models from the schemas.py file
from models.schemas import TodoCreate, TodoUpdate, TodoInDB

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TodoInDB)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo(db=db, todo=todo)

@router.get("/{todo_id}", response_model=TodoInDB)
def read_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.get("/", response_model=List[TodoInDB])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_todos(db, skip=skip, limit=limit)

@router.put("/{todo_id}", response_model=TodoInDB)
def update_todo_endpoint(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    updated_todo = update_todo(db, todo_id, todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    if not delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}
