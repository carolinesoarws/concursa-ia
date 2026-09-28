"""Application entry point."""

from fastapi import FastAPI

app = FastAPI(title="Concursa IA", version="1.0.0")

@app.get("/hello_world")
def hello_world():
    return {"message": "Hello, Concurseiro!"}

@app.get("/health")
def health_check():
    try:
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


    
