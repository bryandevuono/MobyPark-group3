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
    
    return new_vehicle

@router.get("/vehicles", response_model=List[schemas.Vehicle])
async def get_vehicles(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    page: PageParams = Depends(page_params),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    check_token(token.credentials)
    
    query = select(models.Vehicle).where(models.Vehicle.users_id == current_user.id).offset(page.offset).limit(page.limit)
    result = await db.execute(query)
    vehicles = result.scalars().all()
    
    return vehicles

@router.put("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: schemas.VehicleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    check_token(token.credentials)
    
    result = await db.execute(
        select(models.Vehicle).where(
            models.Vehicle.id == vehicle_id,
            models.Vehicle.users_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    if vehicle_update.license_plate is not None:
        vehicle.license_plate = vehicle_update.license_plate
        vehicle.license_plate_clean = licenceplate_clean(vehicle_update.license_plate)
    if vehicle_update.make is not None:
        vehicle.make = vehicle_update.make
    if vehicle_update.model is not None:
        vehicle.model = vehicle_update.model
    if vehicle_update.color is not None:
        vehicle.color = vehicle_update.color
    if vehicle_update.year is not None:
        vehicle.year = vehicle_update.year
    
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    
    return vehicle
@router.delete("/vehicles/{vehicle_id}", response_model=dict)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    check_token(token.credentials)
    
    result = await db.execute(
        select(models.Vehicle).where(
            models.Vehicle.id == vehicle_id,
            models.Vehicle.users_id == current_user.id
        )
    )
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    await db.delete(vehicle)
    await db.commit()
    
    return {"detail": "Vehicle deleted successfully"}