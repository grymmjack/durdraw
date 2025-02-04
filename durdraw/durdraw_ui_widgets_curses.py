# Handlers for durdraw_ui_widgets.py classes

import curses
import pdb
import time
import curses.panel

def curses_cursorOff():
    try:
        curses.curs_set(0)  # turn off cursor
    except curses.error:
        pass    # .. if terminal supports it.

def curses_cursorOn():
    try:
        curses.curs_set(1)  # turn on cursor
    except curses.error:
        pass    # .. if terminal supports it.

def curses_notify(screen, message, pause=False):
    #screen.cursorOff()
    #screen.clearStatusLine()
    screen.addstr(0, 0, message)
    screen.refresh()
    if pause:
        if screen.playing:
            screen.nodelay(0) # wait for input when calling getch
            screen.getch()
            screen.nodelay(1) # do not wait for input when calling getch
        else:
            screen.getch()
    if not pause:
        curses.napms(1500)
        curses.flushinp()
    #screen.clearStatusLine()
    #screen.cursorOn()
    screen.refresh()

def curses_addstr(window, y, x, text, attr=None): # addstr(y, x, str[, attr]) and addstr(str[, attr])
    """ Wraps curses addstr in a try;except, prevents addstr from
        crashing cureses if it fails """
    if not attr:
        try:
            window.addstr(y, x, text)
        except curses.error as e:
            curses_notify(window, f"Debug: Curses error in addstr(): {e.args[0]}")
            #self.testWindowSize()
    else:
        try:
            window.addstr(y, x, text, attr)
        except curses.error:
            pass    # silent ugly fail
            #curses_notify(window, f"Debug: Curses error in addstr(): {curses.error}")
            #self.testWindowSize()

