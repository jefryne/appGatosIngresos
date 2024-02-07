from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_session
from appv1.crud.users import create_new_user, get_user_by_email, get_user_by_id
from appv1.schemas.users import UserCreate, UserRead

router = APIRouter()

@router.post("/create/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    verify_user = get_user_by_email(user.mail, db)
    if verify_user is None:
        return create_new_user(user, db)
    
    raise HTTPException(status_code=404, detail="email already exists")


@router.get("/get/{user_id}", response_model=UserRead)
async def read_user(user_id: str, db: Session = Depends(get_session)):
    user = get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user