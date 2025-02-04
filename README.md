Durdraw
=======

                  __                __
                _|  |__ __ _____ __|  |_____ _____ __ __ __
               / _  |  |  |   __|  _  |   __|  _  |  |  |  |\
              /_____|_____|__|__|_____|__|___\____|________| | 
              \_____________________________________________\|  v 0.24.1


![durdraw-0 24 0-example](./assets/durdraw-0.24.0-example.gif)

## OVERVIEW

Durdraw is an ASCII, Unicode and ANSI art editor for UNIX-like systems (Linux,
macOS, etc). It runs in modern Utf-8 terminals and supports frame-based
animation, custom themes, 256 and 16 color modes, terminal mouse input, DOS
ANSI art viewing, CP437 and Unicode mixing and conversion, HTML output, mIRC
color output, and other interesting features.

Durdraw is heavily inspired by classic ANSI editing software for MS-DOS and
Windows, such as TheDraw, Aciddraw and Pablodraw, but with a modern Unix twist.

## REQUIREMENTS

* Python 3 (3.10+ recommended)
* Linux, macOS, or other Unix-like System

## INSTALLATION

If you just want to run it without instalilng, scroll down to the next section.

1: Download and extract, or use git to download:

```
   git clone https://github.com/cmang/durdraw.git  
   cd durdraw 
```

2: Install or upgrade using pip:

```
    pip install --upgrade .
```

Or run the installer:

```
   python3 setup.py install
```

3: Optionally, install some themes and a sample configuration file for your local user into ~/.durdraw/:

```
    ./installconf.sh
```


You should now be able to run `durdraw`. This tries to run in 256-color mode by default. To start in 16-color mode for viewing MS-DOS style ANSI art, use `durdraw --16color`.

## RUNNING WITHOUT INSTALLING

You may need to install the "PIL" or "pillow" python module first:

```
    pip3 install pillow
```

Then you can run Durdraw with:

```
    ./start-durdraw
```

To look at some included example animations:

```
    ./start-durdraw -p examples/*.dur
```

To edit 16-color PC Scene (MS-DOS/CP437) ANSI art files in a Utf-8 terminal, use the --16colors option:

```
    ./start-durdraw --16colors
```


## GALLERY


