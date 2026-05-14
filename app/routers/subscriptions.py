from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from dateutil.relativedelta import relativedelta

from app.auth.auth import TokenData, decode_token
from app.database import  add_subscription_query, get_subscription_query, \
    cancel_subscription_query, has_active_subscription, update_subscription_query
from app.models.models import SubscriptionOut

router = APIRouter(
    prefix="/subscription",
    tags=["Subscriptions"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_subscription(type: str, token: TokenData = Depends(decode_token)):
    end_date = date.today()

    weekly_type = {"standard", "premium"}
    yearly_type = {"standard_yearly", "premium_yearly"}

    type_lower = type.lower()
    if type_lower not in weekly_type.union(yearly_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be one of: standard, standard_yearly, premium and premium_yearly"
        )
    family = get_family(type_lower)

    if has_active_subscription(token.username, family):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active or pending subscription. Cancel it or wait for it to expire before creating a new one."
        )
    
    if type_lower in weekly_type:
        end_date += relativedelta(months=1)
    elif type_lower in yearly_type:
        end_date += relativedelta(years=1)

    return add_subscription_query(token.username, type_lower, end_date)

@router.get("/me/", response_model=SubscriptionOut)
def get_user_subscription(token: TokenData = Depends(decode_token)):
    subs = get_subscription_query(token.username)

    # isinstance detecta casos informativo y devuelve en 404 el mensaje de la query
    if isinstance(subs, str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=subs
        )
    return subs

@router.delete("/me/", response_model=SubscriptionOut)
def cancel_subscription(token: TokenData = Depends(decode_token)):
    cancel = cancel_subscription_query(token.username)
    if not cancel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription to cancel."
        )
    return cancel

# Cancelar subscripcion, actualizar
# Perfiles se crean con usuarios con subscripcion
# Yo, Payment, User, Subscripcion, profile, añadir tokens diferentes
# Gerardas, content, genre, history, rating

# Función auxiliar
def get_family(subtype: str) -> str:
    subtype = subtype.lower()
    if subtype.startswith("standard"):
        return "standard"
    elif subtype.startswith("premium"):
        return "premium"
    return ""

@router.put("/me/", response_model=SubscriptionOut)
def update_subscription(new_type: str, token: TokenData = Depends(decode_token)):
    end_date = date.today()

    type_lower = new_type.lower()
    family = get_family(type_lower)
    weekly_type = {"standard", "premium"}
    yearly_type = {"standard_yearly", "premium_yearly"}

    if has_active_subscription(token.username, family):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have a similar type of subscription"
        )
    
    if type_lower in weekly_type:
        end_date += relativedelta(months=1)
    elif type_lower in yearly_type:
        end_date += relativedelta(years=1)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be one of: standard, premium, standard_yearly, premium_yearly"
        )

    return update_subscription_query(token.username, type_lower, end_date)



# IDEA:
# Añadir un nuevo estado "pending" al ENUM de SUBSCRIPTION.
# De esta forma, cuando un usuario crea una subscripción, esta se registra primero como "pending",
# sin dar acceso todavía al contenido.
# El proceso de pago se gestiona en un endpoint separado; cuando el pago se completa correctamente,
# se actualiza el estado de la subscripción a "active".
# Así evitamos subscripciones activas sin pago confirmado y mantenemos la lógica más clara y segura.