import sys

from appv1.models.User import User
from fastapi import HTTPException
from appv1.schemas.users import DeleteUser, UserCreate, UpdateUser
from sqlalchemy.orm import Session
from core.security import get_hashed_password, verify_password
from core.utils import generate_user_id


def create_new_user(user:UserCreate,rol: str, db: Session):
    db_user = User(
        user_id = generate_user_id(),
        full_name = user.full_name,
        mail = user.mail,
        passhash = get_hashed_password(user.passhash),
        user_role = rol,
        user_status = user.user_status
    )
    
    try: 
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {str(e)}",  file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

def update_user(user: UpdateUser, db: Session):
    db_user = get_user_by_id(user.user_id, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")

    db_user.full_name = user.full_name
    db_user.mail = user.mail
    db_user.passhash = get_hashed_password(user.passhash)
    db_user.user_role = user.user_role if db_user.user_role == 'admin' else db_user.user_role

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al  actualizar usuario: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")
    


def delete_user(user: DeleteUser, db: Session):
    db_user = get_user_by_id(user.user_id, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")

    db_user.user_status = user.user_status

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")


def get_user_by_email(mail: str, db: Session):
    user = db.query(User).filter(User.mail == mail).first()
    return user

def get_user_by_id(id: str, db: Session):
    user = db.query(User).filter(User.user_id == id).first()
    return user

def get_all_user(db: Session):
    users = db.query(User).all()
    return users

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_email(username, db)
    if not user:
        return False
    if not verify_password(password, user.passhash):
        return False
    if not user.user_status:
        return False
    return user