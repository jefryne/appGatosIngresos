import sys

from appv1.models import User
from fastapi import HTTPException
from appv1.schemas.users import UserCreate, UserRead
from sqlalchemy.orm import Session
from core.security import get_hashed_password
from core.utils import generate_user_id


def create_new_user(user:UserCreate, db: Session):
    db_user = User(
        user_id = generate_user_id(),
        full_name = user.full_name,
        mail = user.mail,
        passhash = get_hashed_password(user.passhash),
        user_role = user.user_role,
        user_status = user.user_status
    )
    
    try: 
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        #imprimir el error en la consola 
        print(f"Error al crear usuario: {str(e)}",  file=sys.stderr)
        #Devolver una respuesta de error detallada
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")
    
def get_user_by_email(mail: str, db: Session):
    user = db.query(User).filter(User.mail == mail).first()
    return user

def get_user_by_id(id: str, db: Session):
    user = db.query(User).filter(User.user_id == id).first()
    return user