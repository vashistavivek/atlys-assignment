import requests
from typing import Optional

from bs4 import BeautifulSoup
from fastapi import Depends, BackgroundTasks
from tenacity import stop_after_attempt, wait_fixed, retry, RetryError

from constants import scrap_site_url, RECIPIENTS, RETRY_ATTEMPTS, RETRY_INTERVAL_IN_SECONDS
from domain.domain import ProductScrapper, NotificationService
from domain.notification.sms import get_notification_service
from models.product import Product
from models.user import User
from repository.product import get_product_repository
from repository.repository import ProductRepository


class ProductScrapperImpl(ProductScrapper):

    def __init__(self, pr: ProductRepository = None, ns: NotificationService = None, tasks: BackgroundTasks = None):
        self.repository = pr
        self.notification_service = ns
        self.tasks = tasks

    def set_background_task(self, background_tasks: BackgroundTasks):
        self.tasks = background_tasks

    def scrap(self, limit, proxy: Optional[str] = None):
        print(f"start scrapping from {scrap_site_url} with limit {limit}, proxy: {proxy}")
        for page in range(1, limit + 1):
            try:
                self.tasks.add_task(self.scrap_page, page, proxy)
            except RetryError as ex:
                print(f"error in retry scrapping page: {page}, {ex}")

    @retry(wait=wait_fixed(RETRY_INTERVAL_IN_SECONDS), stop=stop_after_attempt(RETRY_ATTEMPTS))
    def scrap_page(self, page_number: int, proxy: str):
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(scrap_site_url.format(page_number), proxies=proxies)

        if response.status_code != 200:
            print(f"error in request: {response.text}")
            raise ValueError(f"error response, {response.status_code}")

        products_info = self.get_scrapped_products(response.content)
        print(f"scrapped {len(products_info)} products, now saving into storage")
        if len(products_info) > 0:
            self.repository.save(products_info)
            message: str = f"Hey, {len(products_info)} product(s) has been added in-stock, do check it out here!"
            self.notification_service.send(RECIPIENTS, message)

    @classmethod
    def get_scrapped_products(cls, content):
        soup = BeautifulSoup(content, "html.parser")
        products = soup.findAll("li", class_="product")

        products_info = list()
        for product in products:
            name = product.select_one(".woo-loop-product__title a").text.strip()
            image_url = product.find("img").get("data-lazy-src")
            price = product.select_one(".mf-product-price-box bdi").text.strip()
            product = Product(name, image_url, price)
            products_info.append(product)
        return products_info


def get_scrapper(repo: ProductRepository = Depends(get_product_repository),
                 ns: NotificationService = Depends(get_notification_service("sms"))) -> ProductScrapper:
    return ProductScrapperImpl(pr=repo, ns=ns)
