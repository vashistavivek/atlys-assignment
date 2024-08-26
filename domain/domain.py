from abc import ABC, abstractmethod
from typing import Optional, List

from fastapi import BackgroundTasks

from models.user import User

"""
    All abstract classes are defined here
"""


class ProductScrapper(ABC):

    @abstractmethod
    def scrap(self, limit, proxy: Optional[str] = None):
        pass

    @abstractmethod
    def set_background_task(self, background_task: BackgroundTasks):
        pass


class NotificationService(ABC):

    @abstractmethod
    def send(self, recipients: List[str], message: str):
        pass
