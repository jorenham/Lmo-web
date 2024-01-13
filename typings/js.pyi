# based on https://github.com/pyodide/pyodide/blob/0.24.1/src/py/js.pyi

from collections.abc import Callable, Iterable
from typing import Any, ClassVar, Final, Literal, TypeAlias

from pyodide.ffi import (
    JsArray,
    JsDomElement,
    JsException,
    JsFetchResponse,
    JsProxy,
    JsTypedArray,
)
from pyodide.webloop import PyodideFuture

# in browser the cancellation token is an int, in node it's a special opaque
# object.
_CancellationToken: TypeAlias = int | JsProxy
_Callback: TypeAlias = Callable[[], Any]

def setTimeout(cb: _Callback, timeout: int | float) -> _CancellationToken: ...
def clearTimeout(id: _CancellationToken) -> None: ...
def setInterval(cb: _Callback, interval: int | float) -> _CancellationToken: ...
def clearInterval(id: _CancellationToken) -> None: ...
def fetch(url: str, options: JsProxy | None = ...) -> PyodideFuture[JsFetchResponse]: ...

self: Final[Any] = ...
window: Final[Any] = ...

# Shenanigans to convince skeptical type system to behave correctly:
#
# These classes we are declaring are actually JavaScript objects, so the class
# objects themselves need to be instances of JsProxy. So their type needs to
# subclass JsProxy. We do this with a custom metaclass.

class _JsMeta(type, JsProxy): ...
class _JsObject(metaclass=_JsMeta): ...

class XMLHttpRequest(_JsObject):
    response: str

    @staticmethod
    def new() -> XMLHttpRequest: ...
    def open(self, method: str, url: str, sync: bool) -> None: ...
    def send(self, body: JsProxy | None = ...) -> None: ...

class Object(_JsObject):
    @staticmethod
    def fromEntries(it: Iterable[JsArray[Any]]) -> JsProxy: ...

class Array(_JsObject):
    @staticmethod
    def new() -> JsArray[Any]: ...

class ImageData(_JsObject):
    width: int
    height: int

    @staticmethod
    def new(width: int, height: int, settings: JsProxy | None = ...) -> ImageData: ...

class _TypedArray(_JsObject):
    @staticmethod
    def new(
        a: int | Iterable[int | float] | JsProxy | None,
        byteOffset: int = ...,
        length: int = ...,
    ) -> JsTypedArray: ...

class Uint8Array(_TypedArray):
    BYTES_PER_ELEMENT: ClassVar[Literal[1]]

class Float64Array(_TypedArray):
    BYTES_PER_ELEMENT: ClassVar[Literal[8]]

class JSON(_JsObject):
    @staticmethod
    def stringify(a: JsProxy) -> str: ...
    @staticmethod
    def parse(a: str) -> JsProxy: ...

class document(_JsObject):
    body: JsDomElement
    children: list[JsDomElement]

    @staticmethod
    def createElement(tagName: str) -> JsDomElement: ...
    @staticmethod
    def appendChild(child: JsDomElement) -> None: ...

class ArrayBuffer(_JsObject):
    @staticmethod
    def isView(x: Any) -> bool: ...

class DOMException(JsException): ...
