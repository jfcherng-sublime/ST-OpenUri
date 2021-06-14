OpenUri has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUri » CHANGELOG

## [6.4.0] - 2021-06-14

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
