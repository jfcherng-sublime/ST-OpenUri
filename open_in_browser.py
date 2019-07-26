import bisect
import re
import sublime
import sublime_plugin
from .functions import get_setting, get_image_path, open_browser, view_find_all_fast

# our goal is to find URLs ASAP rather than validate them
URL_REGEX = r"(?:https?|ftps?)://[A-Za-z0-9@~_+\-*/&=#%|:.,?]+(?<=[A-Za-z0-9@~_+\-*/&=#%|])"
URL_REGEX_OBJ = re.compile(URL_REGEX, re.IGNORECASE)


class OpenInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view)
        self.url_regions = []

        # the width/height of the phantom image
        self.phantom_img_wh = {
            "w": view.settings().get("font_size", 15) + 2,
            "h": view.settings().get("font_size", 15) + 2,
        }

    def on_load_async(self):
        if get_setting("enable"):
            self._detect_urls()

    def on_activated_async(self):
        if get_setting("enable"):
            self._detect_urls()

    def on_modified_async(self):
        if get_setting("enable"):
            self._detect_urls()

    def on_hover(self, point, hover_zone):
        if not self.url_regions or not get_setting("only_on_hover") or not get_setting("enable"):
            return

        # since "url_regions" is auto sorted, we could perform a binary searching
        insert_idx = bisect.bisect_right(
            self.url_regions,
            sublime.Region(
                point,
                # this ending point is a trick for binary searching
                self.url_regions[-1].end() + 1,
            ),
        )

        # this is the only region which can possibly contain the hovered point
        region_check = self.url_regions[insert_idx - 1]

        self._update_phantom([region_check] if region_check.contains(point) else [])

    def _detect_urls(self):
        self.url_regions = view_find_all_fast(self.view, URL_REGEX_OBJ)

        if get_setting("only_on_hover"):
            return

        self._update_phantom(self.url_regions)

    def _generate_phantom_html(self, url):
        return '<a href="{url}"><img width="{w}" height="{h}" src="res://{src}"></a>'.format(
            url=url, src=get_image_path(), **self.phantom_img_wh
        )

    def _new_url_phantom(self, url_region):
        # if the "url_region" is tuple, list or...
        # always make "url_region" a sublime.Region object
        if not isinstance(url_region, sublime.Region):
            url_region = sublime.Region(*(url_region[0:2]))

        # calulate the point to insert the phantom usually it's exact at the end of URL, but if
        # the next char is a quotation mark, there could be a problem on break  "scope brackets"
        # highlighting in BracketHilighter. In that case, we shift the position until the next char
        # is not a quotation mark.
        phantom_point = url_region.end()
        while self.view.substr(phantom_point) in "'\"":
            phantom_point += 1

        return sublime.Phantom(
            sublime.Region(phantom_point),
            self._generate_phantom_html(self.view.substr(url_region)),
            sublime.LAYOUT_INLINE,
            on_navigate=open_browser,
        )

    def _new_url_phantoms(self, url_regions):
        return [self._new_url_phantom(r) for r in url_regions]

    def _erase_phantom(self):
        self.phantom_set.update([])

    def _update_phantom(self, url_regions):
        self.phantom_set.update(self._new_url_phantoms(url_regions))
