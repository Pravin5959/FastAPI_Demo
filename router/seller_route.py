from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import models.schemas as schemas
import models.models as models
from database.database import SessionLocal
from typing import List
from passlib.context import CryptContext

from router.login_route import get_current_user

router = APIRouter(tags = ["Sellers"],
                   prefix = '/seller')

pwd_context = CryptContext(schemes = ["bcrypt"],\
                          deprecated = "auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('', 
          response_model = schemas.DisplaySeller, 
          status_code = status.HTTP_201_CREATED,
          )
def add_seller(request: schemas.Seller = Depends(), db: Session = Depends(get_db)\
                   , current_user: schemas.Seller = Depends(get_current_user)):
    try:
        new_seller = models.Seller(name = request.name,\
                                 email = request.email,\
                                 password = pwd_context.hash(request.password))
        print(new_seller)
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        return new_seller
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,\
                                detail = "Due to internal server details the system stopped working")