[![Watch the video](https://durdraw.org/durdraw-youtube-thumbnail-with-play-button.png)](https://youtu.be/7Icf08bkJxg)
![durdraw-xmas-example](https://github.com/cmang/durdraw/assets/261501/4137eb2d-0de0-47ca-8789-cca0c8519e91)

![dopetrans3](https://user-images.githubusercontent.com/261501/210064369-4c416e85-12d0-47aa-b182-db5435ae0c78.gif)
![durdraw-screenshot](https://user-images.githubusercontent.com/261501/142838691-9eaf58b0-8a1f-4636-a41a-fe8617937d1d.gif)
![durdraw-linux-unicode-ansi](https://user-images.githubusercontent.com/261501/161380487-ac6e2b5f-d44a-493a-ba78-9903a6a9f1ca.png)
![eye](https://user-images.githubusercontent.com/261501/210064343-6e68f88d-9e3e-415a-9792-a38684231ba0.gif)
![cm-doge](https://user-images.githubusercontent.com/261501/210064365-e9303bee-7842-4068-b356-cd314341098b.gif)
![bsd-color-new](https://user-images.githubusercontent.com/261501/210064354-5c1c2adc-06a3-43c5-8e21-30b1a81db315.gif)

## COMMAND LINE USAGE

You can play a .dur file or series of .dur files with:

```
    $ durdraw -p filename.dur
    $ durdraw -p file1.dur file2.dur file3.dur ...
```

Other command-line options:

<pre>

usage: start-durdraw [-h] [-p PLAY [PLAY ...]] [-q | -w | -x TIMES] [--256color | --16color] [-b]
                     [-W WIDTH] [-H HEIGHT] [-m] [--nomouse] [-A] [-u UNDOSIZE] [-V] [--debug]
                     [filename]

positional arguments:
  filename              .dur or ascii file to load

optional arguments:
  -h, --help            show this help message and exit
  -p PLAY [PLAY ...], --play PLAY [PLAY ...]
                        Just play .dur file or files, then exit
  -q, --quick           Skip startup screen
  -w, --wait            Pause at startup screen
  -x TIMES, --times TIMES
                        Play X number of times (requires -p)
  --256color            Try 256 color mode
  --16color             Try 16 color mode
  -b, --blackbg         Use a black background color instead of terminal default
  -W WIDTH, --width WIDTH
                        Set canvas width
  -H HEIGHT, --height HEIGHT
                        Set canvas height
  -m, --max             Maximum canvas size for terminal (overrides -W and -H)
  --nomouse             Disable mouse support
  --cursor CURSOR       Cursor mode (block, underscore, or pipe)
  --notheme             Disable theme support
  --theme THEME         Load a custom theme file
  --cp437               Encode extended characters using Code Page 437 (IBM-PC/MS-DOS) encoding
                        instead of Utf-8. (Needs CP437 capable terminal and font)
  --export-ansi         Export loaded art to an ANSI file and exit
  -u UNDOSIZE, --undosize UNDOSIZE
                        Set the number of undo history states - default is 100. More requires more
                        RAM, less saves RAM.
  -V, --version         Show version number and exit

</pre>

## INTERACTIVE USAGE/EDITING

Use the arrow keys (or mouse) and other keys to edit, much like a text editor.
You can use the "Esc" (or "Meta") key to access commands:

```
  .. Art Editing .....................   .. About ...........................
  : F1-F10 - insert character        :   : version: {ver}                   :
  : esc-up - next fg color           :   : color mode: {colormode}          :
  : esc-down - prev fg color         :   : character encoding: {charmode}   :
  : esc-right - next bg color (16c)  :   :..................................:
  : esc-left - prev bg color         :
  : esc-/ - insert line              :   .. Animation .......................
  : esc-' - delete line              :   : esc-k - next frame               :
  : esc-. - insert column            :   : esc-j - previous frame           :
  : esc-, - delete column            :   : esc-p - start/stop payback       :
  : esc-] - next character group     :   : esc-n - clone frame              :
  : esc-[ - previous character group :   : esc-N - append empty frame       :
  : esc-S - change character set     :   : esc-d - delete frame             :
  : esc-y - eyedrop (pick up color)  :   : esc-D - set frame delay          :
  : esc-l - color character          :   : esc-+/esc-- - faster/slower      :
  : esc-c - color picker             :   : esc-R - set playback/edit range  :
  : shift-arrows - select for copy   :   : esc-g - go to frame #            :
  : esc-K - mark selection           :   : esc-M - move frame               :
  : esc-v - paste                    :   :..................................:
  :..................................:
                                         .. UI/Misc .........................
  .. File Operations .................   : esc-m - main menu                :
  : esc-C - new/clear canvas         :   : esc-t - mouse tools              :
  : esc-o - open                     :   : esc-z - undo                     :
  : esc-s - save                     :   : esc-r - redo                     :
  :..................................:   : esc-V - view mode                :
                                         : esc-i - file/canvas info         :
  .. Canvas Size .....................   : esc-I - character inspector      :
  : esc-" - insert line              :   : tab - focus canvas or colors     :
  : esc-: - delete line              :   : ctrl-l - redraw screen           :
  : esc-> - insert column            :   : esc-h - help                     :
  : esc-< - delete column            :   : esc-q - quit                     :
  :..................................:   :..................................:
                                                            Prev   Next
                                                            Frame  Frame
                                                            |      |
Main   Frame     Speed     Frame   Play/Edit  Mouse   First | Play |  Last
Menu   Number      |       Delay   Range      Tools   Frame | Pause|  Frame
 |     |           |        |       |          |         |  |  |   |  |
[Menu] F: 1/8    <FPS>: 8   D: 0.00 R: 1/8   [Move]      |< << |> >> >|  
```

## CONFIGURATION

You can create a custom startup file where you can set a theme.


If you did not already do so during installation, you can install a sample configuration and some themes into ~/.durdraw/ with the command:

```
    ./installconf.sh
```

This will place durdraw.ini into ~/.durdraw/ and the themes into ~/.durdraw/themes/.

Here is an example durdraw.ini file:

<pre>
; Durdraw 0.20 Configuration File
[Theme]
theme-16: ~/.durdraw/themes/purpledrank-16.dtheme.ini
theme-256: ~/.durdraw/themes/mutedform-256.dtheme.ini
</pre>

The option 'theme-16' sets the path to the theme file used in 16-color mode, and 'theme-256' sets the theme file used for 256-color mode. 

Note that you can also load a custom theme file using the --theme command-line argument and passing it the path to a theme file, or disable themes entirely with the --notheme command line option.

Here is an example 16-color theme:

<pre>
[Theme-16]
name: 'Purple Drank'
mainColor: 6
clickColor: 3
borderColor: 6
clickHighlightColor: 5
notificationColor: 4
promptColor: 4
</pre>

and a 256-color theme:

<pre>
[Theme-256]
name: 'Muted Form'
mainColor: 104
clickColor: 37
borderColor: 236
clickHighlightColor: 15
notificationColor: 87
promptColor: 189
menuItemColor: 189
menuTitleColor: 159
menuBorderColor: 24
</pre>

The colors and theme options are as follows:

colors for 16-color mode:
1 black
2 blue
3 green
4 cyan
5 red
6 magenta
7 yellow
8 white

color codes numbers for 256-color mode can be found in Durdraw's 256-color selector.

```
mainColor: the color of most text
clickColor: the color of buttons (clickable items)
clickHighlightColor: the color the button changes to for a moment when clicked
borderColor: the color of the border around a drawing
notificationColor: the color of notification messages
promptColor: the color of user prompt messages
menuItemColor: the color of menu items
menuTitleColor: the color of menu titles
menuBorderColor: the color of the border around menus
```


## OTHER TIPS

    * To use themes, copy durdraw.ini to ~/.durdraw/ and edit it. Durdraw
      will also check in the current directory for durdraw.ini.

    * The mouse can be used for moving the cursor (even over SSH) and
      clicking buttons, if your terminal supports Xterm mouse reporting.
      In iTerm2 this is under Profiles, Terminal and Terminal Emulation.

## OPTIONAL INSTALLATION

For PNG and animated GIF export, install Ansilove (https://ansilove.org/) and make sure it is is in your path. PNG and GIF export only work in 16-color mode for now.

## FAQ

#### Q: Don't TheDraw and some other programs already do ANSI animation?
A: Yes, but traditional ANSI animation does not provide any control over timing, instead relying on terminal baud rate to control the speed. This does not work well on modern systems without baud rate emulation. Durdraw gives the artist fine control over frame rate, and delays per frame. Traditional ANSI animation also updates the animation one character at a time, while Durdraw updates the animation a full frame at a time. This makes it less vulnerable to visual corruption from things like errant terminal characters, resized windows, line noise, etc. Finally, unlike TheDraw, which requires MS-DOS, Durdraw runs in modern Unicode terminals.

#### Q: Can I run Durdraw in Windows?
A: Short answer: It's not supported, but it seems to work fine in the Windows Subsystem for Linux (WSL). Long answer: Some versions run fine in Windows Command Prompt, Windows Terminal, etc, without WSL, but it's not tested or supported. If you want to help make Durdraw work better in Windows, please help by testing, submitting bug reports and submitting patches.

#### Q: Can I run Durdraw on Amiga, MS-DOS, Classic MacOS, iOS, Android, etc?
A: Probably not easily. Durdraw requires Python 3 and Ncurses. If your platform can support these, it will probably run. However, the file format for Durdraw movies is a plain text JSON format. It should be possible to support this format in different operating systems and in different applications.

#### Q: Does Durdraw support IBM-PC ANSI art?
A: Yes! IBM-PC ANSI art popular in the "ANSI Art Scene" uses Code Page 437 character encoding, which is not usually compatible with modern terminals. When Durdraw encounters these files, it will convert them toe Unicode and carry on. When you save ANSI files, it will ask if you want to use CP437 or Utf-8 encoding.

### CREDITS

Developer: Sam Foster

Home page: http://durdraw.org

Development: https://github.com/cmang/durdraw

ANSI and ASCII artists: cmang, H7, LDA

### LEGAL

Durdraw is Copyright (c) 2009-2023 Sam Foster <samfoster@gmail.com>. All rights reserved.

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

License for dos437.ttf font:
Copyright (c) 2011 joshua stein <jcs@jcs.org>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

The vga.pcf font was taken from the Dosemu project and appears to be in
the public domain. Further discussion on its copyright status can be found
at http://www.dosemu.org/docs/misc/COPYING.html

