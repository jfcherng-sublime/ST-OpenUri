from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource
from abc import ABCMeta
from typing import Iterable, Optional
import sublime


class AbstractCopyUriCommand(AbstractUriCommand, metaclass=ABCMeta):
    def run(
        self,
        edit: sublime.Edit,
        event: Optional[EventDict] = None,
        unique: bool = True,
        sort: bool = True,
    ) -> None:
        if uri_regions := self.get_uri_regions(event):
            uris: Iterable[str] = map(self.view.substr, uri_regions)
            if unique:
                uris = set(uris)
            if sort:
                uris = sorted(uris)
            sublime.set_clipboard("\n".join(uris))


class CopyUriFromViewCommand(AbstractCopyUriCommand):
    source = UriSource.FILE


class CopyUriFromCursorsCommand(AbstractCopyUriCommand):
    source = UriSource.CURSORS


class CopyUriFromContextMenuCommand(AbstractCopyUriCommand):
    source = UriSource.CONTEXT_MENU

    def description(self, event: Optional[EventDict] = None) -> str:  # type: ignore
        return f"Copy {self._find_url(event)}"

    def is_visible(self, event: Optional[EventDict] = None) -> bool:  # type: ignore
        return super().is_visible() and bool(self.get_uri_regions(event))

    def want_event(self) -> bool:
        return True

    def _find_url(self, event: Optional[EventDict] = None) -> str:
        uri_region = next(iter(self.get_uri_regions(event)), None)
        return self.view.substr(uri_region) if uri_region else ""
