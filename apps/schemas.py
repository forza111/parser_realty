from pydantic import BaseModel


class Announcement(BaseModel):
    id: int
    description: str
    price_in_rub: str
    price_in_eur: str
    price_note: str
    placement_date: str
    photo_url: str
    url_addres: str

    class Config:
        orm_mode = True
