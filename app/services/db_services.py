from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TronAddress
from app.schemas import AddressInfoResponse, PaginatedResponse


class DatabaseService:
    async def create_address_request(self, db: AsyncSession, info: AddressInfoResponse):
        db_request = TronAddress(
            address=info.address,
            bandwidth=info.bandwidth,
            energy=info.energy,
            trx_balance=info.trx_balance,
        )
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)
        return db_request

    async def get_address_requests(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10
    ) -> PaginatedResponse:
        total = (await db.execute(select(func.count()).select_from(TronAddress))).scalar_one()

        query = await db.execute(
            select(TronAddress)
            .order_by(TronAddress.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = query.scalars().all()

        return PaginatedResponse(
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            page_size=limit,
            items=result,
        )
