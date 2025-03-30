from pydantic import BaseModel


class AddressInfoRequest(BaseModel):
    address: str


class AddressInfoResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    trx_balance: int

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[AddressInfoResponse]
