from typing import List

from domain.domain import NotificationService
from models.user import User


class SMSNotificationService(NotificationService):

    def __init__(self):
        self.template = "SMS sent to: {}, \nbody: {}"

    def send(self, recipients: List[str], message: str):
        print(self.template.format(recipients, message))


def get_notification_service(n_type: str):
    def get_service() -> NotificationService:
        if n_type == "sms":
            return SMSNotificationService()
        return NotificationService()
    return get_service
