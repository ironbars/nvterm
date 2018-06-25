import os
import time

from prompt_toolkit.layout.controls import UIControl, UIContent
from prompt_toolkit.token import Token
from prompt_toolkit.layout.screen import Point, Char


class MenuControl(UIControl):
    """
    UIControl suitable for displaying a full screen menu
    """
    def __init__(self, menu_items):
        assert isinstance(menu_items, list)

        self.menu_items = menu_items
        self.current_selection = 0

    def create_content(self, cli, width, height):
        def get_menu_item(i):
            if i == self.current_selection:
                token = Token.SetCursorPosition
            else:
                token = Token.Text

            return [(token, self.menu_items[i])]

        return UIContent(get_line=get_menu_item,
                         cursor_position=Point(x=0, y=self.current_selection),
                         line_count=len(self.menu_items),
                         default_char=Char(" ", Token.Text))

    def move_cursor_down(self, cli):
        self.current_selection = ((self.current_selection + 1) %
                                   len(self.menu_items))

    def move_cursor_up(self, cli):
        self.current_selection = ((self.current_selection - 1) %
                                   len(self.menu_items))

    def get_selection(self):
        return self.menu_items[self.current_selection]


class FileData(object):
    """
    Class to hold file meta data and (by extension) a reference to a file
    """
    def __init__(self, filepath):
        assert os.path.exits(filepath) and os.path.isfile(filepath)

        self.filepath = filepath
        self.mtime = os.path.getmtime(self.filepath)

    def repr_mtime(self):
        return time.strftime("%I:%M %p, %b %d", time.localtime(self.mtime))
