from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models.recipes import Recipe
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_recipe = Recipe(
        sandwich_id=request.sandwich_id,
        resource_id=request.resource_id,
        amount=request.amount
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )

    return new_recipe


def read_all(db: Session):
    try:
        recipes = db.query(Recipe).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return recipes


def read_one(db: Session, item_id):
    try:
        recipe = db.query(Recipe).filter(Recipe.id == item_id).first()
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return recipe


def update(db: Session, item_id, request):
    try:
        recipe_query = db.query(Recipe).filter(Recipe.id == item_id)
        if not recipe_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )
        update_data = request.dict(exclude_unset=True)
        recipe_query.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return recipe_query.first()


def delete(db: Session, item_id):
    try:
        recipe_query = db.query(Recipe).filter(Recipe.id == item_id)
        if not recipe_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )
        recipe_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error.__dict__['orig'])
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)