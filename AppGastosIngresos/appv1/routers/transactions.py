from typing import List
from fastapi import APIRouter, Depends, HTTPException
from appv1.schemas.users import  UserRead
from sqlalchemy.orm import Session
from core.token import get_current_user
from db.session import get_session
from appv1.crud.transactions import create_new_transaction, update_transaction, get_transaction_by_id, get_all_transaction, get_transaction_by_user
from appv1.schemas.transactions import CreateTransaction, UpdateTransaction, TransactionRead

router = APIRouter()

@router.post("/create-transaction/", response_model=CreateTransaction)
async def create_transaction(transaction: CreateTransaction, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="El monto no puede ser menor o igual a 0")
    if current_user.user_role == 'user' and transaction.user_id == current_user.user_id:
        return create_new_transaction(transaction, db)
    raise HTTPException(status_code=401, detail="Not authorized")



@router.put("/update-transaction/", response_model=UpdateTransaction)
def update_transaction_route(transaction: UpdateTransaction, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="El monto no puede ser menor o igual a 0")
    if transaction.user_id == current_user.user_id:
        if transaction is not None: 
            transaction_updated = update_transaction(transaction, db)
            if transaction_updated is None:
                raise HTTPException(status_code=404, detail="transaction not found")
            return transaction_updated
        else:
            raise HTTPException(status_code=400, detail="transaction data cannot be empty")
    raise HTTPException(status_code=401, detail="Invalid Token user not authorized")


@router.get("/get/{transaction_id}", response_model=TransactionRead)
def read_category(transaction_id: int, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    transaction = get_transaction_by_id(transaction_id, db)
    if transaction is None:
        raise HTTPException(status_code=404, detail="transaction not found")
    if current_user.user_role == "admin" or transaction.user_id == current_user.user_id:
       return transaction
    raise HTTPException(status_code=401, detail="Invalid Token")

@router.get("/get/", response_model=List[TransactionRead])
def read_transaction(offzise: int, limit: int, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin":
        transaction = get_all_transaction(offzise,limit,db)
        return transaction
    raise HTTPException(status_code=401, detail="Invalid Token")


@router.get("/get-by-user/{id_user}", response_model=List[TransactionRead])
def read_transaction(id_user: str, db: Session = Depends(get_session), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_role == "admin" or current_user.user_id == id_user:
        transaction = get_transaction_by_user(id_user, db)
        return transaction
    raise HTTPException(status_code=401, detail="Invalid Token user not authorized")