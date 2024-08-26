from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from constants import scrap_page_limit, STATIC_TOKEN
from domain.domain import ProductScrapper
from domain.product_scrapper import get_scrapper

app = FastAPI()
security = HTTPBearer()


def token_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/api/v1/scrap", dependencies=[Depends(token_auth)])
def scrap(background_tasks: BackgroundTasks, limit: int = scrap_page_limit, proxy: Optional[str] = None,
          scrapper: ProductScrapper = Depends(get_scrapper)):
    """
    :param scrapper: inject dependency of scrapper
    :param limit: how many pages to be scrapped
    :param proxy: proxy server url
    :return: None
    """
    scrapper.set_background_task(background_tasks)
    scrapper.scrap(limit, proxy=proxy)
    print("finished scrapping...")
