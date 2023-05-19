from __future__ import annotations

from abc import ABC
from typing import Iterable

import sublime

from ..types import EventDict
from .abstract import AbstractUriCommand, UriSource


class AbstractCopyUriCommand(AbstractUriCommand, ABC):
    def run(
        self,
        _: sublime.Edit,
        event: EventDict | None = None,
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

    def description(self, event: EventDict | None = None) -> str:  # type: ignore
        return f"Copy {self._find_url(event)}"

    def is_visible(self, event: EventDict | None = None) -> bool:  # type: ignore
        return super().is_visible() and bool(self.get_uri_regions(event))

    def want_event(self) -> bool:
        return True

    def _find_url(self, event: EventDict | None = None) -> str:
        uri_region = next(iter(self.get_uri_regions(event)), None)
        return self.view.substr(uri_region) if uri_region else ""
