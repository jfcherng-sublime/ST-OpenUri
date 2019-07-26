import bisect
import re
import sublime
import sublime_plugin
from .functions import (
    find_url_region_by_point,
    get_image_path,
    get_setting,
    open_browser,
    view_find_all_fast,
    view_url_regions_val,
)

# our goal is to find URLs ASAP rather than validate them
URL_REGEX = r"(?:https?|ftps?)://[A-Za-z0-9@~_+\-*/&=#%|:.,?]+(?<=[A-Za-z0-9@~_+\-*/&=#%|])"
URL_REGEX_OBJ = re.compile(URL_REGEX, re.IGNORECASE)


class OpenInBrowserFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit, args={}):
        sels = list(filter(lambda sel: sel.begin() == sel.end(), self.view.sel()))

        if not any(True for _ in sels):
            return

        pts = list(map(lambda sel: sel.begin(), sels))
        url_regions = view_url_regions_val(self.view)
        browser = args.get("browser", None)

        for pt in pts:
            url_region = find_url_region_by_point(url_regions, pt)

            if not url_region:
                continue

            open_browser(self.view.substr(sublime.Region(*url_region)), browser)


class OpenInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view)
        view_url_regions_val(self.view, [])

    def on_load_async(self):
        self._detect_urls()

    def on_activated_async(self):
        self._detect_urls()

    def on_modified_async(self):
        self._detect_urls()

    def on_hover(self, point, hover_zone):
        url_regions = view_url_regions_val(self.view)

        if not url_regions or not get_setting("only_on_hover"):
            return

        region = find_url_region_by_point(url_regions, point)

        self._update_phantom([region] if region else [])

    def _detect_urls(self):
        url_regions = view_find_all_fast(self.view, URL_REGEX_OBJ)

        view_url_regions_val(self.view, url_regions)

        if get_setting("only_on_hover"):
            return

        self._update_phantom(url_regions)

    def _generate_phantom_html(self, url):
        view_font_size = self.view.settings().get("font_size")

        return '<a href="{url}"><img width="{w}" height="{h}" src="res://{src}"></a>'.format(
            url=url, src=get_image_path(), w=view_font_size + 2, h=view_font_size + 2
        )

    def _new_url_phantom(self, url_region):
        # if the "url_region" is tuple, list or...
        # always make "url_region" a sublime.Region object
        if not isinstance(url_region, sublime.Region):
            url_region = sublime.Region(*(url_region[0:2]))

        # calculate the point to insert the phantom usually it's exact at the end of URL, but if
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
