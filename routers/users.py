from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate,UserPatch,UserResponse,UserListResponse
router = APIRouter(prefix="/api/v1/users",tags=["Users"])

@router.post("",response_model=UserResponse,status_code=201)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    existing_user = (db.query(User).filter(User.email == user.email).first())
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    new_user = User(name=user.name,email=user.email,password_hash=user.password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("",response_model=UserListResponse)
def get_users(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)):
    query = db.query(User)
    total = query.count()
    users = (query.offset(offset).limit(limit).all())
    return {"total": total,"limit": limit,"offset": offset,"items": users}

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int,db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id: int,user_data: UserCreate,db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    user.name = user_data.name
    user.email = user_data.email
    user.password_hash = user_data.password_hash
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}",response_model=UserResponse)
def patch_user(user_id: int,user_data: UserPatch,db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password_hash is not None:
        user.password_hash = user_data.password_hash
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}",status_code=204)
def delete_user(user_id: int,db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(user)
    db.commit()
    return None