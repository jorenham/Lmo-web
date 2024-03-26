__all__ = 'PyodideFuture', 'PyodideTask', 'WebLoop', 'WebLoopPolicy'

import asyncio as _asyncio
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, Self, override

type _Handler[V, R] = Callable[[V], Awaitable[R]] | Callable[[V], R]

class PyodideFuture[T](_asyncio.Future[T]):
    def then[S](
        self,
        onfulfilled: _Handler[T, S] | None,
        onrejected: _Handler[BaseException, S] | None = ...,
        /,
    ) -> PyodideFuture[S]: ...
    def catch[S](
        self,
        onrejected: _Handler[BaseException, S],
        /,
    ) -> PyodideFuture[S]: ...
    def finally_(self, onfinally: Callable[[], None], /) -> Self: ...

class PyodideTask[T](_asyncio.Task[T], PyodideFuture[T]): ...

class WebLoop(_asyncio.AbstractEventLoop):
    @override
    def create_future(self) -> PyodideFuture[Any]: ...
    @override
    def create_task[T](  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        coro: Coroutine[Any, None, T],
        *,
        name: str | None = ...,
    ) -> PyodideTask[T]: ...
    @override
    def run_in_executor[*Ts, R](
        self,
        executor: Any,
        func: Callable[[*Ts], R],
        *args: *Ts,
    ) -> PyodideFuture[R]: ...

class WebLoopPolicy(_asyncio.DefaultEventLoopPolicy):
    @override
    def get_event_loop(self) -> WebLoop: ...
    @override
    def new_event_loop(self) -> WebLoop: ...
