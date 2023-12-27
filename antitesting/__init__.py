import sys

from antitesting.proxy_module import ProxyModule


sys.modules[__name__].__class__ = ProxyModule
