# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [2.0.2] - 2019-07-27

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
