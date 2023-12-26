from antitesting.state import collector
from antitesting.collector import DisabledTestsCollector


def add_forbidding_file(*args: str) -> None:
    for file_name in args:
        collector.cannibalize(DisabledTestsCollector(file_name))
