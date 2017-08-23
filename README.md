# open_in_browser

[Sublime Text 3](http://www.sublimetext.com/3) plugin to display a link when you hover over a hyperlink or filepath. On click of the link your default browser will open the link or default application for that file extension will open the file.

![open-in-browser-sublime3-plugin](http://i.imgur.com/QZfWsee.gif)

## Installation

This plugin is not yet available on [Package Control](https://packagecontrol.io). Once it's available, I'll update this README file. So, we've to install it manually from git.

### Steps

#### Mac
```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone https://github.com/vicke4/open_in_browser
```

#### Linux
```
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/vicke4/open_in_browser
```

#### Windows
```
cd "%APPDATA%\Sublime Text 3\Packages"
git clone https://github.com/vicke4/open_in_browser
```

## Limitations
- For now, this plugin works only for the 
URLs/filepaths between quotes or whitespaces. In future, this will support all types of URLs & filepaths.

#### Example 1: 
```
<a href='http://github.com'></a>
<img src='http://i.imgur.com/uBzlF64.gif'/>
```

#### Example 2:
```
http://facebook.com
~/Desktop/test_image.jpg
```

## Customization
So, this plugin opens the default browser while you click on links. Yet, We can specify which browser must be used to open links. Navigate to `Preferences -> Package Settings -> Open in Browser -> Settings`. You'll see a similar JSON file.

```
{
	"enable": true,  	       //Set enable to false to disable this plugin
	"custom_browser": "", 	       //Custom browser setting can be used to set a default browser to open links
	"open_with_default_app": true  //To open files with the system default applications set this to true
}
```
You can disable the plugin by setting `enable` to `false`.

You can set default browser by setting value to `custom_browser`.

If `open_with_default_app` is `false`, browser will open the file.

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
