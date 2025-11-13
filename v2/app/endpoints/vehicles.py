from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database import get_db
from app import models, schemas
from app.security import check_token ,require_admin
from app.dependancies import get_current_user, page_params, PageParams, licenceplate_clean

router = APIRouter(prefix="", tags=["vehicles"])
bearer_scheme = HTTPBearer(auto_error=True)

@router.post("/vehicles", response_model=schemas.Vehicle)
async def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    check_token(token.credentials)

    new_vehicle = models.Vehicle(
        users_id=current_user.id,
        license_plate=vehicle.license_plate,
        license_plate_clean=licenceplate_clean(vehicle.license_plate),
        make=vehicle.make,
        model=vehicle.model,
        color=vehicle.color,
        year=vehicle.year
    )
    
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    
    return vehicle