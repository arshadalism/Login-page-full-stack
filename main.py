import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from db_client import database
from fastapi.middleware.cors import CORSMiddleware

login_page_col = database.get_collection("login_page_data")

app = FastAPI(title="Login page")

origins = [
    "http://127.0.0.1:63342",
    "http://localhost:63342"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(user: User):
    data = {
        "user": user.username,
        "password": user.password
    }
    await login_page_col.insert_one(data)
    return {"message": "login successfully"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)