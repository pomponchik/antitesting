from typing import List

from pytest import Session, Config, Item, hookimpl

from antitesting.state import collector


@hookimpl  # type: ignore[misc]
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) -> None:
    forbidden_ids = [index for index, item in enumerate(items) if item in collector]
    forbidden_ids.reverse()


    for item_id in forbidden_ids:
        items.pop(item_id)
