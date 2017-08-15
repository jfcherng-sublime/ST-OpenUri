# open_in_browser

[Sublime Text 3](http://www.sublimetext.com/3) plugin to display popup with a link when you hover over a hyperlink or filepath. On click of the link your default browser will open the link or file.

![open-in-browser-sublime3-plugin](http://i.imgur.com/jyn2ELA.gif)

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

## Known Issues
- On Mac OS Sierra, though the default browser may be Chrome or Safari, If Firefox is installed, it opens the URLs all the time. Haven't tested on other verions of Mac.

## Improvements
- To get rid of the above mentioned issue, we can add a settings file to this package to define the desired browser to open files/URLs. That will be added in future. Feel free to make Pull requests.
