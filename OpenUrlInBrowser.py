import re
import sublime
import sublime_plugin
from .functions import (
    find_url_regions_by_region,
    find_url_regions_by_regions,
    get_image_path,
    get_setting,
    open_url_from_browser,
    view_find_all_fast,
    view_url_regions_val,
)

# our goal is to find URLs ASAP rather than validate them
URL_REGEX = r"\b(?:https?|ftps?)://[A-Za-z0-9@~_+\-*/&=#%|:.,?]+(?<=[A-Za-z0-9@~_+\-*/&=#%|])"
URL_REGEX_OBJ = re.compile(URL_REGEX, re.IGNORECASE)


class OpenUrlInBrowserFromCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit, args={}):
        urls = map(
            lambda region: self.view.substr(sublime.Region(*region)),
            find_url_regions_by_regions(self.view, self.view.sel()),
        )

        for url in set(urls):
            open_url_from_browser(url, args.get("browser", None))


class OpenUrlInBrowser(sublime_plugin.ViewEventListener):
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
        if not get_setting("only_on_hover"):
            return

        self._update_phantom(find_url_regions_by_region(self.view, point))

    def _detect_urls(self):
        url_regions = view_find_all_fast(self.view, URL_REGEX_OBJ)

        # update found URL regions
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
            on_navigate=open_url_from_browser,
        )

    def _new_url_phantoms(self, url_regions):
        return [self._new_url_phantom(r) for r in url_regions]

    def _erase_phantom(self):
        self.phantom_set.update([])

    def _update_phantom(self, url_regions):
        self.phantom_set.update(self._new_url_phantoms(url_regions))
