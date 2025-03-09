import os
from typing import List
from contextlib import contextmanager

import pytest

import antitesting


forbidding_file_path = os.path.join('examples', 'forbidding_file.txt')
antitesting(forbidding_file_path)  # type: ignore[operator]


@pytest.fixture
def forbidding_file_changer():
    @contextmanager
    def changer(add_lines: List[str]):
        with open(forbidding_file_path, 'r') as file:
            content_before = file.read()

        with open(forbidding_file_path, 'a') as file:
            for line in add_lines:
                file.write(f'{line}\n')

        yield content_before

        with open(forbidding_file_path, 'w') as file:
            file.write(content_before)

    return changer
