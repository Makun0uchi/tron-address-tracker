import asyncio
from concurrent.futures import ThreadPoolExecutor

from tronpy import Tron
from tronpy.exceptions import AddressNotFound

from app.config import settings
from app.schemas import AddressInfoResponse


class TronService:
    def __init__(self):
        self.client = Tron(network=settings.tron_network)
        self.executor = ThreadPoolExecutor()

    async def get_address_info(self, address: str) -> AddressInfoResponse:
        loop = asyncio.get_event_loop()
        try:
            account = await loop.run_in_executor(
                self.executor,
                lambda: self.client.get_account(address)
            )

            return AddressInfoResponse(
                address=address,
                bandwidth=account.get('net_window_size'),
                energy=account.get('account_resource', {}).get('energy_window_size'),
                trx_balance=account.get('balance')
            )
        except AddressNotFound:
            raise ValueError('Address not found on Tron network')

    async def close(self):
        self.executor.shutdown(wait=True)
