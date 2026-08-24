from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware

from database.models import Base, Users
from database.config import engine, get_db
from database.schemes import UserData, UsersUpdateData

from routes.drugs import drug_route
from routes.sale import check_route

# CORS -> Cross -origin  recourse sharing

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(drug_route)
app.include_router(check_route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

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


@app.get("/users/")
def users_get(admin_id: int,start:int = 0, skip:int = 10, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role.value == "admin":
        users = db.query(Users).all()[start:skip]
        return {"message":"Fetched successfully !", "success":True, "data":users}
    else:
        return {"message":"Bir aylanib keling", "success":False}


@app.delete("/users-delete/{account_id}")
def user_delete(account_id: int, admin_id: int, db = Depends(get_db)):
    admin_users = db.query(Users).filter(Users.id == admin_id).first()
    if admin_users.role.value == "admin":
        delete_account = db.query(Users).filter(Users.id == account_id).first()
        db.delete(delete_account)
        db.commit()
        return {"message":"Deleted !", "success":True}
    else:
        return {"message":"Bir aylanib keling", "success":False}


@app.put("/account-update/")
def account_update(admin_id:int,user_data:UsersUpdateData, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role.value == "admin":
        user = db.query(Users).filter(Users.id == user_data.id).first()

        new_user_data = user_data.model_dump(exclude_unset=True)

        for key, value in new_user_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return {"message":"Updated !", "success":True, "data":user}
    else:
        return {"message":"Bir aylanib keling", "success":False}



