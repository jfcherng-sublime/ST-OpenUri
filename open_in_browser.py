import os, re, sublime, sublime_plugin, webbrowser
from urllib.parse import urlparse

class OpenInBrowser(sublime_plugin.ViewEventListener):
    def clickable_here(url):
        print(url)
        webbrowser.open(url)
        pass
        
    def on_hover(self, point, hover_zone):
        if hover_zone == sublime.HOVER_TEXT:
            print("Id here ", self.view.id())
            print("Point here ", point)
            inspect_reg = self.view.expand_by_class(point, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END, ' ')

            print("Expected piece of text - ", self.view.substr(inspect_reg))
            matched_reg = self.view.find(r"(?<=[\'\"]).+(?=[\'\"])", inspect_reg.begin())
            print ("Matched region begins here ", matched_reg.begin())
            matched_str = self.view.substr(matched_reg)
            print ("Matched String ", matched_str)
            matched_arr = re.split('[\'\"]', matched_str)
            print("Matched array here ", matched_arr)

            temp_int = matched_reg.begin()
            temp_str = url = ''

            if temp_int > point:
                return
            else:
                for word in matched_arr:
                    temp_int += len(word)

                    if temp_int >= point:
                        temp_str = word
                        break

            print("At last temp string ", temp_str)

            urlparse_obj = urlparse(temp_str)

            print("Os result ", os.path.isfile(temp_str))
            if os.path.isfile(temp_str):
                url = 'file://' + temp_str

            if urlparse_obj.scheme and urlparse_obj.netloc:
                url = temp_str

            if not url:
                return

            print("Nah na na na Nah ", url)

            html_var = sublime.expand_variables("<a href='${url}'>Open in Browser</a>", {"url": url})
            self.view.show_popup(html_var, sublime.HIDE_ON_MOUSE_MOVE_AWAY, point, on_navigate=OpenInBrowser.clickable_here)
            print("Oh YEAH!!!")
