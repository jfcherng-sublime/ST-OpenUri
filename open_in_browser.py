import base64, os, re, sublime, sublime_plugin, subprocess, webbrowser
from urllib.parse import urlparse
from .settings import get_setting

image_path = os.path.join(os.path.dirname(__file__), 'open-in-browser.png')
ENCODED_IMG = base64.b64encode(open(image_path, 'rb').read()).decode()

class OpenInBrowser(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.platform = sublime.platform()

    def open_app(self, url):
        is_url = url.startswith('http://') or url.startswith('https://')
        browser = get_setting('custom_browser')
        open_with_app = get_setting('open_with_default_app')
        platform = self.platform
        status = 99

        if not browser == "" and (is_url or not open_with_app):
            if platform == 'osx':
                status = os.system("open -a '" + browser + "' " + url)
            elif platform == 'linux':
                try:
                    status = 0
                    subprocess.Popen([browser, url])
                except:
                    status = 99
            elif platform == 'windows':
                status = os.system("start " + browser + " " + url)

        elif not is_url and open_with_app:
            if platform == 'osx':
                status = os.system("open " + url)
            elif platform == 'linux':
                status = os.system("xdg-open " + url)
            elif platform == 'windows':
                status = os.system("start " + url)

        if status > 0:
            webbrowser.open(url)

        self.view.erase_phantoms('open_link_phantom')

    def get_url_filepath(self, string):
        urlparse_obj = urlparse(string)

        if urlparse_obj.scheme and urlparse_obj.netloc:
            return string

        if os.path.isfile(string):
            return 'file://' + string
        else:
            filename = self.view.file_name()
            if self.platform == 'windows':
                rindex = filename.rfind('\\')
            else:
                rindex = filename.rfind('/')

            filepath = os.path.normpath(os.path.join(filename[0:rindex], string))
            return 'file://' + filepath if os.path.isfile(filepath) else None

        return None

    def on_hover(self, point, hover_zone):
        if not get_setting('enable', True):
            return

        view = self.view
        view.erase_phantoms('open_link_phantom')

        if hover_zone == sublime.HOVER_TEXT:
            inspect_reg = view.expand_by_class(point, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, ' ')
            matched_reg = view.find(r"(?<=[\'\"]).+(?=[\'\"])", inspect_reg.begin())
            matched_str = view.substr(matched_reg)
            matched_arr = re.split('[\'\"]', matched_str)

            temp_int = matched_reg.begin()
            temp_str = ''

            if matched_reg.begin() < inspect_reg.end() and matched_reg.begin() != -1:
                if temp_int > point:
                    return
                else:
                    for word in matched_arr:
                        temp_int += len(word)

                        if temp_int >= point:
                            temp_str = word
                            break
            else:
                temp_str = view.substr(inspect_reg)

            url = self.get_url_filepath(temp_str)

            if not url:
                return

            font_size = view.settings().get('font_size', 15) + 3
            html_var = sublime.expand_variables("<a href='${url}'><img width='${font_size}', height='${font_size}' src='data:image/png;base64,${encoded_img}' /></a>", {"url": url, "encoded_img": ENCODED_IMG, 'font_size': str(font_size)})
            view.add_phantom('open_link_phantom', sublime.Region(point, point), html_var, sublime.LAYOUT_INLINE, on_navigate=self.open_app)
            return
