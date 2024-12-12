from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import reviews as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_review = model.Reviews(
        description = request.description,
        rating = request.rating
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(error.__dict__['orig'])
        )

    return new_review

def read_all(db: Session):
    try:
        reviews = db.query(model.Reviews).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return reviews

def read_one(db: Session, item_id):
    try:
        review = db.query(model.Reviews).filter(model.Reviews.id == item_id).first()
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review ID not found"
            )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return review

def update(db: Session, item_id, request):
    try:
        review_query = db.query(model.Reviews).filter(model.Reviews.id == item_id)
        if not review_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review ID not found"
            )
        update_data = request.dict(exclude_unset=True)
        review_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return review_query.first()

def delete(db: Session, item_id):
    try:
        review_query = db.query(model.Reviews).filter(model.Reviews.id == item_id)
        if not review_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review ID not found"
            )
        review_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
