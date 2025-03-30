from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services

from .database import get_db

app = FastAPI()

tron_service = services.TronService()
db_service = services.DatabaseService()


@app.post('/address-info/', response_model=schemas.AddressInfoResponse)
async def get_address_info(request: schemas.AddressInfoRequest, db: AsyncSession = Depends(get_db)):
    try:
        info = await tron_service.get_address_info(request.address)
        await db_service.create_address_request(db, info)
        return info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/request-history/', response_model=schemas.PaginatedResponse)
async def get_request_history(db: AsyncSession = Depends(get_db)):
    try:
        result = await db_service.get_address_requests(db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Failed to fetch request history: {str(e)}'
        )
