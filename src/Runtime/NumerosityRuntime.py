from typing import List, Callable


def add(a: int, b: int) -> int:
    return a + b


def add_partial(a: int) -> Callable[[int], int]:
    return lambda b: add(a, b)


def subtract(a: int, b: int) -> int:
    return a - b


def subtract_partial(a: int) -> Callable[[int], int]:
    return lambda b: subtract(b, a)


def inc(n: int) -> int:
    return add(n, 1)


def dec(n: int) -> int:
    return subtract(n, 1)


def max_list(numbers: List[int]) -> int:
    return max(numbers)


def min_list(numbers: List[int]) -> int:
    return min(numbers)


def greater_than(a: int, b: int) -> bool:
    return a > b


def greater_than_partial(a: int) -> Callable[[int], bool]:
    return lambda b: greater_than(b, a)


def lesser_than(a: int, b: int) -> bool:
    return a < b


def lesser_than_partial(a: int) -> Callable[[int], bool]:
    return lambda b: lesser_than(b, a)


def equal_to(a: int, b: int) -> bool:
    return a == b


def equal_to_partial(a: int) -> Callable[[int], bool]:
    return lambda b: equal_to(a, b)
