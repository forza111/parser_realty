from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import HttpUrl

from apps import crud


router = APIRouter(tags=["public"])

@router.get("/", response_class=HTMLResponse)
def get_announcements(url: HttpUrl):
    """
    ## Performing page parsing at the given URL.

    Query Parameters
    ----------
    * url: HttpUrl
      #### example: https://www.avito.ru/moskva/nedvizhimost

    Returns
    -------
    html table with extracted data.
    """
    dataframe = crud.get_dataframe(url)
    response = (dataframe.style).to_html()
    crud.create_announcements(dataframe)
    return response
