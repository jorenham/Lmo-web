"""
Pythonic interface for interacting with implementations of the Web Storage API.

The values are automatically converted to/from JSON.
"""
__all__ = ('Storage', 'local_storage', 'session_storage')

import json
from collections.abc import Iterator, Mapping, MutableMapping, Sequence
from typing import Any, Final, Protocol, override, runtime_checkable

from pyscript import window

# https://github.com/python/typing/issues/182#issuecomment-1320974824
type _JSON = (
    Mapping[str, '_JSON']
    | Sequence['_JSON']
    | str
    | int
    | float
    | bool
    | None
)


@runtime_checkable
class JsStorage(Protocol):
    # https://html.spec.whatwg.org/multipage/webstorage.html#storage-2
    @property
    def length(self) -> int: ...

    def key(self, index: int, /) -> str | None: ...
    def getItem(self, key: str, /) -> str | None: ...  # noqa: N802
    def setItem(self, key: str, value: str, /) -> None: ...  # noqa: N802
    def removeItem(self, key: str, /) -> None: ...  # noqa: N802
    def clear(self, /) -> None: ...


class Storage[V: _JSON](MutableMapping[str, V]):
    __slots__ = ('_storage', )

    _storage: Final[JsStorage]

    def __init__(self, storage: JsStorage, /):
        self._storage = storage

    __hash__ = None

    @override
    def __len__(self) -> int:
        return self._storage.length

    @override
    def __iter__(self) -> Iterator[str]:
        storage = self._storage
        for i in range(storage.length):
            name = storage.key(i)
            assert name is not None
            yield name

    @override
    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return self._storage.getItem(key) is not None

    @override
    def __getitem__(self, key: str) -> V:
        value = self._storage.getItem(key)
        if value is None:
            raise KeyError(key)

        return json.loads(value)

    @override
    def __setitem__(self, key: str, value: V) -> None:
        self._storage.setItem(key, json.dumps(value))

    @override
    def __delitem__(self, key: str) -> None:
        self._storage.removeItem(key)

    @override
    def clear(self) -> None:
        self._storage.clear()


local_storage: Final[Storage[Any]] = Storage(window.localStorage)  # type: ignore  # noqa: PGH003
session_storage: Final[Storage[Any]] = Storage(window.sessionStorage)  # type: ignore  # noqa: PGH003
