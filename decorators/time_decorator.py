import time
import inspect
import typing
from typing import Callable
from functools import wraps

from playwright.sync_api import Page

from exceptions.not_web_testable_exception import NotWebTestableException

def timeout_decorator(func: Callable) -> Callable:
    sig: inspect.Signature = inspect.signature(func)

    if "page" not in sig.parameters or not issubclass(sig.parameters["page"].annotation, Page):
        raise NotWebTestableException("Decorated method can only take testable Page objects!")

    @wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable:
        page_arg: Page = None

        bound_args = sig.bind(**kwargs)
        if "page" in bound_args.arguments:
            page_arg = bound_args.arguments["page"]

        result = func(*args, **kwargs)
        page_arg.wait_for_timeout(3000)
        return result
    return wrapper


if __name__ == "__main__":
    print("Hello World")

    @timeout_decorator
    def test(page: Page):
        pass