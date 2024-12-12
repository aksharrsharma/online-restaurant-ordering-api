from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import payments as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_payment = model.Payment(
        description = request.description,
        amount = request.amount,
        timestamp = request.timestamp,
        promo = request.promo
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(error.__dict__['orig'])
        )

    return new_payment

def read_all(db: Session):
    try:
        payments = db.query(model.Payment).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return payments

def read_one(db: Session, item_id):
    try:
        payment = db.query(model.Payment).filter(model.Payment.id == item_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment ID not found"
            )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return payment

def update(db: Session, item_id, request):
    try:
        payment_query = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not payment_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment ID not found"
            )
        update_data = request.dict(exclude_unset=True)
        payment_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return payment_query.first()

def delete(db: Session, item_id):
    try:
        payment_query = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not payment_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment ID not found"
            )
        payment_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)