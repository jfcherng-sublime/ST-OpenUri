OpenUri has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUri » CHANGELOG

## [7.0.1] - 2021-07-24

- feat: check all foreground views for updating

  Previously, OpenUri only checks the current activated view.
  Since OpenUri also checks whether the view is dirty before perform a update,
  I think this shouldn't be resource consuming.
