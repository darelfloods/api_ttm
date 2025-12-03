import json

from fastapi import APIRouter, Depends, Request
import requests
from sqlalchemy.orm import Session
from typing import Annotated, Dict

from ..Middleware import DatabaseSession, IsAuthenticated
from ..Controller import MyPayGaController
from ..Schema import MyPayGaSchema, UserSchema
try:
    from core.config import settings
except ModuleNotFoundError:
    from api_ttm.core.config import settings


router = APIRouter()


@router.post("/subscribe_pricing", tags=["My Pay Ga"])
async def get_all(
        my_pay_ga: MyPayGaSchema.Create,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "urls": {
            "success_url": settings.success_url,
            "callback_url": f"{settings.callback_url}/{current_user.id}/{my_pay_ga.rate_id}",
            "fail_url": settings.fail_url
        },
        "apikey": settings.apikey,
        "client_phone": my_pay_ga.client_phone,
        "amount": my_pay_ga.amount,
        "country": settings.country,
        "network": my_pay_ga.network,
        "type": settings.type,
        "unique_id": MyPayGaController.generate_unique_id(),
        "firstname": "ttm",
        "lastname": my_pay_ga.lastname,
        "email": my_pay_ga.email
    }
    # verif = await MyPayGaController.take_rate(db=db, current_user=current_user, rate_id=my_pay_ga.rate_id,
    #                                           request=request)
    request_my_pay_ga = requests.post(settings.link_payment, data=json.dumps(body), headers=headers).json()

    if request_my_pay_ga['request_status'] == '200':
        # await MyPayGaController.take_rate(db=db, current_user=current_user, rate_id=my_pay_ga.rate_id, request=request)
        return {"success_url": settings.success_url, "message": request_my_pay_ga['message'],
                "transaction": request_my_pay_ga['transaction'], "request_status": request_my_pay_ga['request_status']}
    else:
        return {"fail_url": settings.fail_url, "message": request_my_pay_ga['message']}


@router.post("/callback_url/{user_id}/{rate_id}", tags=["My Pay Ga"])
async def callback_function(
        user_id: int,
        rate_id: int,
        body: Dict,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    print(f"ça callback_url: {body}")
    print(f"ça user_id: {user_id}")

    # L'API MyPayGa peut renvoyer order_status en string ou en nombre, avec 0 ou 200 comme succès
    raw_status = body.get('order_status') or body.get('request_status')
    try:
        status = int(str(raw_status))
    except (TypeError, ValueError):
        status = None

    if status in (0, 200):
        await MyPayGaController.take_rate_by_id(db=db, user_id=user_id, rate_id=rate_id, request=request)
        return {"message": body.get('message'), "request_status": raw_status}
    else:
        return {"message": body.get('message'), "request_status": raw_status}


@router.post("/success_url", tags=["My Pay Ga"])
async def callback_function(request: Request, body: Dict):
    print(f"ça success_url: {body}")


@router.post("/fail_url", tags=["My Pay Ga"])
async def callback_function(request: Request, body: Dict):
    print(f"ça fail_url: {body}")
