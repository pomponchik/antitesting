from typing import List

from pytest import Session, Config, Item, hookimpl

from antitesting.state import collector
from antitesting.errors import UndefinedTestName


@hookimpl  # type: ignore[misc]
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) -> None:
    unique_items_names = {item.name for item in items}
    for collected_test in collector:
        if collected_test.name not in unique_items_names:
            raise UndefinedTestName(f'There is no test named "{collected_test.name}". You specified this name in the skip list.')

    forbidden_ids = [index for index, item in enumerate(items) if item in collector]
    forbidden_ids.reverse()

    for item_id in forbidden_ids:
        items.pop(item_id)
