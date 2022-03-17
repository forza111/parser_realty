from pydantic import HttpUrl
from fastapi.responses import FileResponse

from core.main import app

@app.get("/")
def main(url: HttpUrl):
    """
    ## Performing page parsing at the given URL.
    Query Parameters
    ----------
    * url: HttpUrl
      #### example: https://www.timberland.com/shop/mens-boots
    * width: Optional[int (10-100)] Width line (DEFAULT 60).
    * image_url: Optional[bool] Display image url (DEFAULT False).
    Returns
    -------
    .txtFile with extracted data.
    """

    path = get_content(url)
    return FileResponse(path)