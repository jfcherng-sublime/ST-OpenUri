import os, re, sublime, sublime_plugin, webbrowser
from urllib.parse import urlparse

class OpenInBrowser(sublime_plugin.ViewEventListener):
    def open_browser(url):
        webbrowser.open(url)

    def get_url_filepath(string, view):
        urlparse_obj = urlparse(string)

        if urlparse_obj.scheme and urlparse_obj.netloc:
            return string

        if os.path.isfile(string):
            return 'file://' + string
        else:
            filename = view.file_name()
            filepath = os.path.normpath(os.path.join(filename[0:filename.rfind('/')], string))
            return 'file://' + filepath if os.path.isfile(filepath) else None

        return None

    def on_hover(self, point, hover_zone):
        if hover_zone == sublime.HOVER_TEXT:
            inspect_reg = self.view.expand_by_class(point, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, ' ')
            matched_reg = self.view.find(r"(?<=[\'\"]).+(?=[\'\"])", inspect_reg.begin())
            matched_str = self.view.substr(matched_reg)
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
                temp_str = self.view.substr(inspect_reg)

            url = OpenInBrowser.get_url_filepath(temp_str, self.view)

            if not url:
                return

            html_var = sublime.expand_variables("<a href='${url}'>Open in Browser</a>", {"url": url})
            self.view.show_popup(html_var, sublime.HIDE_ON_MOUSE_MOVE_AWAY, point, on_navigate=OpenInBrowser.open_browser)

            return
