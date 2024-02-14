from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_token
from db.session import get_session
from appv1.schemas.users import UserCreate, UserCreateAdmin, UserRead, Token
from appv1.crud.users import authenticate_user, create_new_user, get_user_by_email, get_user_by_id


router = APIRouter()

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



    
@router.post("/create-user/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):

    verify_user = get_user_by_email(user.mail, db)
    if verify_user is None:
        return create_new_user(user, 'user', db)
    
    raise HTTPException(status_code=400, detail="email alredy exists")


@router.post("/create-admin/", response_model=UserRead)
async def create_user(user: UserCreateAdmin, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == 'admin':
        verify_user = get_user_by_email(user.mail, db)
        if verify_user is None:
            return create_new_user(user, user.user_role, db)
        raise HTTPException(status_code=401, detail="User already exists")
    raise HTTPException(status_code=401, detail="Not authorized")


#update user, solo dar token usurios activos, todo lo de categorias insert, update, solo el admin puede modificar eliminar categorias crear
# el admin puede hacerlo de todos el usuario solo de el mismo





@router.get("/get/{user_id}", response_model=UserRead)
def read_user(user_id: str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" or current_user.user_id == user_id:
        user = get_user_by_id(user_id, db)
        if user is None:
            print("holaaaaaaa")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    raise HTTPException(status_code=401, detail="Invalid Token")
    
    
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.user_id} )
    return {"access_token": access_token, "token_type": "bearer"}