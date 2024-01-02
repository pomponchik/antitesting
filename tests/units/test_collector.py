from datetime import date

import pytest

from antitesting.collector import DisabledTestsCollector
from antitesting.specification import Specification
from antitesting.errors import UndefinedTestNameError


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


def test_check_unique_test_names_bad_way():
    disabled_test_names = ['kek', 'cheburek']
    collection = DisabledTestsCollector(disabled_test_names)

    real_tests = [PseudoItem(item_name) for item_name in ('kek', 'mek')]

    with pytest.raises(UndefinedTestNameError, match='There is no test named "cheburek". You specified this name in the skip list.'):
        collection.check_unique_test_names(real_tests)


def test_check_unique_test_names_good_way():
    disabled_test_names = ['kek', 'cheburek']
    collection = DisabledTestsCollector(disabled_test_names)

    real_tests = [PseudoItem(item_name) for item_name in ('kek', 'mek', 'cheburek')]

    collection.check_unique_test_names(real_tests)
