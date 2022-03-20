from sqlalchemy import Column, Integer, String

from db.database import Base

class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200))
    price_in_rub = Column(String(50))
    price_in_eur = Column(String(50))
    price_note = Column(String(50), nullable=True)
    placement_date = Column(String(50))
    photo_url = Column(String(50))
    url_address = Column(String(50))

    class Config:
        orm_mode = True