class MenuHandler:
    """ hook into Curses to draw menu 
    """
    def __init__(self, menu, window, appState=None, statusBar=None):
        self.menu = menu
        self.window = window
        self.appState=appState
        self.parentWindow = self.menu.caller.window
        self.x = menu.x
        self.y = menu.y
        self.width = None
        self.height = None
        self.title = menu.title # show the title if one is set
        self.menuOriginLine = 0
        #self.rebuild()
        #self.panel = curses.panel.new_panel(self.curses_win)

    def rebuild(self):
        height = len(self.menu.items) + 2  # 2 for top and bottom border lines
        if self.title:
            height += 1
        # find widest item in list, go a few characters larger 
        width = len(max(self.menu.items, key = len)) + 4  + 7 # 4 for padding and side borders, more for shortcuts
        if self.menu.title:
            titleWidth = len(self.menu.title) + 4 
            if titleWidth> width:
                width = titleWidth
        self.width = width
        self.x = self.menu.x - height
        self.curses_win = curses.newwin(height, width, self.x, self.y)
        #self.curses_win.border()
        line = 1
        if self.title:
            line += 1
        textColor = curses.color_pair(self.appState.theme['mainColor']) | curses.A_BOLD
        buttonColor = curses.color_pair(self.appState.theme['clickColor'])
        shortcutColor = curses.color_pair(self.appState.theme['menuBorderColor'])
        borderColor = curses.color_pair(self.appState.theme['menuBorderColor'])
        menuTitleColor = curses.color_pair(self.appState.theme['menuTitleColor']) | curses.A_BOLD | curses.A_UNDERLINE
        maxX, maxY = self.parentWindow.getmaxyx()
        self.menuOriginLine = maxX - 2 - height
        # Draw a pretty border
        curses_addstr(self.curses_win, 0, 0, ".", borderColor)
        curses_addstr(self.curses_win, 0, 1, ("." * (self.width - 2)), borderColor)
        curses_addstr(self.curses_win, 0, width - 1, ".", borderColor)
        if self.title:
            curses_addstr(self.curses_win, 1, 0, ':', borderColor)
            curses_addstr(self.curses_win, 1, 2, self.menu.title, menuTitleColor) # Menu title
            curses_addstr(self.curses_win, 1, width - 1, ':', borderColor)
        for (item, button) in zip(self.menu.items, self.menu.buttons):
            shortcut = self.menu.items[item]["shortcut"]
            has_submenu = self.menu.items[item]["has_submenu"]

            curses_addstr(self.curses_win, line, 0, ':', borderColor)
            curses_addstr(self.curses_win, line, width - 1, ':', borderColor)
            curses_addstr(self.curses_win, line, 2, item, textColor)    # Menu item
            if shortcut:
                curses_addstr(self.curses_win, line, width - 7, shortcut, shortcutColor)
            if has_submenu:
                curses_addstr(self.curses_win, line, width - 2, ">", shortcutColor)
            top_of_menu = self.menu.caller.y - len(self.menu.buttons)
            button.update_real_xy(x=self.menuOriginLine + line, y=self.menu.y) # working for putting menu on first line
            button.window = self.window
            line += 1
        curses_addstr(self.curses_win, line, 0, ':', borderColor)
        curses_addstr(self.curses_win, line,  width - 1, ':', borderColor)
        curses_addstr(self.curses_win, line, 1, ("." * (width - 2)), borderColor)
        self.panel = curses.panel.new_panel(self.curses_win)
        try:
            self.panel.hide()
        except:
            pass

    def show(self):
        self.rebuild()
        self.panel.top()
        #self.panel.move(0,0)
        #self.panel.move(self.menuOriginLine, 0)
        #self.panel.move(self.menuOriginLine, self.menu.x)
        self.panel.move(self.menuOriginLine, self.menu.y)
        self.panel.show()
        self.curses_win.keypad(True)
        curses.panel.update_panels()
        curses.doupdate()
        self.curses_win.refresh()
        # Input loop
        self.window.nodelay(1)
        #self.curses_win.nodelay(0)
        prompting = True
        options = []
        current_option = 0
        for item in self.menu.items:
            options.append(item)
        self.refresh()
        curses_cursorOff()
        #pdb.set_trace()
        #curses.mousemask(1)
        #print('\033[?1003l') # disable mouse reporting
        borderColor = curses.color_pair(self.appState.theme['borderColor'])
        menuItemColor = curses.color_pair(self.appState.theme['menuItemColor'])
        response = "Close"  # default thing to do when done, returned to menu wrapper
        while(prompting):
            time.sleep(0.01)
            line = 1
            if self.title:
                line += 1
            c = self.window.getch()
            for item in self.menu.items:
                if item == options[current_option]: # selected item
                    textColor = menuItemColor | curses.A_REVERSE
                else:
                    textColor = menuItemColor
                curses_addstr(self.curses_win, line, 2, item, textColor)

                hotkeyIndex = 0
                itemString = next(iter(item))
                foundHotkey = False
                for letter in item:
                    if letter.lower() == self.menu.items[item]["hotkey"] and foundHotkey == False:
                        curses_addstr(self.curses_win, line, 2 + hotkeyIndex, letter, textColor | curses.A_UNDERLINE | curses.A_BOLD)
                        foundHotkey = True
                    hotkeyIndex += 1

                line += 1
                curses.panel.update_panels()
                self.window.refresh()
                if c == ord(self.menu.items[item]["hotkey"]):    # hotkey pressed
                    if self.menu.items[item]["has_submenu"]:    # If it opens a sub-menu..
                        # Keep it on the screen.
                        # Redraw previously selected as normal:
                        curses_addstr(self.curses_win, current_option + 1, 2, options[current_option], menuItemColor)
                        # Then highlight the new one.
                        current_option = options.index(item)
                        #self.rebuild()
                        textColor = menuItemColor | curses.A_REVERSE
                        curses_addstr(self.curses_win, line - 1, 2, item, textColor)
                    else:
                        # Otherwise, hide it
                        self.hide()
                    self.menu.items[item]["on_click"]()
                    prompting = False
            if c == curses.KEY_UP:
                current_option = max(0, current_option - 1)
                #pdb.set_trace()
            elif c == curses.KEY_DOWN:
                current_option = min(len(options) - 1, current_option + 1)
            elif c in [13, curses.KEY_ENTER]:    # selected an option
                #pdb.set_trace()
                self.hide()
                prompting = False
                # yikes lol
                self.menu.items[options[current_option]]["on_click"]() 
            elif c in [98, curses.KEY_LEFT]:
                self.hide()
                prompting = False
                response = "Left"
                #self.hide()
                #prompting = False
                # Here: Launch a different menu
                #self.menu.statusBar.menuButton.on_click
            elif c in [102, curses.KEY_RIGHT]:
                if self.menu.items[options[current_option]]["has_submenu"]:    # If it opens a sub-menu..
                    #curses_notify(window, f"Debug: Fnord")
                    #self.hide()
                    #prompting = False
                    self.menu.items[options[current_option]]["on_click"]() 
                    prompting = False
                else:
                    # Jump out of the menu, and tell the parent handler to move to the next menu
                    self.hide()
                    prompting = False
                    response = "Right"
                    #self.hide()
                    #prompting = False
                    # Here: Launch a different menu
            elif c == 27:  # normal esc
                self.hide()
                prompting = False
            elif c == curses.KEY_MOUSE:
                try:
                    _, mouseX, mouseY, _, mouseState = curses.getmouse()
                except:
                    pass

                if not self.appState.hasMouseScroll:
                    curses.BUTTON5_PRESSED = 0
                    curses.BUTTON4_PRESSED = 0 
                if mouseState & curses.BUTTON4_PRESSED:   # wheel up
                    current_option = max(0, current_option - 1)
                elif mouseState & curses.BUTTON5_PRESSED:   # wheel down
                    current_option = min(len(options) - 1, current_option + 1)
                else:   # assume a click
                    # Did the user click in the menu area?
                    if mouseY > self.menuOriginLine and mouseY < self.menuOriginLine + len(self.menu.items):  # on a menu line?
                        if mouseX < self.x and mouseX > self.x - self.width:    # in a menu column
                            # Un-highlight selected item
                            curses_addstr(self.curses_win, current_option + 1, 2, options[current_option], menuItemColor)
                            # Highlight the one we're clicking on
                            current_option = mouseY - self.menuOriginLine - 1
                            #item = self.menu.items[options[current_option]]
                            #curses_notify(self.window, f"current_option: {current_option}")
                            #self.rebuild()
                            textColor = menuItemColor | curses.A_REVERSE
                            curses_addstr(self.curses_win, current_option + 1, 2, options[current_option], textColor)

                            has_submenu = self.menu.items[options[current_option]]["has_submenu"]
                            if has_submenu:
                                prompting = False
                                self.menu.items[options[current_option]]["on_click"]() 
                            else:
                                self.hide()
                                prompting = False
                                #self.menu.items[options[current_option]]["on_click"]() 
                                self.menu.gui.got_click("Click", mouseX, mouseY)
                        else:
                            #curses_notify(self.window, f"Debug: mouseX: {mouseX}, mouseY: {mouseY}, self.x: {self.x}, self.menuOriginLine: {self.menuOriginLine}")
                            prompting = False
                            self.menu.gui.got_click("Click", mouseX, mouseY)
                            self.hide()
                            #curses_notify(self.window, f"This should never happen. mouseX: {mouseX}, mouseY: {mouseY}, self.x: {self.x}, self.menuOriginLine: {self.menuOriginLine}")
                                
                    else:
                        #curses_notify(self.window, f"Debug: mouseX: {mouseX}, mouseY: {mouseY}, self.x: {self.x}, self.menuOriginLine: {self.menuOriginLine}")
                        prompting = False
                        self.menu.gui.got_click("Click", mouseX, mouseY)
                        self.hide()
            #jif c in [104, 63]:  # h H Help
            #    self.hide()
            #    self.items["Help"]["on_click"]()
            #    prompting = False
        #pdb.set_trace()
        curses_cursorOn()
        self.menu.hide()
        if not self.menu.caller.caller.playing:    # lol .. the caller.caller is the main UI thing
            self.window.nodelay(0)
        #pdb.set_trace()
        return response
        #curses_addstr(self.window, self.menu.x, self.menu.y, "Show menu")

    def refresh(self):
        self.window.refresh()
        curses.panel.update_panels()
        #self.window.move(0,0)
        curses.doupdate()

    def hide(self):
        try:
            self.panel.hide()
        except:
            pass 
        self.refresh()
        #curses_addstr(self.window, self.menu.x, self.menu.y, "Hide menu")

