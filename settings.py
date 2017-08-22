import sublime

def get_setting(key, default=None):
	settings = sublime.load_settings('OpenInBrowser.sublime-settings')
	return settings.get(key, default)