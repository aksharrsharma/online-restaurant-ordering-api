from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.resources import Resource
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_resource = Resource(
        amount=request.amount,
        item=request.item
    )
    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return new_resource


def read_all(db: Session):
    try:
        return db.query(Resource).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )


def read_one(db: Session, item_id):
    try:
        resource = db.query(Resource).filter(Resource.id == item_id).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return resource


def update(db: Session, item_id, request):
    try:
        resource_to_update = db.query(Resource).filter(Resource.id == item_id)
        if not resource_to_update.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        update_data = request.dict(exclude_unset=True)
        resource_to_update.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return resource_to_update.first()


def delete(db: Session, item_id):
    try:
        resource_to_delete = db.query(Resource).filter(Resource.id == item_id)
        if not resource_to_delete.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        resource_to_delete.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
