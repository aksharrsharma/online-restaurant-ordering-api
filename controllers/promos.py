from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import promos as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_promo = model.Promos(
        code = request.code,
        percent_off = request.percent_off,
        expiration = request.expiration
    )

    try:
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(error.__dict__['orig'])
        )

    return new_promo

def read_all(db: Session):
    try:
        promos = db.query(model.Promos).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return promos

def read_one(db: Session, item_id):
    try:
        promo = db.query(model.Promos).filter(model.Promos.id == item_id).first()
        if not promo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promo ID not found"
            )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return promo

def update(db: Session, item_id, request):
    try:
        promo_query = db.query(model.Promos).filter(model.Promos.id == item_id)
        if not promo_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promo ID not found"
            )
        update_data = request.dict(exclude_unset=True)
        promo_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return promo_query.first()

def delete(db: Session, item_id):
    try:
        promo_query = db.query(model.Promos).filter(model.Promos.id == item_id)
        if not promo_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promo ID not found"
            )
        promo_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)