# ST-OpenUri

[![Required ST Build](https://img.shields.io/badge/ST-4105+-orange.svg?style=flat-square&logo=sublime-text)](https://www.sublimetext.com)
[![GitHub Actions](https://img.shields.io/github/workflow/status/jfcherng-sublime/ST-OpenUri/Python?style=flat-square)](https://github.com/jfcherng-sublime/ST-OpenUri/actions)
[![Package Control](https://img.shields.io/packagecontrol/dt/OpenUri?style=flat-square)](https://packagecontrol.io/packages/OpenUri)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/jfcherng-sublime/ST-OpenUri?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-OpenUri/tags)
[![Project license](https://img.shields.io/github/license/jfcherng-sublime/ST-OpenUri?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-OpenUri/blob/st4/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jfcherng-sublime/ST-OpenUri?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-OpenUri/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

Finally! A performant and highly customizable URI-opening plugin comes.

![screenshot](https://raw.githubusercontent.com/jfcherng-sublime/ST-OpenUri/st4/docs/screenshot.png)

`OpenUri` is a Sublime Text plugin which provides an easy access to URIs (mostly URLs)
in a file by clicking on a phantom, the popup or key/mouse bindings.

## Installation

This plugin is available on [Package Control][package-control] by the name of [OpenUri][openuri].

## Settings

To edit settings, go to `Preferences` » `Package Settings` » `OpenUri` » `Settings`.

I try to make the [settings file](https://github.com/jfcherng-sublime/ST-OpenUri/blob/st4/OpenUri.sublime-settings)
self-explanatory. But if you still have questions, feel free to open an issue.

## Default Bindings

### Key Binding

- <kbd>Alt + o</kbd>, <kbd>Alt + u</kbd>:
  Open URIs from (multiple) cursors. `o, u` is mnemonic for `Open, URI`.

### Mouse Binding

- <kbd>Ctrl + Right Click</kbd>: Open the clicked URI. (`open_context_url`)

### How to disable default bindings

If you do not want those default key/mouse bindings, you can use an empty one to overwrite them.
Or if you want to change them, you can use a non-empty one.

Here I take the default mouse binding as an example.

1. Go to `Preferences` » `Browser Packages...`.
1. Create file `OpenUri/bindings/Default.sublime-mousemap` (and its parent directories if necessary).
1. Fill `Default.sublime-mousemap` with `[]`.
   Then this `Default.sublime-mousemap` will overwrite this plugin's.

## Commands

These commands are always available no matter what `show_open_button` is or how large the file is.

| Command                 | Functionality                     |
| ----------------------- | --------------------------------- |
| open_uri_from_cursors   | Open URIs from cursors            |
| open_uri_from_view      | Open URIs from the current view   |
| select_uri_from_cursors | Select URIs from cursors          |
| select_uri_from_view    | Select URIs from the current view |

[openuri]: https://packagecontrol.io/packages/OpenUri
[package-control]: https://packagecontrol.io