class DrawCharPickerHandler:
    def __init__(self, caller, window):
        self.caller = caller    # drawCharPicker
        self.window = window

    def pickChar(self):
        maxLines, maxCol = self.window.getmaxyx()
        #pdb.set_trace()
        self.window.addstr(maxLines - 3, 0, "Enter a character to use for drawing: ")
        prompting = True
        while prompting:
            c = self.window.getch()
            time.sleep(0.01)
            if c in [curses.KEY_F1]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f1'])
                prompting = False
            elif c in [curses.KEY_F2]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f2'])
                prompting = False
            elif c in [curses.KEY_F3]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f3'])
                prompting = False
            elif c in [curses.KEY_F4]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f4'])
                prompting = False
            elif c in [curses.KEY_F5]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f5'])
                prompting = False
            elif c in [curses.KEY_F6]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f6'])
                prompting = False
            elif c in [curses.KEY_F7]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f7'])
                prompting = False
            elif c in [curses.KEY_F8]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f8'])
                prompting = False
            elif c in [curses.KEY_F9]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f9'])
                prompting = False
            elif c in [curses.KEY_F10]:
                self.caller.appState.drawChar = chr(self.caller.caller.caller.chMap['f10'])
                prompting = False
            elif c == 27:   # esc, cancel
                prompting = False
            else:
                self.caller.appState.drawChar = chr(c)
                prompting = False
        #self.caller.caller.drawCharPickerButton.label = self.caller.appState.drawChar
        self.caller.caller.drawCharPickerButton.set_label(self.caller.appState.drawChar)
        self.window.addstr(maxLines - 3, 0, "                                          ")
        self.caller.caller.caller.refresh()

