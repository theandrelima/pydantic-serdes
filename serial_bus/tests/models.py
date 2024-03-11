from typing import Tuple
from pydantic import EmailStr, Field
from serial_bus.models import SerialBusBaseModel, SerialBusRenderableModel


class ProductModel(SerialBusBaseModel):
    _key = ("prod_id",)  # fields that should be used to uniquely ID a model instance
    _directive = "products"  # yaml key that indicates data for instances of this model
    _err_on_duplicate = True  # if data leading to duplicates are present, should we error?

    prod_id: str
    name: str
    category: str


class CustomerModel(SerialBusRenderableModel):
    _key = ("email",)
    _directive = "customers"
    _err_on_duplicate = True

    name: str
    age: int = Field(ge=18, le=100)
    send_ads: bool
    email: EmailStr
    flagged_interests: Tuple[ProductModel, ...]

    @classmethod
    def create(cls, dict_args, *args, **kwargs):
        interests = list()

        for category in dict_args["flagged_interests"]:
            interests += [prod for prod in ProductModel.filter({"category": category})]

        # serial_bus will take care of ultimately converting this to a tuple.
        dict_args["flagged_interests"] = interests

        super().create(dict_args, *args, **kwargs)
