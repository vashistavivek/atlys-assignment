class Product:

    def __init__(self, name, image, price):
        self.name = name
        self.image = image
        self.price = price

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self):
        return f"{self.name}, {self.image}, {self.price}"
