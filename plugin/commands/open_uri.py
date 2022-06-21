from ..functions import open_uri_with_browser
from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource
from abc import ABC
from typing import Optional
import sublime


class AbstractOpenUriCommand(AbstractUriCommand, ABC):
    def run(self, _: sublime.Edit, event: Optional[EventDict] = None, browser: str = "") -> None:
        for uri in set(map(self.view.substr, self.get_uri_regions(event))):
            open_uri_with_browser(uri, browser)


class OpenUriFromViewCommand(AbstractOpenUriCommand):
    source = UriSource.FILE


class OpenUriFromCursorsCommand(AbstractOpenUriCommand):
    source = UriSource.CURSORS
