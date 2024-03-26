# https://github.com/pyodide/pyodide/blob/main/src/py/pyodide/console.py

__all__ = (
    'BANNER',
    'Console',
    'ConsoleFuture',
    'PyodideConsole',
    'repr_shorten',
)

from asyncio import Future
from collections.abc import Callable, Generator
from contextlib import contextmanager
from types import TracebackType
from typing import Any, Final, Literal, override

from pyodide.code import CodeRunner

type ConsoleFutureStatus = Literal['incomplete', 'syntax-error', 'complete']

INCOMPLETE: Final[ConsoleFutureStatus] = ...
SYNTAX_ERROR: Final[ConsoleFutureStatus] = ...
COMPLETE: Final[ConsoleFutureStatus] = ...

BANNER: Final[str] = ...

class ConsoleFuture(Future[Any]):
    syntax_check: ConsoleFutureStatus
    formatted_error: str | None

    def __init__(self, syntax_check: ConsoleFutureStatus) -> None: ...

class Console:
    globals: dict[str, Any]
    stdin_callback: Callable[[int], str] | None
    stdout_callback: Callable[[str], None] | None
    stderr_callback: Callable[[str], None] | None
    buffer: list[str]
    completer_word_break_characters: str

    def __init__(
        self,
        globals: dict[str, Any] | None = ...,  # noqa: A002
        *,
        stdin_callback: Callable[[int], str] | None = ...,
        stdout_callback: Callable[[str], None] | None = ...,
        stderr_callback: Callable[[str], None] | None = ...,
        persistent_stream_redirection: bool = ..., filename: str = ...,
    ) -> None: ...
    def persistent_redirect_streams(self) -> None: ...
    def persistent_restore_streams(self) -> None: ...
    @contextmanager
    def redirect_streams(self) -> Generator[None, None, None]: ...
    def runsource(self, source: str, filename: str = ...) -> ConsoleFuture: ...
    async def runcode(self, source: str, code: CodeRunner) -> Any: ...
    def formatsyntaxerror(self, e: Exception) -> str: ...
    def num_frames_to_keep(self, tb: TracebackType | None) -> int: ...
    def formattraceback(self, e: BaseException) -> str: ...
    def push(self, line: str) -> ConsoleFuture: ...
    def complete(self, source: str) -> tuple[list[str], int]: ...

class PyodideConsole(Console):
    @override
    async def runcode(
        self,
        source: str,
        code: CodeRunner,
    ) -> ConsoleFuture: ...

def shorten(
    text: str,
    limit: int = ...,
    split: int | None = ...,
    separator: str = ...,
) -> str: ...

def repr_shorten(
    value: Any,
    limit: int = ...,
    split: int | None = ...,
    separator: str = ...,
) -> str: ...
