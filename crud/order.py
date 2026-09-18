from sqlalchemy.orm import Session

from models.order import Order


def get_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_multi(db: Session,limit:int,offset:int,user_id: int,status:str):
    query = db.query(Order)
    if user_id is not None:
        query = query.filter(Order.user_id == user_id)
    if status is not None:
        query = query.filter(Order.status == status)
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return total, items


def create(db: Session, user_id: int, status: str, total_amount: float):
    order = Order(user_id=user_id, status=status, total_amount=total_amount)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_status(db: Session, order: Order, status: str):
    order.status = status
    db.commit()
    db.refresh(order)
    return order
