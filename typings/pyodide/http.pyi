"""
This type stub file was generated by pyright.
"""

from io import StringIO
from typing import Any
from .ffi import IN_BROWSER, JsBuffer, JsFetchResponse

if IN_BROWSER:
    ...
__all__ = ["open_url", "pyfetch", "FetchResponse"]
def open_url(url: str) -> StringIO:
    """Fetches a given URL synchronously.

    The download of binary files is not supported. To download binary
    files use :func:`pyodide.http.pyfetch` which is asynchronous.

    Parameters
    ----------
    url :
       URL to fetch

    Returns
    -------
        The contents of the URL.

    Examples
    --------
    >>> from pyodide.http import open_url
    >>> url = "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/repodata.json"
    >>> url_contents = open_url(url)
    >>> url_contents.read()
    {
      "info": {
          ... # long output truncated
        }
    }
    """
    ...

class FetchResponse:
    """A wrapper for a Javascript fetch :js:data:`Response`.

    Parameters
    ----------
    url
        URL to fetch
    js_response
        A :py:class:`~pyodide.ffi.JsProxy` of the fetch response
    """
    def __init__(self, url: str, js_response: JsFetchResponse) -> None:
        ...
    
    @property
    def body_used(self) -> bool:
        """Has the response been used yet?

        If so, attempting to retrieve the body again will raise an
        :py:exc:`OSError`. Use :py:meth:`~FetchResponse.clone` first to avoid this.
        See :js:attr:`Response.bodyUsed`.
        """
        ...
    
    @property
    def headers(self) -> dict[str, str]:
        """Response headers as dictionary."""
        ...
    
    @property
    def ok(self) -> bool:
        """Was the request successful?

        See :js:attr:`Response.ok`.
        """
        ...
    
    @property
    def redirected(self) -> bool:
        """Was the request redirected?

        See :js:attr:`Response.redirected`.
        """
        ...
    
    @property
    def status(self) -> int:
        """Response status code

        See :js:attr:`Response.status`.
        """
        ...
    
    @property
    def status_text(self) -> str:
        """Response status text

        See :js:attr:`Response.statusText`.
        """
        ...
    
    @property
    def type(self) -> str:
        """The type of the response.

        See :js:attr:`Response.type`.
        """
        ...
    
    @property
    def url(self) -> str:
        """The url of the response.

        The value may be different than the url passed to fetch.
        See :js:attr:`Response.url`.
        """
        ...
    
    def raise_for_status(self) -> None:
        """Raise an :py:exc:`OSError` if the status of the response is an error (4xx or 5xx)"""
        ...
    
    def clone(self) -> FetchResponse:
        """Return an identical copy of the :py:class:`FetchResponse`.

        This method exists to allow multiple uses of :py:class:`FetchResponse`
        objects. See :js:meth:`Response.clone`.
        """
        ...
    
    async def buffer(self) -> JsBuffer:
        """Return the response body as a Javascript :js:class:`ArrayBuffer`.

        See :js:meth:`Response.arrayBuffer`.
        """
        ...
    
    async def text(self) -> str:
        """Return the response body as a string"""
        ...
    
    async def string(self) -> str:
        """Return the response body as a string

        Does the same thing as :py:meth:`FetchResponse.text`.


        .. deprecated:: 0.24.0

            Use :py:meth:`FetchResponse.text` instead.
        """
        ...
    
    async def json(self, **kwargs: Any) -> Any:
        """Treat the response body as a JSON string and use
        :py:func:`json.loads` to parse it into a Python object.

        Any keyword arguments are passed to :py:func:`json.loads`.
        """
        ...
    
    async def memoryview(self) -> memoryview:
        """Return the response body as a :py:class:`memoryview` object"""
        ...
    
    async def bytes(self) -> bytes:
        """Return the response body as a bytes object"""
        ...
    
    async def unpack_archive(self, *, extract_dir: str | None = ..., format: str | None = ...) -> None:
        """Treat the data as an archive and unpack it into target directory.

        Assumes that the file is an archive in a format that :py:mod:`shutil` has
        an unpacker for. The arguments ``extract_dir`` and ``format`` are passed
        directly on to :py:func:`shutil.unpack_archive`.

        Parameters
        ----------
        extract_dir :
            Directory to extract the archive into. If not provided, the current
            working directory is used.

        format :
            The archive format: one of ``"zip"``, ``"tar"``, ``"gztar"``,
            ``"bztar"``. Or any other format registered with
            :py:func:`shutil.register_unpack_format`. If not provided,
            :py:meth:`unpack_archive` will use the archive file name extension and
            see if an unpacker was registered for that extension. In case none
            is found, a :py:exc:`ValueError` is raised.
        """
        ...
    


async def pyfetch(url: str, **kwargs: Any) -> FetchResponse:
    r"""Fetch the url and return the response.

    This functions provides a similar API to :js:func:`fetch` however it is
    designed to be convenient to use from Python. The
    :class:`~pyodide.http.FetchResponse` has methods with the output types
    already converted to Python objects.

    Parameters
    ----------
    url :
        URL to fetch.

    \*\*kwargs :
        keyword arguments are passed along as `optional parameters to the fetch API
        <https://developer.mozilla.org/en-US/docs/Web/API/fetch#options>`_.

    Examples
    --------
    >>> from pyodide.http import pyfetch
    >>> res = await pyfetch("https://cdn.jsdelivr.net/pyodide/v0.23.4/full/repodata.json")
    >>> res.ok
    True
    >>> res.status
    200
    >>> data = await res.json()
    >>> data
    {'info': {'arch': 'wasm32', 'platform': 'emscripten_3_1_32',
    'version': '0.23.4', 'python': '3.11.2'}, ... # long output truncated
    """
    ...
