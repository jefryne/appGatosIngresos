from pydantic import BaseModel


class BaseCategory(BaseModel):
    category_name: str
    category_description: str

class CategoryCreate(BaseCategory):
    pass

class CategoryUpdate(BaseCategory):
    category_id: int 

class DeleteCategory(BaseModel):
    category_id: int 
    category_status: bool


class CategoryRead(BaseCategory):
    category_id: int 
    category_status: bool