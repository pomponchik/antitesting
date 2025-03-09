from typing import Protocol, runtime_checkable


@runtime_checkable
class ItemProtocol(Protocol):
    name: str
