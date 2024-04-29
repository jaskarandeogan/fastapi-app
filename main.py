import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine, SessionLocal
# Apply the DebugMiddleware to enable debug mode
from fastapi.middleware.cors import CORSMiddleware
from apis import todo

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo API", version="1.0")
app.include_router(todo.router)

# Log incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

# Create tables on startup
app.add_event_handler("startup", create_tables)

# Exception handlers
# Add an exception handler for SQLAlchemy errors
# This will catch any SQLAlchemy errors that occur during request processing
# and return a 500 error response with a generic message to the client.
@app.exception_handler(SQLAlchemyError)
def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"SQLAlchemy error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred while processing your request with the database."}
    )
    
# Add a general exception handler
# This will catch any unhandled exceptions and return a 500 error response
# with a generic message to the client.
@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."}
    )
    
# Health check endpoint to verify the API is running
@app.get("/")
def api_health():
    return {
        "status": 200,
        "message": "API is Healthy"
    }
    
# Run the application with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)  # Enable debug mode here
