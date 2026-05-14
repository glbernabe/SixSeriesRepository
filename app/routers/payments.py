from fastapi import APIRouter, Depends

from app.auth.auth import TokenData, decode_token
from app.database import confirm_payment_query, get_payments_query, cancel_payment_query
from app.models.models import PaymentOut, PaymentType

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)
@router.post("/add/", response_model=PaymentOut)
async def confirm_payment(subscription_id: str, method: PaymentType, token: TokenData = Depends(decode_token)):
    return confirm_payment_query(token.username, method, subscription_id)

@router.get("/me/", response_model=PaymentOut)
async def get_payments(token: TokenData = Depends(decode_token)):
    return get_payments_query(token.username)

@router.put("/cancel/{payment_id}")
async def cancel_payment(payment_id: str, token: TokenData = Depends(decode_token)):
    return cancel_payment_query(payment_id, token.username)

# obtener todos los pagos (solo admin)
# falta funcion que devuelva el status general de una cuenta, tipo si es cliente, status de sub, plan, que dia expira etc...