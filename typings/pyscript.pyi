# ruff: noqa: A002, PLW3201
__all__ = (
    'HTML',
    'RUNNING_IN_WORKER',
    'PyWorker',
    'display',
    'document',
    'sync',
    'when',
    'window',
)

from collections.abc import Callable
from typing import IO, Any, Final, Protocol

import js as window
from js import document

# /pyscript/pyscript.core/src/stdlib/pyscript/display.py

class _SupportsRepr(Protocol):
    ...

class _SupportsHTML(Protocol):
    def _repr_html_(self) -> str: ...

class _SupportsMarkdown(Protocol):
    def _repr_markdown_(self) -> str: ...

class _SupportsSVG(Protocol):
    def _repr_svg_(self) -> str: ...

class _SupportsPDF(Protocol):
    def _repr_pdf_(self) -> bytes: ...

class _SupportsJPEG(Protocol):
    def _repr_jpeg_(self) -> bytes: ...

class _SupportsPNG(Protocol):
    def _repr_png_(self) -> bytes: ...

class _SupportsLatex(Protocol):
    def _repr_latex_(self) -> str: ...

class _SupportsJSON(Protocol):
    def _repr_json_(self) -> str: ...

class _SupportsJavascript(Protocol):
    def _repr_javascript_(self) -> str: ...

class _SupportsFig(Protocol):
    def _repr_savefig_(self, __fp: IO[bytes], format: str = ...) -> Any: ...

class _SupportsBundle(Protocol):
    def _repr_mimebundle_(self, __fp: IO[bytes], format: str = ...) -> Any: ...

type _AnyMIME = (
    str
    | _SupportsFig
    | _SupportsHTML
    | _SupportsJavascript
    | _SupportsJPEG
    | _SupportsJSON
    | _SupportsLatex
    | _SupportsMarkdown
    | _SupportsBundle
    | _SupportsPDF
    | _SupportsPNG
    | _SupportsSVG
    | _SupportsRepr
)

class HTML(_SupportsHTML):
    def __init__(self, html: str) -> None: ...

def display(
    *values: _AnyMIME,
    target: str | None = ...,
    append: bool = ...,
) -> None: ...

type _Event = object

# /pyscript/pyscript.core/src/stdlib/pyscript/event_handling.py
type _Listener[_E: _Event] = Callable[[_E], None] | Callable[[], None]

# raises TypeError when called from a worker
def when[_F: _Listener[Any]](
    event_type: str,
    selector: str | None = ...,
) -> Callable[[_F], _F]: ...

# /pyscript/pyscript.core/src/stdlib/pyscript/magic_js.py
RUNNING_IN_WORKER: Final[bool]

# raises TypeError when called from a worker
def PyWorker(  # noqa: N802
    __file: str,
    options: dict[str, str | bool | object] | None = ...,
) -> object: ...

def current_target() -> str | None: ...

js_modules: Final[object]
sync: Final[object]
