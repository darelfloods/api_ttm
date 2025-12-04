from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List
import requests
import json
import logging
import traceback
from requests.exceptions import Timeout, ConnectionError
from bson import ObjectId

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Schema import ProductSchema, UserSchema, EventSchema
from ..Controller import EventController
from core.config import settings
from ..Db.Connection import get_db, products_collection
from ..Db.Model.ProductModel import Product
from ..Schema.ProductSchema import Read, Create

router = APIRouter()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

X_API_KEY = settings.X_API_KEY
EPG_SUPERVISOR_ADDRESS = settings.EPG_SUPERVISOR_ADDRESS
ADMIN_PANEL = settings.ADMIN_PANEL
LARAVEL_API_URL = "http://localhost:8000"



@router.get("/all_products/{page}/{count}", tags=["Consommation depuis l'API EPG"])
async def make_request(page: int, count: int):
    try:
        logger.info(f"Début de la requête all_products avec page={page}, count={count}")
        headers = {
            "x-api-key": X_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Test de connexion rapide
        try:
            logger.info("Test de connexion au serveur EPG...")
            test_response = requests.get(
                EPG_SUPERVISOR_ADDRESS,
                timeout=5,
                verify=False
            )
            logger.info(f"Test de connexion: Status={test_response.status_code}")
        except ConnectionError as e:
            error_msg = f"Impossible de se connecter au serveur EPG: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_msg
            )
        except Timeout:
            error_msg = "Le serveur EPG ne répond pas au test de connexion"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=error_msg
            )
        
        # Requête principale avec un timeout plus court
        url = f"{EPG_SUPERVISOR_ADDRESS}/api/produits?page={page}&count={count}"
        logger.info(f"Envoi de la requête à {url}")
        
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10,  # Timeout réduit à 10 secondes
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info("Données reçues avec succès")
                return data
            else:
                error_msg = f"Erreur du serveur EPG: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_msg
                )
                
        except Timeout:
            error_msg = "Le serveur EPG met trop de temps à répondre"
            logger.error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=error_msg
            )
            
    except Exception as e:
        error_msg = f"Erreur inattendue: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )



@router.get("/produits/recherche_par_libelle/{libelle}", tags=["rechercherProduits"])
async def products_searched(libelle: str):
    # Construire l'URL avec paramètre GET
    url = f"{ADMIN_PANEL}api/produits/recherche_par_libelle"
    
    # Requête vers Laravel
    response = requests.get(url, params={"libelle": libelle})

    # Retourner la réponse en JSON
    return response.json()


@router.post("/disponibility_product", tags=["Consommation depuis l'API EPG"])
async def getDisponibiliteProduit(
        data: ProductSchema.Base,
        request: Request,
        # current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        db: Session = Depends(DatabaseSession.get_db)
):
    body = {"pharmacy": data.pharmacy, "cips": [data.cip]}
    print(f"contenue du data récupérer par ttm front {data}")
    print(f"contenue du body récupérer par ttm front {body}")
    response = requests.get(f"{ADMIN_PANEL}/api/produits/{data.cip}/disponibilite")
    print(f"response from panel_admin {response.status_code}")
    return response.json()
    # event = EventSchema.Create(
    #     action="Disponibilité d'un produit",
    #     entity="api_epg",
    #     entity_id=data.cip,
    #     current_user_id=f"{current_user.id}"
    # )
    # await EventController.add(db=db, event=event, request=request)
    # headers = {
    #     "x-api-key": X_API_KEY,
    #     "Content-Type": "application/json"
    # }
    # body = {"pharmacy": data.pharmacy, "cips": [data.cip]}
    # response = requests.post(f"{EPG_SUPERVISOR_ADDRESS}/open-api/disponibilite",
    #                          data=json.dumps(body), headers=headers, timeout=5)

    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     raise HTTPException(status_code=response.status_code, detail="Request failed")


@router.post("/reservation", tags=["Consommation depuis l'API EPG"])
async def reservation(
        data: ProductSchema.Reservation,
        request: Request,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        db: Session = Depends(DatabaseSession.get_db)
):
    headers = {
        "x-api-key": X_API_KEY,
        "content-type": "application/json"
    }
    data1 = {"pharmacy": data.pharmacy, "buyer": f"{current_user.lastname}",
                "buyerPhone": current_user.phone,
                "buyerEmail": current_user.email, "produits": data.produits}
    response = requests.post(f"{EPG_SUPERVISOR_ADDRESS}/open-api/reservation",
                             json.dumps(data1), headers=headers, timeout=5)
    print(f"Voila la requête: {response.request.body}")
    if response.status_code == 200:
        print(f"La requête a réussit")
        event = EventSchema.Create(
            action="Réservation d'un produit",
            entity="api_epg",
            entity_id=data.pharmacy,
            current_user_id=f"{current_user.id}"
        )
        await EventController.add(db=db, event=event, request=request)
        return response.json()
    else:
        print(f"La requête a échoué")
        raise HTTPException(status_code=response.status_code, detail="Request failed1")


@router.get("/all_products", response_model=List[Read])
async def get_all_products():
    """
    Récupère la liste de tous les produits depuis MongoDB
    """
    products = []
    async for product in products_collection.find():
        # Convertir l'ObjectId en str pour la sérialisation JSON
        product["id"] = str(product.pop("_id"))
        products.append(product)
    return products


@router.post("/products", response_model=Read, status_code=status.HTTP_201_CREATED)
async def create_product(product: Create):
    """
    Crée un nouveau produit dans MongoDB
    """
    product_dict = product.dict()
    result = await products_collection.insert_one(product_dict)
    created_product = await products_collection.find_one({"_id": result.inserted_id})
    created_product["id"] = str(created_product.pop("_id"))
    return created_product
