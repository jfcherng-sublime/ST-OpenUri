# open_in_browser

[Sublime Text 3](http://www.sublimetext.com/3) plugin to display a link when you hover over a hyperlink. On click of the link your default browser will open the link (Of course you can customise the behaviour
).

## Installation

You can download this plugin from [Package Control](https://packagecontrol.io). Inside Sublime press `ctrl + shift + p` (Mac users press `cmd + shift + p`). Type install package and press `enter`. Then type `open in browser`. Select the one with spaces. Press `enter`. That's it.

## Customization
So, this plugin opens the default browser while you click on links. Yet, We can specify which browser must be used to open links. Navigate to `Preferences -> Package Settings -> Open in Browser -> Settings`. You'll see a JSON file like the one below.

```
{
    "enable": true,         // Set enable to false to disable this plugin
    "custom_browser": "",   // Set a default browser to open links
    "only_on_hover": false  // Make this true to get links beside URLs only on hover
}
```
You can disable the plugin by setting `enable` to `false`.

You can set the default browser to open links by setting value to `custom_browser` (Refer below).

If `only_on_hover` is `true`, links will be displayed only when you hover over it.

#### Mac
Enter the browser's name as you'd see in Applications window.

Eg: `Google Chrome`, `Firefox`

#### Linux
Here, you've to provide executable name. Mostly, you'll be able to find it in `/usr/bin`

Eg: `google-chrome`, `firefox`

#### Windows
The name with .exe extension. You can find in `C:\Program Files\<app name>\*.exe`

Eg: `chrome`, `firefox`

## Known Issues
- On Mac OS Sierra, though the default browser may be Chrome or Safari, If Firefox is installed, it opens the URLs all the time. We can change this behaviour (Read customization section above).

## Improvements
- More Regex can be added to detect links & file paths. Feel free to make Pull requests.
