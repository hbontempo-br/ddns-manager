from inspect import signature
from typing import Callable


def is_abstract(callable: Callable) -> bool:
    return callable.__isabstractmethod__


def callable_signature(callable: Callable) -> str:
    return str(signature(callable))
