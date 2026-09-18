from sqlalchemy.orm import Session

from models.payment import Payment


def get_by_id(db: Session, payment_id: int) -> Payment | None:
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_by_transaction_id(db: Session, transaction_id: str) -> Payment | None:
    return db.query(Payment).filter(Payment.transaction_id == transaction_id).first()


def get_multi(db: Session, limit: int, offset: int) -> tuple[int, list[Payment]]:
    query = db.query(Payment)
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return total, items


def create(
    db: Session,
    order_id: int,
    amount: float,
    payment_method: str,
    status: str,
    transaction_id: str | None,
) -> Payment:
    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method=payment_method,
        status=status,
        transaction_id=transaction_id,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
