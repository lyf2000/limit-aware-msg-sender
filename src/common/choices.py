from typing import Any, Iterable


Key = Any
Repr = str


class BaseChoices:
    CHOICES: tuple[tuple[Key, Repr]] = ()

    @classmethod
    def dict(cls) -> dict:
        return dict(cls.CHOICES)

    @classmethod
    def keys(cls) -> Iterable[Key]:
        return cls.dict().keys()
