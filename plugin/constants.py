from __future__ import annotations

import sublime

PLUGIN_NAME = __package__.partition(".")[0]
SETTINGS_FILE_NAME = f"{PLUGIN_NAME}.sublime-settings"

ST_SUPPORT_EXPAND_TO_SCOPE = int(sublime.version()) >= 4132

URI_REGION_KEY = "OUIB_uri_regions"
VIEW_SETTING_TIMESTAMP_KEY = "OUIB_last_update_timestamp"
