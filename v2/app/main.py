from fastapi import FastAPI

app = FastAPI(title="Movypark API v2")

@app.get("/")
async def root():
    return {"message": "Welcome to Movypark API v2"}