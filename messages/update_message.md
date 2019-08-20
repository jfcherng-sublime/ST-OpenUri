OpenUrlInBrowser has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUrlInBrowser » CHANGELOG


## [5.7.0] - 2019-08-20

### Added
Allow using different path regexes for different schemes.

### Changed
- Change `uri_path_regex` to prevent from some HTML problem.
  Escaped HTML entity may be trailing in a URL.
  Disallow `<...>` in URI because it's ambiguous with HTML tags.

### Fixed
- Fix scheme for `mailto:`.
