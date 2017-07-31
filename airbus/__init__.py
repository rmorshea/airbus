import six
import types
import inspect
import functools
from contextlib import contextmanager


def merge_mappings(mappings):
    new = {}
    for old in (m for m in mappings if m):
        for k in old:
            if k not in new:
                new[k] = old[k]
    return new


class Private(object):
    
    def __init__(self, value):
        self.value = value
    
    def __get__(self, obj, cls):
        return self.value


class MetaAirbus(type):

    def __init__(cls, name, bases, classdict):
        if "directions" in classdict:
            directions = merge_mappings(
                vars(c).get("directions")
                for c in cls.mro())
            cls.destinations = []
            destination = directions.get(None)
            while destination is not None:
                cls.destinations.append(destination)
                destination = directions.get(destination)


class Airbus(six.with_metaclass(MetaAirbus, object)):

    _index = 0
    directions = {}
    
    @property
    def heading(self):
        if self._index < len(self.destinations):
            return self.destinations[self._index]
        else:
            del self._index

    def __call__(self, *args, **kwargs):
        self._index = 0
        for destination in self.destinations:
            method = getattr(self, destination, None)
            if method is not None:
                result = method(*args, **kwargs)
                if isinstance(result, tuple):
                    args = result
                elif result is not None:
                    args = (result,)
                else:
                    args = ()
                yield result


def between(after, before):
    frame = inspect.currentframe().f_back
    frame.f_locals.setdefault("directions", {})
    directions = frame.f_locals["directions"]

    def setup(method):
        name = method.__name__
        directions[after] = method.__name__
        directions[method.__name__] = before
        return routing(method)

    return setup


def after(name):
    frame = inspect.currentframe().f_back
    frame.f_locals.setdefault("directions", {})
    directions = frame.f_locals["directions"]

    def setup(method):
        directions[name] = method.__name__
        return routing(method)

    return setup


def before(name):
    frame = inspect.currentframe().f_back
    frame.f_locals.setdefault("directions", {})
    directions = frame.f_locals["directions"]

    def setup(method):
        directions[method.__name__] = name
        return routing(method)

    return setup


def run(action, *args, **kwargs):
    result = None
    for _result in action(*args, **kwargs):
        if _result is not None:
            result = _result
    return result


def routing(method):
    bind = method.__get__
    if six.PY3 and inspect.iscoroutinefunction(method):
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            result = await bind(self)(*args, **kwargs)
            self._index += 1
            return result
    else:
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            result = bind(self)(*args, **kwargs)
            self._index += 1
            return result
    return wrapper
