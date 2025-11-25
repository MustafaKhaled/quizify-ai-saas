from fastapi import FastAPI

# The FastAPI application instance
app = FastAPI()

# A GET endpoint for health check
@app.get("/")
def read_root():
    return {"message": "AI Quiz Backend Running", "status": "OK"}