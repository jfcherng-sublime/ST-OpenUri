import sublime

PLUGIN_NAME = __package__.partition(".")[0]
SETTINGS_FILE_NAME = f"{PLUGIN_NAME}.sublime-settings"

ST_SUPPORT_EXPAND_TO_SCOPE = int(sublime.version()) >= 4132
