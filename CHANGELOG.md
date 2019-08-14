# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [5.4.0] - 2019-08-16

### Added
- Add new FontAwesome imagaes: `link`, `share-square`, `star`.
- Add new `image_new_window_color` values: `"@scope"`, `"@scope_inverted"`.
  This will make the phantom be the same color with the corresponding URI.

### Changed
- Change default "on_modified_typing_period" to 150.
- Downscaling FontAwesome images to 48x48.


## [5.3.0] - 2019-08-13

### Added
- Colored phantom PNG images are now generated in-memory.
  So you are able to use any color for those images.
  See setting `image_new_window_color`.

### Changed
- Use icons from FontAwesome.
- Default `uri_path_regex` now matches Unicode URIs.

### Fixed
- Fix phantom may break "scope brackets" `` ` `` for BracketHilighter.
- Fix scaling ratio when using non-square images in phantoms.


## [5.2.1] - 2019-08-11

### Added
- Add setting `use_show_open_button_fallback_if_file_larger_than`.
- Add setting `show_open_button_fallback`.
- Add new `show_open_button` values: `never`.

### Fixed
- `on_hover` now draws URI regions if `draw_uri_regions` is enabled.


## [5.1.2] - 2019-08-10

### Fixed
- Fix that I misunderstand how `sublime.Settings.add_on_change()` works.


## [5.1.1] - 2019-08-09

nits


## [5.1.0] - 2019-08-07

### Added
- Add config the regex to match URI's path part. (`uri_path_regex`)
- Add new schemes: `mms://` and `sftp://`.


## [5.0.0] - 2019-08-04

### Changed
- The settings of `detect_schemes` is now plain text rather than regex.
  This allows the generated regex to be further optimized.


## [4.1.0] - 2019-08-04

### Added
- Add the ability to highlight URI regions. (see `draw_uri_regions`)

### Changed
- Remove detection for websocket scheme.


## [4.0.5] - 2019-08-03

### Changed
- Better phantom looking.


## [4.0.4] - 2019-08-03

### Changed
- Change default "on_modified_typing_period" to 150.


## [4.0.3] - 2019-08-03

### Fixed
- Fix circular import.


## [4.0.2] - 2019-08-03

### Changed
- Cache the "new_window" image content in memory.


## [4.0.1] - 2019-08-01

### Changed
- Setting `on_hover` is now changed to `show_open_button`.
  `"on_hover": true` is the same with `"show_open_button": "hover"`.
  `"on_hover": false` is the same with `"show_open_button": "always"`.


## [3.2.3] - 2019-07-30

### Fixed
- Fixed old phantoms are not removed after reloading plugin.


## [3.2.2] - 2019-07-29

### Added
- Add commands: `select_uri` and `select_uri_from_cursor`.
- Add some menus.


## [3.1.0] - 2019-07-28

### Added
- Add config: `on_modified_typing_period`.


## [3.0.3] - 2019-07-28

### Changed
- Plugin name has been changed to `OpenUriInBrowser`.
- Command `open_url_in_browser_from_cursor` has been changed to `open_uri_in_browser_from_cursor`.
- All other `URL`-related things have been renamed to `URI` if not mentioned here.


## [2.0.4] - 2019-07-27

### Added
- Allow multiple cursors to open multiple URLs at once via a command (`open_url_in_browser_from_cursor`).

### Changed
- Technically a total rewrite.
- Simplified URL-finding REGEX.
- Self-managed phantom set. Do not clear phantoms when a view is deactivated.
- Use binary searching to find URLs which should be opened.


## [1.2.7] - 2017-11-22

### Added
- User level settings.


## [1.2.6] - 2017-11-18

### Changed
- Getting phantom icon from a function.


## [1.2.5] - 2017-11-14

### Changed
- Fix to read phantom icon.


## [1.2.4] - 2017-11-14

### Changed
- Fix to read phantom icon.


## [1.2.3] - 2017-11-13

### Changed
- Fix settings file.


## [1.2.2] - 2017-11-13

### Added
- Add image to README.md.
### Changed
- Fix settings file.
- Update README.md.


## [1.2.1] - 2017-11-13

### Changed
- Remove firefox as default browser.
- Update README.md.


## [1.2.0] - 2017-11-12

### Added
- Regex to detect URLs.
- Option to display links permanently or on hover.
### Removed
- Support for opening files was removed as the usage is very limited.


## [1.1.1] - 2017-07-26

### Added
- Command option to open settings.
### Fixed
- Fix for URLs with special characters.


## [1.1.0] - 2017-07-23

### Added
- Provision to specify custom browser to open links.
- Option to disable plugin.
- Open files with their default application on system.
### Changed
- Popup was replaced by phantom as suggested by @FichteFoll.


## [1.0.0] - 2017-07-16

### Added
- "Open in Browser" popup while hovering over links or filepaths surrounded by quotes or whitespaces.
