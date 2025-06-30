import time
import inspect
import typing
from typing import Callable
from functools import wraps

from playwright.sync_api import Page

from exceptions.not_web_testable_exception import NotWebTestableException

def with_timeout(func: Callable) -> Callable:
    sig: inspect.Signature = inspect.signature(func)

    if "page" not in sig.parameters or not issubclass(sig.parameters["page"].annotation, Page):
        raise NotWebTestableException()

    @wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable:
        page_arg: Page | None = None

        bound_args = sig.bind(**kwargs)
        if "page" in bound_args.arguments:
            page_arg = bound_args.arguments["page"]

        result = func(*args, **kwargs)
        page_arg.wait_for_timeout(5000)
        return result
    return wrapper


if __name__ == "__main__":
    @with_timeout
    def test(page: Page):
        pass