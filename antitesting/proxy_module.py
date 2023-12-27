import sys

from antitesting.state import collector
from antitesting.collector import DisabledTestsCollector


class ProxyModule(sys.modules[__name__].__class__):  # type: ignore[misc]
    def __call__(self, *args: str) -> None:
        for file_name in args:
            collector.cannibalize(DisabledTestsCollector(file_name))
