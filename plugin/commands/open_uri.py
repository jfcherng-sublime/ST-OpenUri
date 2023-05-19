from __future__ import annotations

from abc import ABC

import sublime

from ..helpers import open_uri_with_browser
from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource


class AbstractOpenUriCommand(AbstractUriCommand, ABC):
    def run(self, _: sublime.Edit, event: EventDict | None = None, browser: str = "") -> None:
        for uri in set(map(self.view.substr, self.get_uri_regions(event))):
            open_uri_with_browser(uri, browser)


class OpenUriFromViewCommand(AbstractOpenUriCommand):
    source = UriSource.FILE


class OpenUriFromCursorsCommand(AbstractOpenUriCommand):
    source = UriSource.CURSORS
