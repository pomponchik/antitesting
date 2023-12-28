from datetime import date

from pytest import Item, Config

from antitesting.collector import DisabledTestsCollector
from antitesting.specification import Specification


class PseudoItem:
    def __init__(self, name: str):
        self.name = name

def test_iter_by_collection():
    test_names = ['kek', 'cheburek']

    assert list(DisabledTestsCollector(test_names)) == [
        Specification(name=name, date_before_disabled=date.max) for name in test_names
    ]


def test_collection_contains():
    test_names = ['kek', 'cheburek']

    collection = DisabledTestsCollector(test_names)

    assert 'kek' in collection
    assert 'lol' not in collection

    assert PseudoItem('kek') in collection
    assert PseudoItem('lol') not in collection
