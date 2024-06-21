from pydantic import field_validator
from pydantic_serdes.custom_collections import OneToMany

def onetomany_validators(cls):
    # Iterate over the class's annotations
    for field_name, field_type in cls.__annotations__.items():
        # Check if the field is a OneToMany field
        if getattr(field_type, '__origin__', None) is OneToMany:
            # If it is, add a validator for this field

            # Get the expected type of the elements
            expected_type = field_type.__args__[0]

            # Define the validator function
            def onetomany_validator(cls, v):
                if not all(isinstance(item, expected_type) for item in v):
                    raise TypeError(f'Each item in {field_name} must be a {expected_type.__name__} instance')
                return v

            # Add the validator to the class
            setattr(cls, f'validate_{field_name}', field_validator(field_name)(onetomany_validator))

    return cls