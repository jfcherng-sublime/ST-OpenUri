import base64, sublime

def get_setting(key, default=None):
	settings = sublime.load_settings('OpenInBrowser.sublime-settings')
	return settings.get(key, default)

def get_image():
    return base64.b64encode(sublime.load_binary_resource("Packages/Open In Browser/open-in-browser.png")).decode()
