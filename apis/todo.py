from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Adjust these imports based on your actual file organization
from database import SessionLocal
from crud import get_todo, create_todo, update_todo, get_todos, delete_todo
from schemas import TodoCreate, TodoUpdate, TodoInDB

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
