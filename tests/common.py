from inspect import formatargspec, getfullargspec
from typing import Any, Callable, Set


def is_abstract(callable: Callable) -> bool:
    return callable.__isabstractmethod__


def arguments(callable: Callable) -> str:
    return formatargspec(*getfullargspec(callable))
