import uuid


class User:

    def __init__(self, name: str, email: str):
        self.id = str(uuid.UUID)
        self.name = name
        self.email = email

    def __str__(self):
        return self.id
