import sublime
from typing import Dict, Iterable, Optional


class PhatomSetsManager:
    # class-level (shared across objects)
    _phantom_sets = {
        # phantom_set_id: PhantomSet object,
    }  # type: Dict[str, sublime.PhantomSet]

    @classmethod
    def get_phantom_set(cls, phantom_set_id: str) -> Optional[sublime.PhantomSet]:
        return cls._phantom_sets.get(phantom_set_id)

    @classmethod
    def init_phantom_set(
        cls, view: sublime.View, phantom_set_id: str, phantom_set_key: str = ""
    ) -> None:
        cls._phantom_sets[phantom_set_id] = sublime.PhantomSet(view, phantom_set_key)

    @classmethod
    def delete_phantom_set(cls, phantom_set_id: str) -> None:
        cls._phantom_sets.pop(phantom_set_id, None)

    @classmethod
    def erase_phantom_set(cls, phantom_set_id: str) -> None:
        if phantom_set_id in cls._phantom_sets:
            cls._phantom_sets[phantom_set_id].update([])

    @classmethod
    def update_phantom_set(cls, phantom_set_id: str, phantoms: Iterable[sublime.Phantom]) -> None:
        if phantom_set_id in cls._phantom_sets:
            cls._phantom_sets[phantom_set_id].update(list(phantoms))

    @classmethod
    def clear(cls) -> None:
        for phantom_set_id in list(cls._phantom_sets.keys()):
            cls.delete_phantom_set(phantom_set_id)

        cls._phantom_sets = {}
