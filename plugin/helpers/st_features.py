import sublime

ST_VERSION = int(sublime.version())

HAS_BH_SCOPED_BRACKETS_BUG = ST_VERSION < 4075
