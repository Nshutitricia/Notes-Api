from fastapi import FastAPI
from router import notes
app = FastAPI(title="Notes API")
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Notes API"}

