from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from apps import crud
from api.depends import get_db


router = APIRouter(tags=["public"])

@router.get("/", response_class=HTMLResponse)
def get_announcements(url):
    dataframe = crud.get_dataframe(url)
    response = (dataframe.style).to_html()
    crud.create_announcements(dataframe)
    return response

@router.get("/announcements")
def get_ann(db: Session = Depends(get_db)):
    users = crud.get_announcements(db)
    return users