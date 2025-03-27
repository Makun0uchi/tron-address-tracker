from sqlalchemy import Column, Integer, String

from app.database import Base


class TronAddress(Base):
    __tablename__ = 'tron_address'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    bandwidth = Column(Integer, nullable=True)
    energy = Column(Integer, nullable=True)
    trx_balance = Column(Integer, nullable=True)

    def __str__(self):
        return (f'<TronAddress({self.address}): {self.bandwidth}Mb/s, '
                f'{self.energy}kWh, {self.trx_balance}b>')

    def __repr__(self):
        return str(self)
