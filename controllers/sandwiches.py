from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    sandwich = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price
    )
    try:
        db.add(sandwich)
        db.commit()
        db.refresh(sandwich)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return sandwich

def read_all(db: Session):
    try:
        return db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )

def read_one(db: Session, item_id):
    try:
        sandwich = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
        if not sandwich:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return sandwich

def update(db: Session, item_id, request):
    try:
        sandwich_query = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not sandwich_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
        update_data = request.dict(exclude_unset=True)
        sandwich_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return sandwich_query.first()

def delete(db: Session, item_id):
    try:
        sandwich_query = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not sandwich_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sandwich not found"
            )
        sandwich_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)