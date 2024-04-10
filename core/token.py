from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException
from core.security import verify_token
from db.session import get_session
from appv1.crud.users import  get_user_by_id
from fastapi.security import OAuth2PasswordBearer




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_session)
):
    
    user_id = await verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, 
        detail="Invalid token")
    user_db = get_user_by_id(user_id, db)
    if user_db is None:
        raise HTTPException(status_code=404, 
        detail="User not found")
    return user_db
