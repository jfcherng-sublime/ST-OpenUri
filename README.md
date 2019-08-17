# Sublime-OpenUriInBrowser

![screenshot](https://raw.githubusercontent.com/jfcherng/Sublime-OpenUriInBrowser/master/screenshot.png)

`OpenUriInBrowser` is a Sublime Text 3 plugin that adds a clickable button beside a URI for opening it.


## Installation

This plugin is available on Package Control by the name of [Open URI in Browser](https://packagecontrol.io/packages/Open%20URI%20in%20Browser).

Note that this plugin only supports ST >= 3118 because of Phantom API.

💡 You may also interest in my other plugins: https://packagecontrol.io/search/jfcherng


## Settings

To edit settings, go `Preferences` » `Package Settings` » `OpenUrlInBrowser` » `Settings`.

<details><summary>Click to Show Full Settings</summary>

```javascript
{
    // browser used to open a URI. leave this empty to use a default browser.
    // available values could be found on https://docs.python.org/3.3/library/webbrowser.html#webbrowser.get
    "browser": "",
    // when to show a phantom button beside a URI?
    // values can be
    //     - "always" (always show buttons)
    //     - "hover" (only when the URI is hovered)
    //     - "never" (never show buttons)
    "show_open_button": "always",
    // only useful if "show_open_button" is "always" and the file is too large
    // this setting will be used as the fallback setting of "show_open_button"
    "show_open_button_fallback": "hover",
    // if the file size is larger than the given one and "show_open_button" is "always"
    // use "show_open_button_fallback" as the fallback
    "use_show_open_button_fallback_if_file_larger_than": 800000, // 800K
    // the period (in millisecond) that consecutive modifications are treated as typing
    // phantoms will be updated only when the user is not considered typing
    // you can make this value larger if you feel ST gets stucked while typing
    // or if you consider your machine is powerful, you can set it to a smaller value
    "on_modified_typing_period": 200,
    // the image used for "open a new window" (only supports PNG format)
    // for other plugin-shipped images, visit https://github.com/jfcherng/Sublime-OpenUriInBrowser/tree/master/images
    // if you don't like them, you can even define your own image path.
    "image_new_window": "Packages/${package_name}/images/FontAwesome/external-link-square.png",
    // the color which used to color the whole image
    // values can be
    //     - "" (empty string, use the original color of the image)
    //     - "@scope" (use the same color with the corresponding URI's, require ST >= 3170)
    //     - "@scope_inverted" (use the inverted color of the corresponding URI's, require ST >= 3170)
    //     - ST's scope (use the color of the scope, require ST >= 3170)
    //     - color code in the form of "#RGB", "#RRGGBB" or "#RRGGBBAA"
    "image_new_window_color": "#fa8c00",
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
    // you may add your own new schemes to be detected
    // key / value = scheme / enabled
    "detect_schemes": {
        // basic
        "file://": false,
        "ftp://": true,
        "ftps://": true,
        "http://": true,
        "https://": true,
        "mailto://": true,
        // server
        "sftp://": false,
        "ssh://": false,
        "telnet://": false,
        "telnets://": false,
        "ws://": false,
        "wss://": false,
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
        "mms://": false,
        "rtmp://": false,
        "rtmps://": false,
    },
    // the regex (case-insensitive) used to match a URI's path part
    "uri_path_regex": "(?:[^\\s()\\[\\]{}<>`^*'\"“”‘’]|\\([^\\s)]*\\)|\\[[^\\s\\]]*\\]|\\{[^\\s}]*\\}|<[^\\s>]*>)+(?<![:;.,!?¡¿，。！？])",
    // how many neighbor chars from a cursor will be used to find a URI
    "uri_search_radius": 200,
}
```

</details>


## Bindings


### Key Binding

- <kbd>Alt + o</kbd>, <kbd>Alt + i</kbd>, <kbd>Alt + b</kbd>:
  Open URIs in browser from (multiple) cursors.
  `o, i, b` is mnemonic for `Open, In, Browser`.


### Mouse Binding

- <kbd>Alt + Left Click</kbd>: Open the clicked URI in browser.


## Commands

These commands are always available no matter what `show_open_button` is or how large the file is.

| Command | Functionality |
|---|---|
| open_uri_in_browser_from_cursor | Open URIs in browser from cursors |
| select_uri | Select URIs from view |
| select_uri_from_cursor | Select URIs from cursors |


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
----------

Thank you guys for sending me some cups of coffee.
