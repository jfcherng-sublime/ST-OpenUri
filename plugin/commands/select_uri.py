from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource
from abc import ABCMeta
from typing import Optional
import sublime


class AbstractSelectUriCommand(AbstractUriCommand, metaclass=ABCMeta):
    def run(self, edit: sublime.Edit, event: Optional[EventDict] = None) -> None:
        if uri_regions := self.get_uri_regions(event):
            sel = self.view.sel()
            sel.clear()
            sel.add_all(uri_regions)


class SelectUriFromViewCommand(AbstractSelectUriCommand):
    source = UriSource.FILE


class SelectUriFromCursorsCommand(AbstractSelectUriCommand):
    source = UriSource.CURSORS
