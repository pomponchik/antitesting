from pathlib import Path
from threading import Lock
from datetime import date
from typing import Dict, Union

from pytest import Item

from antitesting.specification import TestSpecification


class DisabledTestsCollector:
    def __init__(self, *args: Union[str, Path, 'DisabledTestsCollector']) -> None:
        self.lock = Lock()
        self.tests: Dict[str, TestSpecification] = {}

        for item in args:
            if isinstance(item, str):
                self.read_file(Path(item))
            elif isinstance(item, Path):
                self.read_file(item)
            elif type(item) is type(self):
                self.cannibalize(item)
            else:
                raise ValueError()

    def __contains__(self, item: Union[str, Item]) -> bool:
        if isinstance(item, str):
            test_specification = self.tests.get(item, None)
        elif isinstance(item, Item):
            test_specification = self.tests.get(item.name, None)

        if test_specification is None:
            return False

        if not test_specification.disabled:
            return False

        return True

    def read_file(self, path: Path) -> None:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                if line:
                    test_specification = self.convert_line_to_specification(line)
                    self.add_test(test_specification)

    def cannibalize(self, other_collector: 'DisabledTestsCollector') -> None:
        for test_specification in other_collector.tests.values():
            self.add_test(test_specification)

    def convert_line_to_specification(self, line: str) -> TestSpecification:
        line = line.strip()

        if ':' in line:
            splitted_line = [chunk for chunk in line.split(':') if chunk]
            if len(splitted_line) != 2:
                raise ValueError()
            name = splitted_line[0]
            date_as_string = splitted_line[1]
            splitted_string_date = [chunk.strip() for chunk in date_as_string.split('.') if chunk.strip()]
            if len(splitted_string_date) != 3:
                raise ValueError()
            if not all(map(lambda x: x.isdigit(), splitted_string_date)):
                raise ValueError()
            date_before_disabled = date(
                day=int(splitted_string_date[0]),
                month=int(splitted_string_date[1]),
                year=int(splitted_string_date[2]),
            )

        else:
            name = line
            date_before_disabled = date.max

        name = name.strip()

        if not name.isidentifier():
            raise ValueError()

        return TestSpecification(name=name, date_before_disabled=date_before_disabled)

    def add_test(self, test_specification: TestSpecification) -> None:
        with self.lock:
            if test_specification.name not in self.tests:
                self.tests[test_specification.name] = test_specification
            else:
                if self.tests[test_specification.name].date_before_disabled is None:
                    self.tests[test_specification.name] = test_specification