class ColorPickerHandler:
    def __init__(self, colorPicker, window):
        self.colorPicker = colorPicker
        self.parentWindow = window
        self.x = colorPicker.x
        self.y = colorPicker.y
        self.parentWindow = colorPicker.caller.stdscr
        self.appState = colorPicker.caller.appState
        # figure out picker size
        #total = curses.COLORS
        #total = curses.COLORS
        realmaxY,realmaxX = self.parentWindow.getmaxyx()
        self.realmaxY = realmaxY
        self.realmaxX = realmaxX
        #self.height = int(total / realmaxX) + 2 # enough lines to fill content+
        #self.height = 4
        self.height = 8
        #height = int(total / realmaxY) # enough lines to fill content+
        #self.width = realmaxX - 10 
        #self.width = 78
        #self.width = 38 
        self.width = 38 
        #gridLine = [[]] * self.width
        #self.colorGrid = [gridLine] * self.height
        #self.colorGrid = [[0] * self.width] * self.height
        self.colorGrid = [[0 for i in range(self.width)] for j in range(self.height)]
        self.window = curses.newwin(self.height, self.width, self.x, self.y)
        self.window.keypad(True)
        self.curses_win = self.window
        self.panel = curses.panel.new_panel(self.curses_win)
        self.panel.hide()
        #self.fillChar = 9608    # unicode block
        self.fillChar = self.appState.colorPickChar # unicode block
        self.origin = self.x - 2
        #self.move(0,self.x - 2)
        self.move(0,self.origin)

    def drawBorder(self):
        """ Draw a highlighted border around color picker to show it is selected. """
        x = self.x - 2
        y = self.y - 1
        width = self.width + 1
        borderColor = curses.color_pair(self.appState.theme['menuBorderColor'])
        curses_addstr(self.parentWindow, y, x, ("." * (width)), borderColor | curses.A_BOLD)
        for line in range(1, self.height + 1):
            curses_addstr(self.parentWindow, y + line, x, (":"), borderColor | curses.A_BOLD)

    def hideBorder(self):
        x = self.x - 2
        y = self.y - 1
        width = self.width + 1
        borderColor = curses.color_pair(self.appState.theme['menuBorderColor'])
        curses_addstr(self.parentWindow, y, x, (" " * (width)))
        for line in range(1, self.height + 1):
            curses_addstr(self.parentWindow, y + line, x, (" "))

    def show(self):
        self.showFgPicker()

    def hide(self):
        self.panel.bottom()
        try:
            self.panel.hide()
        except:
            pass

    def move(self, x, y):
        self.x = x
        self.y = y
        try:
            self.panel.move(y, x)
        except Exception as E:
            #self.colorPicker.caller.notify(f"Exception {E}")
            #pdb.set_trace()
            pass
        self.origin = self.y

    def updateFgPicker(self):
        line = 0
        col = 1
        #maxWidth = self.realmaxX
        #maxHeight = self.realmaxY
        #for fg in range(0,curses.COLORS):  # 0-255
        width_counter = 0   # for color block width
        for fg in range(1,self.appState.totalFgColors+1):  # 0-255
            color_pair = curses.color_pair(fg)
            if col >= self.width - 2:
                col = 0
                line += 1
            if fg == 16:    # first color for fancy displayed block color palette thing
                line += 1
                col = 0
            if fg > 16:
                width_counter += 1
            if width_counter == 36:
                width_counter = 0
                #line += 1
            try:
                self.colorGrid[line][col] = fg
            except IndexError:
                pass
            #if line > 0:
            #    pdb.set_trace()
            #curses_addstr(self.window, self.colorPicker.y + line, self.colorPicker.x + col, chr(self.fillChar), color_pair)
            # if fg == app's current fg, draw it as a * instead of self.fillChar
            if fg == self.colorPicker.caller.colorfg:
                if fg == 1: # black
                    plain_color_pair = curses.color_pair(9)
                    if self.appState.colorPickerSelected:
                        curses_addstr(self.window, line, col, 'X', plain_color_pair | curses.A_UNDERLINE | curses.A_BLINK)
                    else:
                        curses_addstr(self.window, line, col, 'X', plain_color_pair)
                else:
                    if self.appState.colorPickerSelected:
                        curses_addstr(self.window, line, col, 'X', color_pair | curses.A_UNDERLINE | curses.A_BLINK)
                    else:
                        curses_addstr(self.window, line, col, 'X', color_pair)
            else:
                curses_addstr(self.window, line, col, self.fillChar, color_pair)
            col += 1
        curses_addstr(self.window, line, col + 5, "     ", color_pair)
        curses_addstr(self.window, line, col + 5, str(self.colorPicker.caller.colorfg), color_pair)

    def showFgPicker(self):
        self.showColorPicker(type="fg")

    def showColorPicker(self, type="fg"):
        """ Shows picker, has UI loop for letting user pick color with keyboard or mouse """
        if type == "fg":
            self.updateFgPicker()
        elif type == "bg":
            self.updateBgPicker()
        prompting = True
        self.window.nodelay(1)
        #print('\033[?1003l') # disable mouse movement tracking (xterm api)
        #curses.mousemask(1)
        curses_cursorOff()
        # populate window with colors
        self.panel.top()
        #self.move(0,self.x - 6)
        self.panel.show()
        oldColor = self.colorPicker.caller.colorfg
        color = self.colorPicker.caller.colorfg
        if self.appState.colorPickerSelected:
            prompting = True
        else:
            prompting = False
        if self.appState.colorPickerSelected:
            if self.appState.sideBarShowing:
                self.drawBorder()
        while(prompting):
            time.sleep(0.01)
            #self.colorPicker.caller.drawStatusBar()
            self.update()
            c = self.window.getch()
            if c in [98, curses.KEY_LEFT]:
                if color == 0:
                    color = curses.COLORS - 1
                else:
                    color -= 1
                #self.colorPicker.caller.colorfg = color
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c in [102, curses.KEY_RIGHT]:
                color += 1
                if color >= curses.COLORS:
                    color = 0
                #self.colorPicker.caller.colorfg = color
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c == curses.KEY_UP:
                if color < 32:
                    color -= 16
                elif color > 31 and color < 52:
                    color = 15
                else:
                    color -= self.width - 2
                if color <= 0:
                    color = 1
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c == curses.KEY_DOWN:
                if color < 16:
                    color += 16
                else:
                    color += self.width - 2
                if color >= curses.COLORS:
                    color = curses.COLORS - 1
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c == curses.KEY_HOME:
                color = 1
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c == curses.KEY_END:
                color = 255
                self.colorPicker.caller.setFgColor(color)
                self.updateFgPicker()
                self.colorPicker.caller.drawStatusBar()
            elif c in [13, curses.KEY_ENTER, 9, 353]:   # Return, Accept color. 9=tab, 353=shift-tab
                #if not self.appState.stickyColorPicker:
                if not self.appState.sideBarShowing:
                    self.hide()
                prompting = False
                self.updateFgPicker()
                pass
            elif c == curses.KEY_MOUSE:
                try:
                    _, mouseX, mouseY, _, mouseState = curses.getmouse()
                except:
                    pass

                if not self.appState.hasMouseScroll:
                    curses.BUTTON5_PRESSED = 0
                    curses.BUTTON4_PRESSED = 0
                if mouseState & curses.BUTTON4_PRESSED: # wheel up
                    color += 1
                    if color >= curses.COLORS:
                        color = 0
                    #self.colorPicker.caller.colorfg = color
                    self.colorPicker.caller.setFgColor(color)
                    self.updateFgPicker()
                    self.colorPicker.caller.drawStatusBar()
                elif mouseState & curses.BUTTON5_PRESSED:   # wheel down
                    if color == 0:
                        color = curses.COLORS - 1
                    else:
                        color -= 1
                    #self.colorPicker.caller.colorfg = color
                    self.colorPicker.caller.setFgColor(color)
                    self.updateFgPicker()
                    self.colorPicker.caller.drawStatusBar()
                elif mouseY >= self.origin and mouseX > self.x and mouseX < self.x + len(self.colorGrid[0])-2:   # cpicked in the color picker
                    #self.colorPicker.caller.notify(f"DEBUG: self.origin={self.origin}, self.x = {self.x}. mouseX={mouseX}, mouseY={mouseY}", pause=True)
                    self.gotClick(mouseX, mouseY)
                    prompting = False

                    #clickedCol = mouseX - self.x
                    #clickedLine = mouseY - self.origin
                    #if mouseY < self.origin + self.height:
                    #    if self.colorGrid[clickedLine][clickedCol] != 0:
                    #        # We're in the grid. Set color
                    #        color = self.colorGrid[clickedLine][clickedCol]
                    #        self.colorPicker.caller.setFgColor(color)
                    #        self.updateFgPicker()



                if not prompting:
                    if not self.appState.sideBarShowing:
                        self.hide()
                #self.hide()
                #prompting = False
            elif c == 27:  # normal esc, Cancel
                c = self.window.getch()
                if c == curses.ERR: # Just esc was hit, no other escape sequence
                    self.colorPicker.caller.setFgColor(oldColor)
                    self.updateFgPicker()
                    if not self.appState.sideBarShowing:
                        self.hide()
                    #self.hide()
                    prompting = False

        if self.appState.colorPickerSelected:
            if self.appState.sideBarShowing:
                self.hideBorder()

        self.appState.colorPickerSelected = False   # done prompting
        self.updateFgPicker()

        if not self.appState.sideBarShowing:
            self.hide()

        #self.hide()
        curses_cursorOn()
        self.window.nodelay(0)
        #curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
        #print('\033[?1003h') # enable mouse tracking
        return color

    def gotClick(self, mouseX, mouseY):
        if mouseY >= self.origin and mouseX < + self.x + len(self.colorGrid[0])-2:   # cpicked in the color picker
            clickedCol = mouseX - self.x
            clickedLine = mouseY - self.origin
            if mouseY < self.origin + self.height:
                if self.colorGrid[clickedLine][clickedCol] != 0:
                    color = self.colorGrid[clickedLine][clickedCol]
                    self.colorPicker.caller.setFgColor(color)
                    self.updateFgPicker()


    def update(self):
        curses.panel.update_panels()
        curses.doupdate()
        self.window.refresh()

