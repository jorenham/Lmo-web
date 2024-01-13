"""
Pythonic interface for interacting with implementations of the Web Storage API.

The values are automatically converted to/from JSON.
"""
__all__ = ('Storage', 'local_storage', 'session_storage')

import json
from collections.abc import Iterator, Mapping, MutableMapping, Sequence
from typing import Final, TypeAlias, TypeVar

from pyscript import window

# https://github.com/python/typing/issues/182#issuecomment-1320974824
JSON: TypeAlias = (
    Mapping[str, 'JSON']
    | Sequence['JSON']
    | str
    | int
    | float
    | bool
    | None
)

V = TypeVar('V', bound=JSON)


class Storage(MutableMapping[str, V]):
    __slots__ = ('_storage', )

    def __init__(self, storage):
        self._storage = storage

    __hash__ = None

    def __len__(self) -> int:
        return self._storage.length

    def __iter__(self) -> Iterator[str]:
        storage = self._storage
        for i in range(storage.length):
            yield storage.key(i)

    def __contains__(self, key: object) -> bool:
        return self._storage.getItem(key) is not None

    def __getitem__(self, key: str) -> V:
        value = self._storage.getItem(key)
        if value is None:
            raise KeyError(key)

        return json.loads(value)

    def __setitem__(self, key: str, value: V) -> None:
        self._storage.setItem(key, json.dumps(value))

    def __delitem__(self, key: str) -> None:
        self._storage.removeItem(key)

    def clear(self) -> None:
        self._storage.clear()


local_storage: Final[Storage] = Storage(window.localStorage)  # type: ignore
session_storage: Final[Storage] = Storage(window.sessionStorage) # type: ignore
