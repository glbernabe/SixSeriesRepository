from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.auth import TokenData, decode_token, oauth2_scheme
from app.database import get_user_by_username, confirm_payment_query, get_payments_query, get_subscription_query, \
    cancel_payment_query
from app.models.models import PaymentOut, PaymentType

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)
@router.post("/add/", response_model=PaymentOut)
async def confirm_payment(method: PaymentType, token: str = Depends(oauth2_scheme)):
    method_accept = {"card", "paypal"}
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    method_lower = method.lower()
    if method_lower not in method_accept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The options are card o paypal"
        )
    payment = confirm_payment_query(user.username, method)
    return payment

@router.get("/me/", response_model=PaymentOut)
async def get_payments(token: str = Depends(oauth2_scheme)):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    payments = get_payments_query(user.username)
    return payments
@router.put("/cancel/{payment_id}")
async def cancel_payment(
        payment_id: str,
        token: str = Depends(oauth2_scheme)
):
    data: TokenData = decode_token(token)
    user = get_user_by_username(data.username)

    if not user:
        raise HTTPException(404, "User not found")

    return cancel_payment_query(payment_id, user.username)

# obtener todos los pagos (solo admin)
# falta funcion que devuelva el status general de una cuenta, tipo si es cliente, status de sub, plan, que dia expira etc...