from pydantic import EmailStr, Field

from pydantic_serdes import OneToMany
from pydantic_serdes.models import (PydanticSerdesBaseModel,
                                    PydanticSerdesRenderableModel)


class ProductModel(PydanticSerdesBaseModel):
    _key = ("prod_id",)  # fields that should be used to uniquely ID a model instance
    _directive = "products"  # yaml key that indicates data for instances of this model
    _err_on_duplicate = (
        True  # if data leading to duplicates are present, should we error?
    )

    prod_id: str
    name: str
    category: str


class CustomerModel(PydanticSerdesRenderableModel):
    _key = ("email",)
    _directive = "customers"
    _err_on_duplicate = True

    name: str
    age: int = Field(ge=18, le=100)
    send_ads: bool
    email: EmailStr
    flagged_interests: OneToMany[ProductModel, ...]

    @classmethod
    def create(cls, dict_args, *args, **kwargs):
        interests = list()

        for category in dict_args["flagged_interests"]:
            interests += [prod for prod in ProductModel.filter({"category": category})]

        # even though `interestes` is a list object, pydantic_serdes will
        # take care of ultimately converting this to a OneToMany object.
        dict_args["flagged_interests"] = interests

        super().create(dict_args, *args, **kwargs)
