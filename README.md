# antitesting: no more testing

[![Downloads](https://static.pepy.tech/badge/antitesting/month)](https://pepy.tech/project/antitesting)
[![Downloads](https://static.pepy.tech/badge/antitesting)](https://pepy.tech/project/antitesting)
[![codecov](https://codecov.io/gh/pomponchik/antitesting/graph/badge.svg?token=jHPEZfRrjC)](https://codecov.io/gh/pomponchik/antitesting)
[![Test-Package](https://github.com/pomponchik/antitesting/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/antitesting/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/antitesting.svg)](https://pypi.python.org/pypi/antitesting)
[![PyPI version](https://badge.fury.io/py/antitesting.svg)](https://badge.fury.io/py/antitesting)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


There are standard ways to temporarily disable individual tests. One of them is [`pytest.mark.skip`](https://docs.pytest.org/en/latest/how-to/skipping.html#skipping-test-functions). However, this plugin extends the standard features of Pytest. Now you can put the names of the disabled tests in a separate file, and then correct and supplement them without going into the source code of the tests.

Install the plugin:

```bash
pip install antitesting
```

Create one or more files containing the names of the tests that you want to disable. In our example, this will be a file `disabled_tests.txt` containing the text like this:

```
test_1
test_2 : 12.12.2012
test_3 : 12.12.2025
```

Finally, add these lines to the file `conftest.py`:

```python
import antitesting

antitesting("disabled_tests.txt")
```

The `disabled_tests.txt` file that we created contains the names of the tests that we want to disable. This is equivalent to putting a  [`skip`](https://docs.pytest.org/en/latest/how-to/skipping.html#skipping-test-functions) decorator on each of them, but it does not require getting into the source code of the tests and saves you time. You could also see the dates in the file in the format `DD.MM.YYYY`. If there is a date in this format in the line with the test name, the test will be ignored only until that date, and after that it will become available.
