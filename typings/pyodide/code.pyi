# ruff: noqa: A002

__all__ = (
    'CodeRunner',
    'eval_code',
    'eval_code_async',
    'find_imports',
    'run_js',
    'should_quiet',
)

import ast
from types import CodeType
from typing import Any, Literal, Self

type _ReturnMode = Literal['last_expr', 'last_expr_or_assign', 'none']
type _Scope = dict[str, Any] | None

# https://github.com/pyodide/pyodide/blob/main/src/py/_pyodide/_base.py

def should_quiet(source: str, /) -> bool: ...

def _last_assign_to_expr(mod: ast.Module) -> None: ...

class EvalCodeResultException(Exception):  # noqa: N818
    value: Any
    def __init__(self, v: Any) -> None: ...

class CodeRunner:
    ast: ast.Module
    code: CodeType | None

    def __init__(
        self,
        source: str,
        *,
        return_mode: _ReturnMode = ...,
        mode: str = ...,
        quiet_trailing_semicolon: bool = ...,
        filename: str = ...,
        flags: int = ...,
    ) -> None: ...
    def compile(self) -> Self: ...
    def _set_linecache(self) -> None: ...
    def run(
        self,
        globals: _Scope = ...,
        locals: _Scope = ...,
    ) -> Any | None: ...
    async def run_async(
        self,
        globals: _Scope = ...,
        locals: _Scope = ...,
    ) -> Any | None: ...

def eval_code(
    source: str,
    globals: _Scope = ...,
    locals: _Scope = ...,
    *,
    return_mode: _ReturnMode = ...,
    quiet_trailing_semicolon: bool = ...,
    filename: str = ...,
    flags: int = ...,
) -> Any: ...

async def eval_code_async(
    source: str,
    globals: _Scope = ...,
    locals: _Scope = ...,
    *,
    return_mode: _ReturnMode = ...,
    quiet_trailing_semicolon: bool = ...,
    filename: str = ...,
    flags: int = ...,
) -> Any: ...

def find_imports(source: str) -> list[str]: ...

# https://pyodide.org/en/stable/usage/api/python-api/code.html

def run_js(code: str, /) -> Any: ...
