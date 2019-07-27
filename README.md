## Sublime-OpenUrlInBrowser

`OpenUrlInBrowser` is a Sublime Text 3 plugin that adds a button (inline phantom in ST's term)
beside a URL. Users can click on the button to open the URL from a browser.

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-OpenUrlInBrowser/master/screenshot.png)


## Installation

Currently, this plugin is not on Package Control yet. To install this, you can

- Download the tarball from GitHub and decompress it to `Packages/`.
- Or add a custom Package Control repository (recommended).

  1. `Menu > Preferences > Package Control > Add Repository`:
     https://github.com/jfcherng/Sublime-OpenUrlInBrowser
  1. `Menu > Preferences > Package Control > Install Package`: 
     Find `OpenUrlInBrowser` and install


## Settings

```javascript
{
    // browser used to open a URL. leave this empty to use a default browser.
    // available values could be found on https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
    "browser": "",
    // get a button beside a URL only on hover?
    "only_on_hover": false,
    // the image used for "open a new window"
    // there are several colors which you may use it by changing the color in the filename
    // "black", "blue", "green", "grey", "orange", "purple", "red", "white", "yellow"
    // if you don't like them, you can even define your own image path.
    "image_new_window": "Packages/${package}/images/new-window-blue.png",
}
```


## Commands (Keybindings)

There is no default keybindings, but you can define one for opening URLs at
the current cursor(s). For example, I am using the following one.

```javascript
{ 
    "keys": ["alt+o", "alt+i", "alt+b"],
    "command": "open_url_in_browser_from_cursor",
    // "args": {"browser": ""}, // if you want to force using a specific browser
},
```

`o, i, b` stands for `Open, In, Browser` so I can remember it easily.


## Acknowledgment

This plugin is initially modified from [Open In Browser](https://packagecontrol.io/packages/Open%20In%20Browser).


### Improvements

- Technically a total rewrite.
- Simplified URL-finding REGEX.
- Self-managed phantom set. Do not clear phantoms when a view is deactivated.
- Use binary searching to find URLs which should be opened.
- Allow multiple cursors to open multiple URLs at once via a command (`open_url_in_browser_from_cursor`).
