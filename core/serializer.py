from typing import Union

from fastapi.encoders import jsonable_encoder
from poetry.core.json import ValidationError

from core.models import MODEL
from users.models.user import UserModel


class Serializer:
    fields = None
    exclude = None

    def __init__(self, instance: Union[MODEL, list], many=False):
        self.instance = instance
        self.many = many

        # Validate configuration
        if self.fields and self.exclude or not self.fields and not self.exclude:
            raise ValidationError('Either "fields" or "excluded" must be '
                                  'specified, but not both at the same time.')

    @property
    def data(self):
        # Setting kwargs for include and exclude fields
        if self.fields:
            kwargs = dict(include=self.include_fields, exclude=self.exclude_fields)
        else:
            kwargs = dict(exclude=self.exclude)

        # Encode many instances
        if self.many:
            result = []
            for instance in self.instance:
                result.append(jsonable_encoder(instance, **kwargs))
            return result

        # Encode single instance
        return jsonable_encoder(self.instance, **kwargs)

    @property
    def exclude_fields(self) -> set:
        return self.all_fields - self.include_fields

    @property
    def all_fields(self) -> set:
        return set(UserModel.__fields__.keys())

    @property
    def include_fields(self) -> set:
        return set(self.fields or set())
