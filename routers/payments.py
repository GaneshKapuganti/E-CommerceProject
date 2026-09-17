from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.payment import Payment
from models.order import Order
from schemas.payment import PaymentCreate,PaymentResponse,PaymentListResponse

router = APIRouter(prefix="/api/v1/payments",tags=["Payments"])

@router.post("",response_model=PaymentResponse,status_code=201)
def create_payment(payment: PaymentCreate,db: Session = Depends(get_db)):
    order = (db.query(Order).filter(Order.id == payment.order_id).first())
    if order is None:
        raise HTTPException(status_code=404,detail="Order not found")
    if payment.transaction_id is not None:
        existing_payment = (db.query(Payment).filter(Payment.transaction_id == payment.transaction_id).first())
        if existing_payment:
            raise HTTPException(status_code=400,detail="Transaction ID already exists")

    new_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=payment.status,
        transaction_id=payment.transaction_id
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("",response_model=PaymentListResponse)
def get_payments(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)):
    query = db.query(Payment)
    total = query.count()
    payments = (query.offset(offset).limit(limit).all())
    return {"total": total,"limit": limit,"offset": offset,"items": payments}

@router.get("/{payment_id}",response_model=PaymentResponse)
def get_payment(payment_id: int,db: Session = Depends(get_db)):

    payment = (db.query(Payment).filter(Payment.id == payment_id).first())

    if payment is None:
        raise HTTPException(status_code=404,detail="Payment not found")
    return payment