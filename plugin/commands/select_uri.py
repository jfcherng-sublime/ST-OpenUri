from __future__ import annotations

from abc import ABC

import sublime

from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource


class AbstractSelectUriCommand(AbstractUriCommand, ABC):
    def run(self, _: sublime.Edit, event: EventDict | None = None) -> None:
        if uri_regions := self.get_uri_regions(event):
            sel = self.view.sel()
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(AbstractSelectUriCommand):
    source = UriSource.FILE


class SelectUriFromCursorsCommand(AbstractSelectUriCommand):
    source = UriSource.CURSORS
