# Sublime-OpenUriInBrowser

`OpenUriInBrowser` is a Sublime Text 3 plugin that adds a button (inline phantom in ST's term)
beside a URI. Users can click on the button to open the URI from a browser.

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-OpenUriInBrowser/master/screenshot.png)


## Installation

Install using Package Control (recommended), 
or by downloading the tarball from GitHub and decompress it to `Packages/`.


## Settings

```javascript
{
    // browser used to open a URI. leave this empty to use a default browser.
    // available values could be found on https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
    "browser": "",
    // when to show a phantom button beside a URI?
    // can be "always" (always show buttons) or "hover" (only when the URI is hovered)
    "show_open_button": "always",
    // the period (in milisecond) that consecutive modifications are treated as typing
    // phantoms will be updated only when the user is not considered typing
    // you can make this value larger if you feel ST gets stucked while typing
    "on_modified_typing_period": 150,
    // the image used for "open a new window"
    // there are several colors which you may use it by changing the color in the filename
    // "black", "blue", "green", "grey", "orange", "purple", "red", "white", "yellow"
    // if you don't like them, you can even define your own image path.
    "image_new_window": "Packages/${package}/images/new-window-blue.png",
    // draw URI regions?
    "draw_uri_regions": {
        "enabled": false,
        // the scope used to highlight URI regions (you may customize it with your theme)
        "scope": "string",
        // icon in the gutter: "dot", "circle", "bookmark" or empty string for nothing
        "icon": "",
        // @see https://www.sublimetext.com/docs/3/api_reference.html
        //
        // sublime.DRAW_EMPTY = 1
        // sublime.HIDE_ON_MINIMAP = 2
        // sublime.DRAW_EMPTY_AS_OVERWRITE = 4
        // sublime.DRAW_NO_FILL = 32
        // sublime.HIDDEN = 128
        // sublime.DRAW_NO_OUTLINE = 256
        // sublime.DRAW_SOLID_UNDERLINE = 512
        // sublime.DRAW_STIPPLED_UNDERLINE = 1024
        // sublime.DRAW_SQUIGGLY_UNDERLINE = 2048
        //
        // 802 = HIDE_ON_MINIMAP | DRAW_SOLID_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE
        "flags": 802,
    },
    // defined schemes (case-insensitive) that wants to be detected
    // key / value = scheme / enabled
    "detect_schemes": {
        // basic
        "file://": false,
        "ftp://": true,
        "ftps://": true,
        "http://": true,
        "https://": true,
        "mailto://": false,
        // server
        "ssh://": false,
        "telnet://": false,
        "telnets://": false,
        // VCS
        "git://": false,
        "hg://": false,
        "svn://": false,
        // P2P
        "ed2k://": false,
        "freenet://": false,
        "magnet:?": false,
        // messenger
        "irc://": false,
        "line://": false,
        "skype:": false,
        "tencent://": false,
        "tg://": false,
        // streaming
        "rtmp://": false,
        "rtmps://": false,
    },
    // the regex (case-insensitive) used to match a URI's path part
    "uri_path_regex": "[a-z0-9@~_+\\-*/&=#%|:.,!?]+(?<=[a-z0-9@~_+\\-*/&=#%|])",
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
But it has been fully rewritten now.


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
----------

Thank you guys for sending me some cups of coffee.
