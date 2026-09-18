from sqlalchemy.orm import Session

from models.user import User


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_multi(db: Session, limit: int, offset: int) -> tuple[int, list[User]]:
    query = db.query(User)
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return total, items


def create(db: Session, name: str, email: str, password_hash: str) -> User:
    user = User(name=name, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user: User, name: str, email: str, password_hash: str) -> User:
    user.name = name
    user.email = email
    user.password_hash = password_hash
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
