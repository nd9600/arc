import functools


def compose(functions):
    """
        https://mathieularose.com/function-composition-in-python/
        :param functions:
        :return: function
    """

    def compose2(f, g):
        return lambda x: f(g(x))

    return functools.reduce(compose2, functions, lambda x: x)


def compose_packed(*functions):
    return compose(functions)


def double(x): return x * 2


def inc(x): return x + 1


print(compose([inc, double, inc])(1))
