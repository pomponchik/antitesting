from typing import Any

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class ItemProtocol(Protocol):
    name: str
