# OpenUri Changelog

## 7.1.4

- refactor: for ST >= 4132, utilize `view.expand_to_scope` API

## 7.1.3

- refactor: simplify `boot.py`

## 7.1.2

- fix: modules should be reloaded when update plugin
- fix: RuntimeError: dictionary changed size during iteration
- refactor: tweak directory structure

## 7.1.1

- fix: wrong result if selected region's `.b > .a`
- chore: improve type annotations

## 7.1.0

- feat: add commands to copy URIs
- feat: copy/select URIs from context menu

## 7.0.2

- fix: URI ends with "." in markdown image/link context (#8)

  This fix also introduces a new setting: `expand_uri_regions_selectors`

## 7.0.1

- feat: check all foreground views for updating

  Previously, OpenUri only checks the current activated view.
  Since OpenUri also checks whether the view is dirty before perform a update,
  I think this shouldn't be resource consuming.

## 7.0.0

- refactor: drop ST 3 support
- refactor: default mouse binding has been removed

  If you need the mouse binding, add

  ```js
  [
    // open URL via: alt + right click
    {
      button: 'button2',
      modifiers: ['alt'],
      command: 'open_context_url',
    },
  ]
  ```

## 6.4.1

- refactor: tidy codes

## 6.4.0

Added

- Use strings in setting `draw_uri_regions.flags`

  Previously, it's simply an integer, which is less self-explanatory.
  Now, you can use a list of strings (flag names):

  ```js
  "draw_uri_regions": {
      // the draw flags used, see https://www.sublimetext.com/docs/api_reference.html
      "flags": [
          "HIDE_ON_MINIMAP",
          "DRAW_SOLID_UNDERLINE",
          "DRAW_NO_FILL",
          "DRAW_NO_OUTLINE",
      ],
  },
  ```

Changed

- make `plugin_loaded()` async to speed up ST startup
- make plugin folder structure simpler

Documentation

- Update settings comments for recent ST 4 release

## 6.3.0

Added

- Add setting: `work_for_transient_view`

  This setting controls whether this plugin should work for a transient view
  such as file preview via "Goto Anything".

## 6.2.16

Fixed

- Plugin is not working for transient view. (#5)

## 6.2.15

Fixed

- Replace `open_uri_from_cursors` with `open_context_url` in mousemap.

## 6.2.14

Fixed

- Phantom is not generated when there is `&` in the URI.

## 6.2.13

Fixed

- As of ST 4, remove a phantom position workaround.

## 6.2.12

Fixed

- Prevent from frequently calling `sublime.load_settings()`.

## 6.2.11

Fixed

- Delete phantoms when plugin unloaded.

## 6.2.10

Fixed

- Phantom padding for some color schemes.

  Some color schemes such as Material Theme's have large
  unneeded padding for phantoms somehow.

## 6.2.9

Changed

- Run with Python 3.8 in ST 4.

## 6.2.8

Changed

- `file://` scheme is enabled by default now.
- Update icon `FontAwesome/external-link.svg`.

Fixed

- `file://` scheme is not working for URL-encoded URIs.

## 6.2.7

Changed

- Bound renderer interval with a minimum value.
  So if you accidentally use a tiny value like `0` will not causing ST unresponsive.

## 6.2.6

Added

- Introduce `mypy` for static analysis.

## 6.2.5

Added

- Add and utilize the `typing` module.

Changed

- Make `get_package_name()` not hard-coded.

## 6.2.4

Changed

- The default mouse binding has been changed to `Ctrl + Right Click`.
  Because the `Alt` key seems not working under Linux and I would like to
  provide a binding that hopefully works under all platform.

## 6.2.3

Fixed

- Do not let exceptions terminate the rendering thread.

## 6.2.2

Fixed

- Fix renderer thread crashes when viewing an image file with ST.

## 6.2.1

Changed

- Just some code structure tweaks.

Fixed

- Prevent from weird `phantom_set_id` KeyError.

## 6.2.0

Added

- Add new log level: DEBUG_LOW

Changed

- Render phantoms/regions with another background thread.
- Rename `on_modified_typing_period` to `typing_period`.

Fixed

- Fix and remove workaround for `is_view_too_large()`.

## 6.1.1

Fixed

- Optimize default URI regex for BBCode mismatches.

## 6.1.0

Added

- Allow drawing URI regions on hovering.
- Make text in the hovering popup configurable. (`popup_text_html`)
- Add log to show activated schemes.

Changed

- Allow drawing URI regions even if `show_open_button` is `"never"`.
- Optimize the generated URI-matching regex.
- Change default key binding to `alt+o`, `alt+u`.
- Some minor mathematical optimizations.

## 6.0.0

Changed

- Plugin has been renamed from `OpenUriInBrowser` to `OpenUri`.
- `use_show_open_button_fallback_if_file_larger_than` defaults to `1MB`.

## 5.7.0

Added

- Allow using different path regexes for different schemes.

Changed

- Change `uri_path_regex` to prevent from some HTML problem.
  Escaped HTML entity may be trailing in a URL.
  Disallow `<...>` in URI because it's ambiguous with HTML tags.

Fixed

- Fix scheme for `mailto:`.

## 5.6.0

Added

- Better logging messages with `log_level`.
- Better fitting for light/dark images via inverting gray scale.

Changed

- Auto refresh after saving the settings file to reflect changes.

Fixed

- Fix URL matching regex keeps getting compiled in `find_uri_regions_by_regions()`.

## 5.5.0

Added

- Add new command: `open_uri_from_view`.
- Add default key/mouse bindings.
- Allow setting a different image and color for popup.

Changed

- Hovered behavior now uses popup rather than phantom.
- Image-related user settings have been restructured.
- Command names have been changed.

  - `open_uri_in_browser_from_cursor` -> `open_uri_from_cursors`
  - `select_uri_from_cursor` -> `select_uri_from_cursors`
  - `select_uri` -> `select_uri_from_view`

## 5.4.0

Added

- Add new FontAwesome imagaes: `link`, `share-square`, `star`.
- Add new `image_new_window_color` values: `"@scope"`, `"@scope_inverted"`.
  This will make the phantom be the same color with the corresponding URI.

Changed

- Change default "on_modified_typing_period" to 150.
- Downscaling FontAwesome images to 48x48.

## 5.3.0

Added

- Colored phantom PNG images are now generated in-memory.
  So you are able to use any color for those images.
  See setting `image_new_window_color`.

Changed

- Use icons from FontAwesome.
- Default `uri_path_regex` now matches Unicode URIs.

Fixed

- Fix phantom may break "scope brackets" `` ` `` for BracketHilighter.
- Fix scaling ratio when using non-square images in phantoms.

## 5.2.1

Added

- Add setting `use_show_open_button_fallback_if_file_larger_than`.
- Add setting `show_open_button_fallback`.
- Add new `show_open_button` values: `never`.

Fixed

- `on_hover` now draws URI regions if `draw_uri_regions` is enabled.

## 5.1.2

Fixed

- Fix that I misunderstand how `sublime.Settings.add_on_change()` works.

## 5.1.1

nits

## 5.1.0

Added

- Add config the regex to match URI's path part. (`uri_path_regex`)
- Add new schemes: `mms://` and `sftp://`.

## 5.0.0

Changed

- The settings of `detect_schemes` is now plain text rather than regex.
  This allows the generated regex to be further optimized.

## 4.1.0

Added

- Add the ability to highlight URI regions. (see `draw_uri_regions`)

Changed

- Remove detection for websocket scheme.

## 4.0.5

Changed

- Better phantom looking.

## 4.0.4

Changed

- Change default "on_modified_typing_period" to 150.

## 4.0.3

Fixed

- Fix circular import.

## 4.0.2

Changed

- Cache the "new_window" image content in memory.

## 4.0.1

Changed

- Setting `on_hover` is now changed to `show_open_button`.
  `"on_hover": true` is the same with `"show_open_button": "hover"`.
  `"on_hover": false` is the same with `"show_open_button": "always"`.

## 3.2.3

Fixed

- Fixed old phantoms are not removed after reloading plugin.

## 3.2.2

Added

- Add commands: `select_uri` and `select_uri_from_cursor`.
- Add some menus.

## 3.1.0

Added

- Add config: `on_modified_typing_period`.

## 3.0.3

Changed

- Plugin name has been changed to `OpenUriInBrowser`.
- Command `open_url_in_browser_from_cursor` has been changed to `open_uri_in_browser_from_cursor`.
- All other `URL`-related things have been renamed to `URI` if not mentioned here.

## 2.0.4

Added

- Allow multiple cursors to open multiple URLs at once via a command (`open_url_in_browser_from_cursor`).

Changed

- Technically a total rewrite.
- Simplified URL-finding REGEX.
- Self-managed phantom set. Do not clear phantoms when a view is deactivated.
- Use binary searching to find URLs which should be opened.

## 1.2.7

Added

- User level settings.

## 1.2.6

Changed

- Getting phantom icon from a function.

## 1.2.5

Changed

- Fix to read phantom icon.

## 1.2.4

Changed

- Fix to read phantom icon.

## 1.2.3

Changed

- Fix settings file.

## 1.2.2

Added

- Add image to README.md.

Changed

- Fix settings file.
- Update README.md.

## 1.2.1

Changed

- Remove firefox as default browser.
- Update README.md.

## 1.2.0

Added

- Regex to detect URLs.
- Option to display links permanently or on hover.

Removed

- Support for opening files was removed as the usage is very limited.

## 1.1.1

Added

- Command option to open settings.

Fixed

- Fix for URLs with special characters.

## 1.1.0

Added

- Provision to specify custom browser to open links.
- Option to disable plugin.
- Open files with their default application on system.

Changed

- Popup was replaced by phantom as suggested by @FichteFoll.

## 1.0.0

Added

- "Open in Browser" popup while hovering over links or filepaths surrounded by quotes or whitespaces.
