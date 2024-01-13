'''
https://pyodide.org/en/stable/usage/api/python-api/code.html
'''

__all__ = (
    'CodeRunner',
    'eval_code',
    'eval_code_async',
    'find_imports',
    'should_quiet',
    'run_js',
)

import ast
from types import CodeType
from typing import Any, Literal, Self, TypeAlias


# from _pyodide._base

def should_quiet(source: str, /) -> bool: ...

def _last_assign_to_expr(mod: ast.Module) -> None: ...

class EvalCodeResultException(Exception):
    value: Any

    def __init__(self, v: Any) -> None: ...

ReturnMode: TypeAlias = Literal['last_expr', 'last_expr_or_assign', 'none']
_Scope: TypeAlias = dict[str, Any] | None

class CodeRunner:
    ast: ast.Module
    code: CodeType | None

    def __init__(
        self,
        source: str,
        *,
        return_mode: ReturnMode = ...,
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
    return_mode: ReturnMode = ...,
    quiet_trailing_semicolon: bool = ...,
    filename: str = ...,
    flags: int = ...,
) -> Any: ...

async def eval_code_async(
    source: str,
    globals: _Scope = ...,
    locals: _Scope = ...,
    *,
    return_mode: ReturnMode = ...,
    quiet_trailing_semicolon: bool = ...,
    filename: str = ...,
    flags: int = ...,
) -> Any: ...

def find_imports(source: str) -> list[str]: ...


# from pyodide.code

def run_js(code: str, /) -> Any: ...


