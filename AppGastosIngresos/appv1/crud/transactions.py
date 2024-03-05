import sys

from appv1.models.Transactions import Transactions
from fastapi import HTTPException
from appv1.schemas.transactions import CreateTransaction, UpdateTransaction
from sqlalchemy.orm import Session



def create_new_transaction(new_transaction: CreateTransaction, db: Session):
    db_transaction = Transactions(
        user_id = new_transaction.user_id,
        category_id = new_transaction.category_id,
        amount = new_transaction.amount,
        t_description = new_transaction.t_description,
        t_type = new_transaction.t_type,
        t_date = new_transaction.t_date
    )
    
    try: 
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        print(f"Error al crear categoria: {str(e)}",  file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al crear categoria: {str(e)}")



def update_transaction(transaction: UpdateTransaction, db: Session):
    db_transaction = get_transaction_by_id(transaction.transactions_id, db)
    if not db_transaction:
        raise HTTPException(status_code=400, detail="transaction not found")

    db_transaction.user_id = transaction.user_id,
    db_transaction.category_id = transaction.category_id,
    db_transaction.amount = transaction.amount,
    db_transaction.t_description = transaction.t_description,
    db_transaction.t_type = transaction.t_type.name
    db_transaction.t_date = transaction.t_date

    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        print(f"Error al  actualizar categoria: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Error al actualizar transaccion: {str(e)}")
    


def get_transaction_by_id(id: int, db: Session):
    transactions = db.query(Transactions).filter(Transactions.transactions_id == id).first()
    return transactions


def get_transaction_by_user(id: int, db: Session):
    transactions = db.query(Transactions).filter(Transactions.user_id == id).all()
    return transactions



def get_all_transaction(db: Session):
    transactions = db.query(Transactions).all()
    return transactions