class ColorSwatchHandler:
    def __init__(self, colorSwatch, window):
        self.colorSwatch = colorSwatch
        self.window = window
        self.fillChar = 9608    # unicode block
    def draw(self, plusX=0, plusY=0):
        for c in range(0, len(self.colorSwatch.bank)-1):
            curses_addstr(self.window, self.colorSwatch.y, self.colorSwatch.x, chr(self.fillChar))

class FgBgColorPickerHandler:
    def __init__(self, fgBgPicker, x=0, y=0):
        self.fgBgPicker = fgBgPicker
        self.window = fgBgPicker.window 
        self.x = x
        self.y = y
        #self.on_click = on_click
    def draw(self, plusX=0, plusY=0):
        curses_addstr(self.window, self.y, self.x, "F:  G:  ")

class ToolTipHandler:
    """ Draw and hide tooltips """
    #def __init__(self, tooltip, window, appState=None):
    def __init__(self, tooltip, context):
        self.tooltip = tooltip
        self.window = context.window
        self.appState = context.appState

    def draw(self):
        tipString = self.tooltip.hotkey
        tipColor = self.appState.theme['clickHighlightColor'] | curses.A_BOLD | curses.A_UNDERLINE
        #curses_addstr(self.window, self.tooltip.column, self.tooltip.row, tipString, tipColor)
        curses_addstr(self.window, self.tooltip.row, self.tooltip.column, tipString, tipColor)

    def show(self):
        self.draw()

    def hide (self):
        pass


