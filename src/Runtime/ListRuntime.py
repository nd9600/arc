from typing import List, TypeVar, Callable

T = TypeVar('T')
S = TypeVar('S')


def copy_element(array: List[T], index) -> List[T]:
    copied_array = array.copy()
    copied_array.append(array[index])
    return copied_array


def delete_element(array: List[T], index) -> List[T]:
    copied_array = array.copy()
    del copied_array[index]
    return copied_array


def append_element(array: List[T], element: T) -> List[T]:
    copied_array = array.copy()
    copied_array.append(element)
    return copied_array


def map_list(f: Callable[[T], S], array: List[T]) -> List[S]:
    return list(map(f, array))


def map_list_partial(f: Callable[[T], S]) -> Callable[[List[T]], List[S]]:
    return lambda array: list(map(f, array))


def filter_list(predicate: Callable[[T], bool], array: List[T]) -> List[T]:
    return list(filter(predicate, array))


def filter_list_partial(predicate: Callable[[T], bool]) -> Callable[[List[T]], List[T]]:
    return lambda array: list(filter(predicate, array))

