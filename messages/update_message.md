OpenUrlInBrowser has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUrlInBrowser » Changelog

## [2.0.4] - 2019-07-27

### Added
- Allow multiple cursors to open multiple URLs at once via a command (`open_url_in_browser_from_cursor`).

### Changed
- Technically a total rewrite.
- Simplified URL-finding REGEX.
- Self-managed phantom set. Do not clear phantoms when a view is deactivated.
- Use binary searching to find URLs which should be opened.
