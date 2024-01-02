from pathlib import Path
from threading import Lock
from datetime import date
from typing import Generator, List, Dict, Union

from antitesting.specification import Specification
from antitesting.errors import UndefinedTestNameError
from antitesting.protocols.item import ItemProtocol


class DisabledTestsCollector:
    def __init__(self, *args: Union[str, Path, 'DisabledTestsCollector', List[str]]) -> None:
        self.lock = Lock()
        self.tests: Dict[str, Specification] = {}

        for item in args:
            if isinstance(item, str):
                self.read_file(Path(item))
            elif isinstance(item, Path):
                self.read_file(item)
            elif type(item) is type(self):
                self.cannibalize(item)  # type: ignore[arg-type]
            elif isinstance(item, list):
                self.collect(item)
            else:
                raise ValueError(f'"{item}" ({type(item).__name__}) is not supported as an initialization argument for {type(self).__name__}.')

    def __contains__(self, item: Union[str, ItemProtocol]) -> bool:
        if isinstance(item, str):
            test_specification = self.tests.get(item, None)
        elif isinstance(item, ItemProtocol):
            test_specification = self.tests.get(item.name, None)

        if test_specification is None:
            return False

        if not test_specification.disabled:
            return False

        return True

    def __iter__(self) -> Generator[Specification, None, None]:
        yield from self.tests.values()

    def check_unique_test_names(self, items: List[ItemProtocol]) -> None:
        unique_items_names = {item.name for item in items}

        for collected_test in self:
            if collected_test.name not in unique_items_names:
                raise UndefinedTestNameError(f'There is no test named "{collected_test.name}". You specified this name in the skip list.')

    def collect(self, tests_names: List[str]) -> None:
        for name in tests_names:
            if not isinstance(name, str):
                raise ValueError(f'Only a string can be passed as the name of the test. You passed "{name}" ({type(name).__name__}).')
            if not name.isidentifier():
                raise ValueError(f'Invalid test name: "{name}".')

        for name in tests_names:
            self.add_test(
                Specification(
                    name=name,
                    date_before_disabled=date.max,
                )
            )

    def read_file(self, path: Path) -> None:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = self.normalize_line(line)
                if line:
                    test_specification = self.convert_line_to_specification(line)
                    self.add_test(test_specification)

    def normalize_line(self, line: str) -> str:
        line = self.cut_line(line)
        line = line.strip()
        return line

    def cut_line(self, line: str) -> str:
        splitted_line = line.split('#')
        return splitted_line[0]

    def cannibalize(self, other_collector: 'DisabledTestsCollector') -> None:
        for test_specification in other_collector.tests.values():
            self.add_test(test_specification)

    def convert_line_to_specification(self, line: str) -> Specification:
        line = line.strip()

        if ':' in line:
            splitted_line = [chunk for chunk in line.split(':') if chunk]
            if len(splitted_line) != 2:
                raise ValueError('You can specify either the name of the test, or the name of the test and the date before which it is disabled, in the format {test_name}:{date}.')
            name = splitted_line[0]
            date_as_string = splitted_line[1]
            splitted_string_date = [chunk.strip() for chunk in date_as_string.split('.') if chunk.strip()]

            if len(splitted_string_date) != 3:
                raise ValueError('The date must consist of three numbers in and two dots in the format "DD.MM.YYYY".')
            if not all(map(lambda x: x.isdigit(), splitted_string_date)):
                raise ValueError('The date must consist of three numbers in and two dots in the format "DD.MM.YYYY".')

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
            raise ValueError(f'Invalid test name: "{name}".')

        return Specification(name=name, date_before_disabled=date_before_disabled)

    def add_test(self, test_specification: Specification) -> None:
        with self.lock:
            if test_specification.name not in self.tests:
                self.tests[test_specification.name] = test_specification
            else:
                if self.tests[test_specification.name].date_before_disabled is None:
                    self.tests[test_specification.name] = test_specification
