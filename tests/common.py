from typing import Any, Callable, Set


def get_method(method_name: str, cls: Any) -> bool:
    return getattr(cls, method_name, None)

def is_abstract(callable: Callable) -> bool:
    return callable.__isabstractmethod__

def arguments(callable: Callable) -> Set:
    return callable.__code__.co_varnames