from fastapi import FastAPI , Depends

from database.models import Base, Users
from database.config import engine, get_db
from database.schemes import UserData
Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def welcome():
    return {"message":"Welcome to Apteka !"}


@app.post("/register/")
def register_user(user_data: UserData, db = Depends(get_db)):
    try:
        new_user = Users(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        return {"message":"Failed!", "error":str(error), "success":False}