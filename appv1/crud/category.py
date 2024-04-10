import sys

from appv1.models.Category import Category
from fastapi import HTTPException
from appv1.schemas.categorys import CategoryCreate, CategoryUpdate, DeleteCategory
from sqlalchemy.orm import Session



def create_new_category(new_category: CategoryCreate, db: Session):
    db_category = Category(
        category_name = new_category.category_name,
        category_description = new_category.category_description
    )
    
    try: 
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al crear categoria: {str(e)}",  file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al crear categoria: {str(e)}")



def update_category(category: CategoryUpdate, db: Session):
    db_category = get_category_by_id(category.category_id, db)
    if not db_category:
        raise HTTPException(status_code=400, detail="El categoria no existe")

    db_category.category_name = category.category_name
    db_category.category_description = category.category_description
    

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al  actualizar categoria: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al actualizar categoria: {str(e)}")
    


def delete_Category(category: DeleteCategory, db: Session):
    db_category = get_category_by_id(category.category_id, db)
    if not db_category:
        raise HTTPException(status_code=400, detail="El categoria no existe")

    db_category.category_status = category.category_status

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")



def get_category_by_id(id: int, db: Session):
    category = db.query(Category).filter(Category.category_id == id).first()
    return category


def get_all_categories(db: Session):
    categorys = db.query(Category).all()
    return categorys