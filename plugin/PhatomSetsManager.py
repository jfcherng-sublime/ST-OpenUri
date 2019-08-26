import sublime
from collections.abc import Iterable


class PhatomSetsManager:
    # class-level (shared across objects)
    _phantom_sets = {
        # phantom_set_id: sublime.PhantomSet object,
    }

    @classmethod
    def get_phantom_set(cls, phantom_set_id: str) -> sublime.PhantomSet:
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
    def update_phantom_set(cls, phantom_set_id: str, phantoms: Iterable) -> None:
        """
        @brief Note that "phantoms" should be Iterable[sublime.Phantom]
        """

        if phantom_set_id in cls._phantom_sets:
            cls._phantom_sets[phantom_set_id].update(list(phantoms))
