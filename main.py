import os
import sys

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# S'assurer que le dossier contenant main.py est dans sys.path
# Cela fonctionne à la fois en local (python main.py) et sur Render (Root Directory = api_ttm)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.config import settings
from app.Api import ProductApi, SingPayApi, MyPayGaApi
from app.Db import Migration, Connection
from app.Router import AuthRouter, UserRouter, RateRouter, AccountRouter, EventRouter, PriceListRouter


Migration.Base.metadata.create_all(bind=Connection.engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Erreur interne au serveur", status_code=500)
    try:
        request.state.db = Connection.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()

    return response

app.include_router(AuthRouter.router, prefix="/auth")
app.include_router(UserRouter.router, prefix="/user")
app.include_router(RateRouter.router, prefix="/rate")
app.include_router(AccountRouter.router, prefix="/account")
app.include_router(PriceListRouter.router, prefix="/price_list")
app.include_router(EventRouter.router, prefix="/event")
app.include_router(ProductApi.router, prefix="/api_epg")
app.include_router(SingPayApi.router, prefix="/sing_pay_api")
app.include_router(MyPayGaApi.router, prefix="/my_pay_ga")


@app.get("/")
def read_root():
    return {"msg": "Serveur démarré"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,  # Port 443 pour SSL
        #ssl_keyfile="/etc/docker/certs/epharma_cle_privee_nopass.key",  # Chemin vers votre clé privée
        #ssl_certfile="/etc/docker/certs/51_68_46_67.crt",  # Chemin vers votre certificat
        #ssl_ca_certs="/etc/docker/certs/SectigoRSADomainValidationSecureServerCA.crt"  # Optionnel: Chemin vers le certificat intermédiaire
    )
