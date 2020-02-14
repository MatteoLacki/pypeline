import inspect


def get_defaults(foo):
    """Get default settings to parameters of a function.

    Arguments:
        foo (function): A function to study.
    Returns:
        dict: mapping argument-default
    """
    s = inspect.signature(foo)
    return {a:v.default for a, v in s.parameters.items() if v.default is not inspect.Parameter.empty}


def test_get_defaults():
    def foo(a, b, c=10, d=23):
        pass
    assert get_defaults(foo) == {'c':10, 'd':23}

    def foo2(a, b, c=10, d=23, *args, **kwds):
        pass
    assert get_defaults(foo2) == {'c':10, 'd':23}