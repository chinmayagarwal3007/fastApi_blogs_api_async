from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_blog():
    return {"message": "Welcome to the blog!"} 