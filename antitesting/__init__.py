import sys

from antitesting.proxy_module import ProxyModule
from antitesting.hook import pytest_collection_modifyitems


sys.modules[__name__].__class__ = ProxyModule
