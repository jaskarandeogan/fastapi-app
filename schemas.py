from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: bool

class TodoInDB(TodoBase):
    id: int
    completed: bool = False

    class Config:
        orm_mode = True

