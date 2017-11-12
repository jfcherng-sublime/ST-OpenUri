import base64, os, re, sublime, sublime_plugin, subprocess, webbrowser
from urllib.parse import urlparse
from .settings import get_setting

image_path = os.path.join(os.path.dirname(__file__), 'open-in-browser.png')
ENCODED_IMG = base64.b64encode(open(image_path, 'rb').read()).decode()
REGEX = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"

class OpenInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.platform = sublime.platform()
        self.font_size = view.settings().get('font_size', 15) + 3
        self.detected_url_regions = None

    def erase_phantom(self):
        self.view.erase_phantoms('open_link_phantom')

    def get_url_link(self, url):
        return sublime.expand_variables("<a href='${url}'><img width='${font_size}', height='${font_size}' src='data:image/png;base64,${encoded_img}' /></a>", {"url": url, "encoded_img": ENCODED_IMG, 'font_size': str(self.font_size)})

    def on_activated_async(self):
        if get_setting('enable'):
            self.detect_urls()

    def on_deactivated_async(self):
        self.erase_phantom()

    def detect_urls(self):
        url_regions = self.view.find_all(REGEX)
        self.detected_url_regions = url_regions

        for region in url_regions:
            point = region.end()
            detected_url = self.view.substr(region)

            if not get_setting('only_on_hover'):
                pid = self.view.add_phantom('open_link_phantom', sublime.Region(point, point), self.get_url_link(detected_url), sublime.LAYOUT_INLINE, on_navigate=self.open_app)
                print('phantom id here')
                print(pid)

    def open_app(self, url):
        is_url = url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://')
        browser = get_setting('custom_browser')
        platform = self.platform
        status = 99

        if not browser == "":
            if platform == 'osx':
                status = os.system("open -a '{browser}' '{url}'".format(browser=browser, url=url))
            elif platform == 'linux':
                try:
                    status = 0
                    subprocess.Popen([browser, url])
                except:
                    status = 99
            elif platform == 'windows':
                status = os.system("start '{browser}' '{url}'".format(browser=browser, url=url))
        else:
            if platform == 'osx':
                status = os.system("open '{url}'".format(url=url))
            elif platform == 'linux':
                status = os.system("xdg-open '{url}'".format(url=url))
            elif platform == 'windows':
                status = os.system("start '{url}'".format(url=url))

        if status > 0:
            webbrowser.open(url)

    def on_hover(self, point, hover_zone):
        if get_setting('only_on_hover') and get_setting('enable'):
            for region in self.detected_url_regions:
                if region.contains(point):
                    url_end_point = region.end()
                    detected_url = self.view.substr(region)

                    self.erase_phantom()
                    pid = self.view.add_phantom('open_link_phantom', sublime.Region(url_end_point, url_end_point), self.get_url_link(detected_url), sublime.LAYOUT_INLINE, on_navigate=self.open_app)

                    break
                else:
                    self.erase_phantom()

class SaveHelper(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        view.erase_phantoms('open_link_phantom')
        oib = OpenInBrowser(view)
        oib.detect_urls();
