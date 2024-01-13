__all__ = "Console", "PyodideConsole", "BANNER", "repr_shorten", "ConsoleFuture"

from asyncio import Future
from codeop import CommandCompiler, Compile
from collections.abc import Callable, Generator
from contextlib import _RedirectStream, contextmanager
from types import TracebackType
from typing import Any, ClassVar, Final, Literal, TypeAlias

from pyodide.code import CodeRunner, ReturnMode

ConsoleFutureStatus: TypeAlias = Literal["incomplete", "syntax-error", "complete"]

INCOMPLETE: Final[ConsoleFutureStatus] = ...
SYNTAX_ERROR: Final[ConsoleFutureStatus] = ...
COMPLETE: Final[ConsoleFutureStatus] = ...

BANNER: Final[str] = ...

class redirect_stdin(_RedirectStream[Any]):
    _stream: ClassVar[str] = ...

class _WriteStream:
    def __init__(
        self,
        write_handler: Callable[[str], Any],
        name: str | None = ...,
    ) -> None: ...
    def write(self, text: str) -> None: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
class _ReadStream:
    def __init__(
        self,
        read_handler: Callable[[int], str],
        name: str | None = ...,
    ) -> None: ...
    def readline(self, n: int = ...) -> str: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
class _Compile(Compile):
    def __init__(
        self,
        *,
        return_mode: ReturnMode = ...,
        quiet_trailing_semicolon: bool = ...,
        flags: int = ...,
    ) -> None: ...
    def __call__(  # type: ignore
        self,
        source: str,
        filename: str,
        symbol: str,
    ) -> CodeRunner: ...
class _CommandCompiler(CommandCompiler):
    def __init__(
        self,
        *,
        return_mode: ReturnMode = ...,
        quiet_trailing_semicolon: bool = ...,
        flags: int = ...,
    ) -> None: ...
    def __call__(  # type: ignore
        self,
        source: str,
        filename: str = ...,
        symbol: str = ...,
    ) -> CodeRunner | None: ...

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
        globals: dict[str, Any] | None = ...,
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

