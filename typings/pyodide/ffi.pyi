# ruff: noqa: N802, N815, N818

__all__ = (
    'IN_BROWSER',
    'ConversionError',
    'JsArray',
    'JsAsyncGenerator',
    'JsAsyncIterable',
    'JsAsyncIterator',
    'JsBuffer',
    'JsCallable',
    'JsDomElement',
    'JsDoubleProxy',
    'JsException',
    'JsFetchResponse',
    'JsGenerator',
    'JsIterable',
    'JsIterator',
    'JsMap',
    'JsMutableMap',
    'JsPromise',
    'JsProxy',
    'JsTypedArray',
    'create_once_callable',
    'create_proxy',
    'destroy_proxies',
    'register_js_module',
    'to_js',
    'unregister_js_module',
)

from collections.abc import (
    AsyncIterator,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)
from types import TracebackType
from typing import (
    IO,
    Any,
    ClassVar,
    Final,
    Protocol,
    Self,
    overload,
    override,
)

type _DictConverter = Callable[[Iterable[JsArray[Any]]], JsProxy] | None
type _DefaultConverter = Callable[
    [
        Any,
        Callable[[Any], JsProxy],
        Callable[[Any, JsProxy], None],
    ],
    JsProxy,
] | None

class _Destroyable(Protocol):
    def destoy(self) -> None: ...

# https://github.com/pyodide/pyodide/blob/main/src/py/_pyodide/_core_docs.py

IN_BROWSER: Final[bool] = ...

class JsProxy:
    _js_type_flags: ClassVar[Any]

    @property
    def js_id(self) -> int: ...
    @property
    def typeof(self) -> str: ...
    def object_entries(self) -> JsArray[JsArray[Any]]: ...
    def object_keys(self) -> JsArray[str]: ...
    def object_values(self) -> JsArray[Any]: ...
    def as_object_map(
        self,
        *,
        hereditary: bool = ...,
    ) -> JsMutableMap[str, Any]: ...
    def new(self, *__args: Any, **__kwargs: Any) -> JsProxy: ...
    def to_py(
        self,
        *,
        depth: int = ...,
        default_converter: _DefaultConverter = ...,
    ) -> Any: ...

class JsDoubleProxy(_Destroyable, JsProxy):
    def unwrap(self) -> Any: ...

type _Handler[V, R] = Callable[[V], Awaitable[R]] | Callable[[V], R]

class JsPromise[T](JsProxy):
    def then[S](
        self,
        onfulfilled: _Handler[T, S] | None,
        onrejected: _Handler[BaseException, S] | None = None,
        /,
    ) -> JsPromise[S]: ...
    def catch[S](
        self,
        onrejected: _Handler[BaseException, S],
        /,
    ) -> JsPromise[S]: ...
    def finally_(self, onfinally: Callable[[], None], /) -> Self: ...

class JsBuffer(JsProxy):
    def assign(self, rhs: Any, /) -> None: ...
    def assign_to(self, to: Any, /) -> None: ...
    def to_memoryview(self) -> memoryview: ...
    def to_bytes(self) -> bytes: ...
    def to_file(self, file: IO[bytes] | IO[str], /) -> None: ...
    def from_file(self, file: IO[bytes] | IO[str], /) -> None: ...
    def _into_file(self, file: IO[bytes] | IO[str], /) -> None: ...
    def to_string(self, encoding: str | None = None) -> str: ...

class JsIterator[T](JsProxy):
    def __next__(self) -> T: ...
    def __iter__(self) -> Iterator[T]: ...

class JsAsyncIterator[T](JsProxy):
    def __anext__(self) -> Awaitable[T]: ...
    def __aiter__(self) -> AsyncIterator[T]: ...

class JsIterable[T](JsProxy):
    def __iter__(self) -> Iterator[T]: ...

class JsAsyncIterable[T](JsProxy):
    def __aiter__(self) -> AsyncIterator[T]: ...

class JsGenerator[T, S, R](JsIterable[T]):
    @override
    def __iter__(self) -> JsGenerator[T, S, R]: ...
    def __next__(self) -> T: ...

    def send(self, value: S) -> T: ...
    @overload
    def throw(
        self,
        typ: type[BaseException],
        val: BaseException | object = ...,
        tb: TracebackType | None = ...,
        /,
    ) -> T: ...
    @overload
    def throw(
        self,
        typ: BaseException,
        val: None = ...,
        tb: TracebackType | None = ...,
        /,
    ) -> T: ...
    def close(self) -> None: ...

