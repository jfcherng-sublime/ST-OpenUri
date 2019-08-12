OpenUrlInBrowser has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUrlInBrowser » CHANGELOG


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
