# ruff: noqa: A002, N801, N802, N803
from collections.abc import Callable, Iterable
from typing import Any, ClassVar, Final, Literal, overload

from pyodide.ffi import (
    JsArray,
    JsDomElement,
    JsException,
    JsFetchResponse,
    JsProxy,
    JsTypedArray,
)
from pyodide.webloop import PyodideFuture

type _CancelToken = int | JsProxy
type _AnyCallback = Callable[[], Any]

# https://github.com/pyodide/pyodide/blob/main/src/py/js.pyi

def setTimeout(cb: _AnyCallback, timeout: float) -> _CancelToken: ...
def clearTimeout(id: _CancelToken) -> None: ...

def setInterval(cb: _AnyCallback, interval: float) -> _CancelToken: ...
def clearInterval(id: _CancelToken) -> None: ...

def fetch(
    url: str,
    options: JsProxy | None = ...,
) -> PyodideFuture[JsFetchResponse]: ...

self: Final[Any] = ...
window: Final[Any] = ...

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
    def new(
        width: int,
        height: int,
        settings: JsProxy | None = ...,
    ) -> ImageData: ...

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

    @overload
    @staticmethod
    def createElement(tagName: Literal['canvas']) -> JsCanvasElement: ...
    @overload
    @staticmethod
    def createElement(tagName: str) -> JsDomElement: ...
    @staticmethod
    def appendChild(child: JsDomElement) -> None: ...

class JsCanvasElement(JsDomElement):
    width: int | float
    height: int | float

    def getContext(
        self,
        ctxType: str,
        *,
        powerPreference: str = ...,
        premultipliedAlpha: bool = ...,
        antialias: bool = ...,
        alpha: bool = ...,
        depth: bool = ...,
        stencil: bool = ...,
    ) -> Any: ...

class ArrayBuffer(_JsObject):
    @staticmethod
    def isView(x: Any) -> bool: ...

class DOMException(JsException): ...

class Map:
    @staticmethod
    def new(a: Iterable[Any]) -> Map: ...

async def sleep(ms: float) -> None: ...
