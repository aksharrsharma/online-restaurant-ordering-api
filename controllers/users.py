from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import users as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_user = model.User(
        name = request.name,
        email = request.email,
        password = request.password,
        user_type = request.user_type
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(error.__dict__['orig'])
        )

    return new_user

def read_all(db: Session):
    try:
        users = db.query(model.User).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return users

def read_one(db: Session, item_id):
    try:
        user = db.query(model.User).filter(model.User.id == item_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User ID not found"
            )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return user

def update(db: Session, item_id, request):
    try:
        user_query = db.query(model.User).filter(model.User.id == item_id)
        if not user_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User ID not found"
            )
        update_data = request.dict(exclude_unset=True)
        user_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return user_query.first()

def delete(db: Session, item_id):
    try:
        user_query = db.query(model.User).filter(model.User.id == item_id)
        if not user_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User ID not found"
            )
        user_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
