from typing import Annotated

from pydantic import StringConstraints

NameStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=128,
    ),
]

PhoneNumberStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=10,
        max_length=20,
    ),
]
