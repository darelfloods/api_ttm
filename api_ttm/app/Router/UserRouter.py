from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import UserController
from ..Schema import UserSchema


router = APIRouter()


@router.get("/all", tags=["Utilisateurs"], response_model=list[UserSchema.Schema])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.get_all(db)


@router.post("/add", tags=["Utilisateurs"], response_model=UserSchema.Read, status_code=status.HTTP_201_CREATED)
async def add(
        user: UserSchema.Create,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.add(db=db, user=user, request=request)


@router.put("/update/{id}", tags=["Utilisateurs"])
async def update_user(
        id: int,
        user: UserSchema.Read,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.update_user(db=db, user=user, id=id, current_user=current_user, request=request)


@router.put("/update_password/{user_id}", tags=["Utilisateurs"])
async def update_password(
        user_id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        new_password: str,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.update_password(db=db, user_id=user_id, new_password=new_password,
                                                current_user=current_user, request=request)


@router.put("/recovery_password/{email}", tags=["Utilisateurs"])
async def recovery_password(
        email: str,
        background_tasks: BackgroundTasks,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.recovery_password(db=db, email=email, background_tasks=background_tasks,
                                                  request=request)


@router.delete("/delete/{id}", tags=["Utilisateurs"])
async def delete_user(
        id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await UserController.delete_user(db=db, id=id, current_user=current_user, request=request)
