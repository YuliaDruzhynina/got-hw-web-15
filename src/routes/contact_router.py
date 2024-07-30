
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import User
from src.schemas import ContactResponse, ContactSchema
from src.services.auth import auth_service
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/")
def main_root():
    return {"message": "Hello, fastapi application!"}

@router.post("/contacts/", response_model=ContactResponse)
async def create_contact(body: ContactSchema, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)

@router.get("/contacts", response_model=list[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    return await repository_contacts.get_contacts(db)

@router.get("/contacts/id/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return await repository_contacts.get_contact_by_id(contact_id, db)

@router.get("/contacts/by_name/{contact_fullname}", response_model=ContactResponse)
async def get_contact_by_fullname(contact_fullname: str = Path(...), db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.get_contact_by_fullname(contact_fullname, db, user)

@router.get("/contacts/by_email/{contact_email}", response_model=ContactResponse)
async def get_contact_by_email(contact_email: str = Path(...), db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.get_contact_by_email(contact_email, db, user)

@router.get("/contacts/by_birthday/{get_birthday}", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return await repository_contacts.get_upcoming_birthdays(db)

@router.get("/contacts/get_new_day/{new_date}", response_model=list[ContactResponse])
async def get_upcoming_birthdays_from_new_date(new_date: str = Path(..., description="Current date in format YYYY-MM-DD"),db: Session = Depends(get_db)):
    return await repository_contacts.get_upcoming_birthdays_from_new_date(new_date, db)

@router.put("/contacts/update/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1),db: Session = Depends(get_db)):
    return await repository_contacts.update_contact(contact_id, body, db) 

@router.delete("/contacts/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    return await repository_contacts.delete_contact(contact_id, db)  