class JsFetchResponse(JsProxy):
    bodyUsed: bool
    ok: bool
    redirected: bool
    status: int
    statusText: str
    type: str
    url: str
    headers: Any

    def clone(self) -> JsFetchResponse: ...
    async def arrayBuffer(self) -> JsBuffer: ...
    async def text(self) -> str: ...
    async def json(self) -> JsProxy: ...

class JsAsyncGenerator[T, S, R](JsAsyncIterable[T]):
    @override
    def __aiter__(self) -> JsAsyncGenerator[T, S, R]: ...
    def __anext__(self) -> Awaitable[T]: ...

    def asend(self, value: S, /) -> Awaitable[T]: ...
    @overload
    def athrow(
        self,
        typ: type[BaseException],
        val: BaseException | object = ...,
        tb: TracebackType | None = ...,
        /,
    ) -> Awaitable[T]: ...
    @overload
    def athrow(
        self,
        typ: BaseException,
        val: None = ...,
        tb: TracebackType | None = ...,
        /,
    ) -> Awaitable[T]: ...
    def aclose(self) -> Awaitable[None]: ...

class JsArray[T](JsIterable[T], MutableSequence[T]):
    @overload
    def __getitem__(self, idx: int) -> T: ...
    @overload
    def __getitem__(self, idx: slice) -> JsArray[T]: ...
    def __mul__(self, other: int) -> JsArray[T]: ...
    @override
    def to_py(
        self,
        *,
        depth: int = ...,
        default_converter: _DefaultConverter = ...,
    ) -> list[Any]: ...
    def push(self, value: T) -> None: ...

class JsTypedArray(JsBuffer, JsArray[int]):
    BYTES_PER_ELEMENT: ClassVar[int]
    buffer: JsBuffer

    def subarray(
        self,
        start: int | None = ...,
        stop: int | None = ...,
    ) -> Self: ...

class JsMap[K, V](JsIterable[K], Mapping[K, V]): ...
class JsMutableMap[K, V](JsMap[K, V], MutableMapping[K, V]): ...

class JsCallable(JsProxy):
    def __call__(self) -> Any: ...

class JsOnceCallable(JsCallable, _Destroyable): ...

class JsException(JsProxy, Exception):
    name: str
    message: str
    stack: str

class ConversionError(Exception): ...
class InternalError(Exception): ...

class JsDomElement(JsProxy):
    id: str

    @property
    def tagName(self) -> str: ...
    @property
    def children(self) -> Sequence[JsDomElement]: ...
    @property
    def style(self) -> Any: ...

    def appendChild(self, child: JsDomElement) -> None: ...
    def addEventListener(
        self,
        event: str,
        listener: Callable[[Any], None],
    ) -> None: ...
    def removeEventListener(
        self,
        event: str,
        listener: Callable[[Any], None],
    ) -> None: ...

def create_once_callable(
    obj: Callable[[], Any],
    /,
    *,
    _may_syncify: bool = ...,
) -> JsOnceCallable: ...

def create_proxy(
    obj: Any,
    /,
    *,
    capture_this: bool = ...,
    roundtrip: bool = ...,
) -> JsDoubleProxy: ...

@overload
def to_js[T](
    obj: list[T] | tuple[T, ...],
    /,
    *,
    depth: int = ...,
    pyproxies: JsProxy | None = ...,
    create_pyproxies: bool = ...,
    dict_converter: _DictConverter = ...,
    default_converter: _DefaultConverter = ...,
) -> JsArray[T]: ...
@overload
def to_js[K, V](
    obj: dict[K, V],
    /,
    *,
    depth: int = ...,
    pyproxies: None = ...,
    create_pyproxies: bool = ...,
    dict_converter: _DictConverter = ...,
    default_converter: _DefaultConverter = ...,
) -> JsMap[K, V]: ...
@overload
def to_js(
    obj: Any,
    /,
    *,
    depth: int = ...,
    pyproxies: JsProxy | None = ...,
    create_pyproxies: bool = ...,
    dict_converter: _DictConverter = ...,
    default_converter: _DefaultConverter = ...,
) -> JsProxy: ...

def destroy_proxies(pyproxies: JsArray[Any], /) -> None: ...

# from _pyodide._importhook

def register_js_module(name: str, jsproxy: Any) -> None: ...
def unregister_js_module(name: str) -> None: ...
