from typing import List

from pytest import Session, Config, hookimpl

from antitesting.state import collector
from antitesting.protocols.item import ItemProtocol


@hookimpl
def pytest_collection_modifyitems(session: Session, config: Config, items: List[ItemProtocol]) -> None:
    collector.check_unique_test_names(items)

    forbidden_ids = [index for index, item in enumerate(items) if item in collector]
    forbidden_ids.reverse()

    for item_id in forbidden_ids:
        items.pop(item_id)