class ButtonHandler:
    """ hook into Curses to draw button
    """
    def __init__(self, button, window, on_click, appState=None):
        #self.label = button.label
        self.button = button
        self.window = window
        self.x = self.button.x
        self.y = self.button.y
        self.on_click = on_click
        self.appState = appState
        self.color = curses.color_pair(self.appState.theme['clickColor']) | curses.A_BOLD   # bright green, clickable

    def draw(self, plusX=0, plusY=9):
        if not self.button.invisible:
            textColor = self.color
            if self.button.selected:
                #curses_notify(self.window, "Tacos")
                textColor = textColor | curses.A_REVERSE
            if self.button:   # a selector type button, to be iframed in []s
                buttonString = f"[{self.button.label}]"
            else:
                buttonString = self.button.label
            #curses_addstr(self.window, plusX + self.button.x, plusY + self.button.y, self.button.label)
            #curses_addstr(self.window, plusX + self.button.x, plusY + self.button.y, self.button.label, self.color)
            #curses_addstr(self.window, self.button.realX, self.button.realY, self.button.label, textColor)
            curses_addstr(self.window, self.button.realX, self.button.realY, buttonString, textColor)
            # render the button on the window
            if self.button.persistant_tooltip or not self.button.tooltip_hidden:
                if self.button.get_tooltip_command():
                    toolTip :str = self.button.get_tooltip_command()
                    tipColor = self.appState.theme['clickHighlightColor'] | curses.A_BOLD | curses.A_UNDERLINE
                    # Figure out if the hint is in the button label, if so, place it over it with
                    # an index offset
                    tipColOffset = 0
                    if toolTip.lower() in self.button.label.lower():
                        tipColOffset = self.button.label.lower().index(toolTip.lower()) + 1
                        #curses_notify(self.window, "Gorditas")
                    # keep the tip from going off screen for some buttons
                    if self.button.realY == 0 and tipColOffset == 0:
                        tipColOffset += 1
                    # Print it next to the button for now
                    curses_addstr(self.window, self.button.realX, self.button.realY + tipColOffset, toolTip, tipColor)


    def showToolTip(self):
        self.button.tooltip_hidden = False

    def hideToolTip(self):
        self.button.tooltip_hidden = True
        # Cover up with spaces
        #if not self.button.hidden:
        #    self.button.draw()
        #if self.button.get_tooltip_command() and not self.button.hidden:
        #    toolTip :str = self.button.get_tooltip_command()
        #    toolTip = " " * len(toolTip)
        #    curses_addstr(self.window, self.button.realX, self.button.realY, toolTip)

    def hide(self):
        self.hidden = True

    def on_click(self):
        curses_addstr(self.window, 0, 0, f"{self.button.label} clicked")

    def update_real_xy(x=0, y=0):
        self.button.realX = x
        self.button.realY = y

    def handle_event(self, event):
        # handle events for the button
        if event.type == 'click':
            self.on_click()
        return True

class StatusBarHandler:
    def __init__(self, statusBar, window): 
        self.statusBar = statusBar
        self.window = window
        self.panel = curses.panel.new_panel(self.window)
        #curses_addstr(window, self.statusBar.x, self.statusBar.y, "Fnord")
        #self.on_click = on_click

    def draw(self, plusX=0, plusY=0):
        pass
        #for item in self.statusBar.items:
        #    curses_addstr(self.window, self.statusBar.x + item.x, self.statusBar.y + item.y, item.label)

    def handle_event(self, event):
        # handle events for the button
        if event.type == 'click':
            self.on_click()
        return True



