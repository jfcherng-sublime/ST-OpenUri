OpenUri has been updated. To see the changelog, visit
Preferences » Package Settings » OpenUri » CHANGELOG

## [7.0.0] - 2021-07-23

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
