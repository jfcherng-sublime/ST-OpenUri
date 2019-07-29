# Sublime-OpenUriInBrowser

`OpenUriInBrowser` is a Sublime Text 3 plugin that adds a button (inline phantom in ST's term)
beside a URI. Users can click on the button to open the URI from a browser.

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-OpenUriInBrowser/master/screenshot.png)


## Installation

Currently, this plugin is not on Package Control yet. To install this, you can

- Download the tarball from GitHub and decompress it to `Packages/`.
- Or add a custom Package Control repository (recommended).

  1. `Menu > Preferences > Package Control > Add Repository`:
     https://github.com/jfcherng/Sublime-OpenUriInBrowser
  1. `Menu > Preferences > Package Control > Install Package`: 
     Find `OpenUriInBrowser` and install


## Settings

```javascript
{
    // browser used to open a URI. leave this empty to use a default browser.
    // available values could be found on https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
    "browser": "",
    // get a button beside a URI only on hover?
    "only_on_hover": false,
    // the period (in milisecond) that consecutive modifications are treated as typing
    // phantoms will be updated only when the user is not considered typing
    // you can make this value larger if you feel ST gets stucked while typing
    "on_modified_typing_period": 0,
    // the image used for "open a new window"
    // there are several colors which you may use it by changing the color in the filename
    // "black", "blue", "green", "grey", "orange", "purple", "red", "white", "yellow"
    // if you don't like them, you can even define your own image path.
    "image_new_window": "Packages/${package}/images/new-window-blue.png",
    // defined schemes (case-insensitive) that wants to be detected
    // the protocols and their delimiters are all in regex
    "detect_schemes": {
        "://": [
            // browser viewable
            "ftps?",
            "https?",
            // messengers
            "irc",
            "line",
            "tencent", // Tencent QQ
            "tg", // Telegram
            // version control systems
            "git",
            "hg", // Mercurial
            "svn",
            // P2P file sharing
            "ed2k",
            "freenet",
            // others
            "file",
            "mailto",
            "ssh",
            "telnets?",
            "wss?", // Websocket
        ],
        ":\\?": [
            "magnet", // https://en.wikipedia.org/wiki/Magnet_URI_scheme
        ],
        ":": [
            "skype",
        ],
    },
}
```


## Commands (Keybindings)

- `open_uri_in_browser_from_cursor`: Open URIs in browser from cursors
- `select_uri`: Select URIs from view
- `select_uri_from_cursor`: Select URIs from cursors

There is no default keybindings, but you can define one for opening URIs at
the current cursor(s). For example, I am using the following one.

```javascript
{ 
    "keys": ["alt+o", "alt+i", "alt+b"],
    "command": "open_uri_in_browser_from_cursor",
    // "args": {"browser": ""}, // if you want to force using a specific browser
},
```

`o, i, b` stands for `Open, In, Browser` so I can remember it easily.


## Acknowledgment

This plugin is initially modified from [Open In Browser](https://packagecontrol.io/packages/Open%20In%20Browser).


### Improvements

- Technically a total rewrite.
- Simplified URI-finding REGEX. Allow detecting custom schemes.
- Self-managed phantom set. Do not clear phantoms when a view is deactivated.
- Use binary searching to find URIs which should be opened.
- Allow multiple cursors to open multiple URIs at once via a command (`open_uri_in_browser_from_cursor`).


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
----------

Thank you guys for sending me some cups of coffee.
