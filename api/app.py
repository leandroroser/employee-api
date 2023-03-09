from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import employee
from fastapi import FastAPI
import os


description = """
"""

tags_metadata = [
    {
        "name": "employee",
        "description": ""
    },
]

    
app = FastAPI(title="employee", openapi_tags = tags_metadata) 
app.include_router(employee.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
    
@app.get("/status", tags=["status"])
def status() -> JSONResponse:
    return {"status": "I am up"}
