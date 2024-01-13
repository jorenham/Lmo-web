from collections.abc import Iterable, Sequence
from typing import Final, Self, SupportsIndex, TypeAlias, overload

from pyodide.ffi import JsProxy

_Primitive: TypeAlias = str | float | int | bool | None

def alert(message: _Primitive = ...): ...

class BaseElement:
    _js: object
    _parent: BaseElement | None
    _proxies: dict[str, OptionsProxy | StyleProxy]
    style: Final[StyleProxy]

    @property
    def parent(self) -> BaseElement | None: ...

    def __init__(self, js_element: object): ...
    def __eq__(self, obj: object) -> bool: ...
    def create(
        self,
        type_: str,
        *,
        is_child: bool = ...,
        classes: Iterable[str] = ...,
        html: str | None = ...,
        label: str | None = ...,
    ) -> Self: ...
    def find(self, selector: str) -> ElementCollection: ...

class Element(BaseElement):
    @property
    def children(self) -> Sequence[Self]: ...
    @property
    def options(self) -> OptionsProxy: ...
    @property
    def classes(self) -> Sequence[str]: ...
    @property
    def html(self) -> str: ...
    @html.setter
    def html(self, value: str): ...
    @property
    def content(self) -> str: ...
    @content.setter
    def content(self, value: str): ...
    @property
    def id(self) -> str: ...
    @id.setter
    def id(self, value: _Primitive): ...
    @property
    def value(self) -> str | None: ...
    @value.setter
    def value(self, value: _Primitive): ...
    @property
    def selected(self) -> bool: ...
    @selected.setter
    def selected(self, value: bool): ...

    def append(self, child: JsProxy | ElementCollection | Element): ...
    def clone(self, new_id: _Primitive = ...) -> Self: ...
    def remove_class(self, classname: str) -> Self: ...
    def add_class(self, classname: str) -> Self: ...
    def show_me(self) -> None: ...

class OptionsProxy:
    _element: Final[Element]

    @property
    def options(self) -> Sequence[Element]: ...
    @property
    def selected(self) -> Element: ...

    def __init__(self, element: Element) -> None: ...
    @overload
    def __getitem__(self, key: SupportsIndex) -> Element: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[Element]: ...
    def __iter__(self) -> Iterable[Element]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def add(
        self,
        value: object = ...,
        html: str | None = ...,
        text: str | None = ...,
        before: Element | int | None = ...,
        **__kws: object,
    ) -> None: ...
    def remove(self, item: int) -> None: ...
    def clear(self) -> None: ...

class StyleProxy(dict):
    _element: Final[Element]

    @property
    def _style(self) -> str: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool): ...

    def __init__(self, element: Element) -> None: ...
    def __getitem__(self, key: str) -> str: ...
    def __setitem__(self, key: str, value: str): ...
    def remove(self, key: str) -> None: ...
    def set(self, **kws: str) -> None: ...

class StyleCollection:
    def __init__(self, collection: ElementCollection) -> None: ...
    def __get__(
        self,
        obj: ElementCollection,
        objtype: type[ElementCollection] | None = ...,
    ) -> dict[str, str]: ...
    @overload
    def __getitem__(self, key: SupportsIndex) -> str: ...
    @overload
    def __getitem__(self, key: slice) -> Sequence[str]: ...
    def __setitem__(self, key: SupportsIndex, value: str): ...
    def remove(self, key: SupportsIndex) -> None: ...

class ElementCollection:
    _elements: Sequence[Element]
    style: Final[StyleCollection]

    @property
    def html(self) -> str: ...
    @html.setter
    def html(self, value: str): ...
    @property
    def value(self) -> str | None: ...
    @value.setter
    def value(self, value: _Primitive): ...
    @property
    def children(self) -> Sequence[Element]: ...

    def __init__(self, elements: Sequence[Element]) -> None: ...
    @overload
    def __getitem__(self, key: SupportsIndex) -> Element: ...
    @overload
    def __getitem__(self, key: slice | str) -> ElementCollection: ...
    def __len__(self) -> int: ...
    def __eq__(self, obj: object) -> bool: ...
    def __iter__(self) -> Iterable[Element]: ...
    def __repr__(self) -> str: ...
    @overload
    def _get_attribute(
        self,
        attr: str,
        index: slice | None = ...,
    ) -> Sequence[object]: ...
    @overload
    def _get_attribute(self, attr: str, index: SupportsIndex) -> object: ...
    def _set_attribute(self, attr: str, value: object) -> None: ...

class DomScope:
    def __getattr__(self, __name: str) -> object | None: ...

class PyDom(BaseElement):
    BaseElement: Final[type[BaseElement]]
    Element: Final[type[Element]]
    ElementCollection: Final[type[ElementCollection]]

    ids: Final[DomScope]
    body: Final[Element]
    head: Final[Element]

    def __init__(self) -> None: ...
    @overload
    def __getitem__(self, key: int | slice) -> list[Element]: ...
    @overload
    def __getitem__(self, key: str) -> ElementCollection | None: ...
    def create(  # type: ignore
        self,
        type_: str,
        *,
        classes: Iterable[str] | None = ...,
        html: str | None = ...,
    ) -> Self: ...


dom: Final[PyDom]