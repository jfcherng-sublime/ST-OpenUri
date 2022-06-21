from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource
from abc import ABC
from typing import Optional
import sublime


class AbstractSelectUriCommand(AbstractUriCommand, ABC):
    def run(self, _: sublime.Edit, event: Optional[EventDict] = None) -> None:
        if uri_regions := self.get_uri_regions(event):
            sel = self.view.sel()
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(AbstractSelectUriCommand):
    source = UriSource.FILE


class SelectUriFromCursorsCommand(AbstractSelectUriCommand):
    source = UriSource.CURSORS
