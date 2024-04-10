from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from core.token import get_current_user
from db.session import get_session
from appv1.schemas.categorys import  CategoryCreate, CategoryRead, CategoryUpdate, DeleteCategory
from appv1.schemas.users import  UserRead
from appv1.crud.category import create_new_category, delete_Category, get_all_categories, get_category_by_id, update_category


router = APIRouter()


@router.post("/create-category/", response_model=CategoryCreate)
async def create_category(category: CategoryCreate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == 'admin':
        return create_new_category(category, db)
    raise HTTPException(status_code=401, detail="Not authorized")



@router.put("/update-category/", response_model=CategoryRead)
def update_category_route(category: CategoryUpdate, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        if category is not None: 
            category_updated = update_category(category, db)
            if category_updated is None:
                raise HTTPException(status_code=404, detail="User not found")
            return category_updated
        else:
            raise HTTPException(status_code=400, detail="User data cannot be empty")
    raise HTTPException(status_code=401, detail="Invalid Token")


@router.delete("/delete-category/", response_model=CategoryRead)
def update_category_route(category: DeleteCategory, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        if category is not None: 
            category_updated = delete_Category(category, db)
            if category_updated is None:
                raise HTTPException(status_code=404, detail="User not found")
            return category_updated
        else:
            raise HTTPException(status_code=400, detail="User data cannot be empty")
    raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/get/{category_id}", response_model=CategoryRead)
def read_category(category_id: str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        category = get_category_by_id(category_id, db)
        if category is None:
            raise HTTPException(status_code=404, detail="category not found")
        return category
    raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/get/", response_model=List[CategoryRead])
def read_categories(db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        categories = get_all_categories(db)
        return categories
    raise HTTPException(status_code=401, detail="Invalid Token")