from fastapi import APIRouter, Depends
from database.config import get_db
from database.models import Drug, Users
from database.schemes import DrugData

drug_route = APIRouter(tags=["Drug routelari"])


@drug_route.post("/drug-create/")
def drug_create(drug_data: DrugData, admin_id: int ,db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user.role.value == "admin":
        new_drug = Drug(**drug_data.model_dump())
        db.add(new_drug)
        db.commit()

        new_drug.bar_code = f"{new_drug.id}-{new_drug.name}"
        db.commit()
        db.refresh(new_drug)

        return {"message":"Created !", "success":True, "data":new_drug}
    else:
        return {"message":"Bir o'ynab keling !", "success":False}