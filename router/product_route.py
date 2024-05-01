from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import models.schemas as schemas
import models.models as models
from database.database import SessionLocal
from typing import List
from router.login_route import get_current_user

router = APIRouter(tags = ["Products"],
                   prefix = '/product')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', 
         response_model = List[schemas.DisplayProduct], 
         status_code = status.HTTP_200_OK, 
         )
def get_products(db: Session = Depends(get_db)):
        try:
            products = db.query(models.Product)\
                         .all()
            return products
        except:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,\
                                detail = "Due to internal server details the system stopped working")
    
@router.get('/{id}', response_model = schemas.DisplayProduct, )
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product)\
                .filter(models.Product.id == id)\
                .first()
    if product:
        return product
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,\
                                detail = f"Product with id {id} is not found")
    
@router.delete('/{id}',
            )
def delete_product(id: int, db: Session = Depends(get_db),\
                    current_user: schemas.Seller = Depends(get_current_user)):
    try:
        get_product(id, db)
        db.query(models.Product)\
          .filter(models.Product.id == id)\
          .delete(synchronize_session = False)
        db.commit()
        return {f"Product with id {id} is deleted"}
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,\
                                detail = f"Product with id {id} is not , cannot be deleted")

@router.put('/{id}', )
def update_product(id: int, request: schemas.Product, db: Session = Depends(get_db)\
                   , current_user: schemas.Seller = Depends(get_current_user)):
    try:
        get_product(id, db)
        db.query(models.Product)\
          .filter(models.Product.id == id)\
          .update(dict(request))
        db.commit()
        return {f"Product with id {id} is updated"}
    except HTTPException as ex:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,\
                                detail = f"Product with id {id} is not , cannot be updated")

@router.post('', 
          response_model = schemas.DisplayProduct, 
          status_code=status.HTTP_201_CREATED, 
          )
def add_products(request: schemas.Product = Depends(), db: Session = Depends(get_db)\
                   , current_user: schemas.Seller = Depends(get_current_user)):
    try:
        new_product = models.Product(name = request.name,\
                                 description = request.description,\
                                 price = request.price,
                                 seller_id = request.seller_id)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,\
                                detail = "Due to internal server details the system stopped working")