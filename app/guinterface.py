""" This module contains all GUI needs. """
from tkinter import *
import settings as s
from .algo import calculate


class Field:
    """ Represents Checkers field. """

    # store defaults
    _columns = s.COLUMNS
    _rows = s.ROWS
    _checkers = s.CHECKERS
    _goal = s.GOAL
    # graphics
    _active_background = 'black'
    _not_active_background = 'white'
    _active_font = 'white'
    _not_active_font = 'black'

    def __init__(self, frame):
        self.frame = frame
        # define attributes
        self.goal = None
        self.checkers = None
        self.rows = None
        self.columns = None
        self.checkers_left = None
        self.points = None
        self.checkers_used_list = []
        self._widgets_list = []
        self.widgets_map = {}

    def draw(self, **kwargs):
        self.goal = kwargs.get('goal', self._goal)
        self.checkers = kwargs.get('checkers', self._checkers)
        self.rows = kwargs.get('rows', self._rows)
        self.columns = kwargs.get('columns', self._columns)
        # draw widgets
        for y in range(self.rows):
            for x in range(self.columns):
                text = '{},{}'.format(x,y)
                widget = Button(
                    self.frame,
                    text=text,
                    background=self._not_active_background,
                    foreground=self._not_active_font,
                    height=2,
                    width=2,
                    command=self._press(text),
                )
                widget.grid(row=y, column=x, padx=5, pady=5)
                self._register_widget(widget)

    def _register_widget(self, widget):
        self._widgets_list.append(widget)
        self.widgets_map[widget['text']] = widget

    def _remove_widget(self, widget):
        widget.grid_forget()
        self.widgets_map.pop(widget['text'])
        del widget

    def _press(self, text):
        x, y = text.split(',')
        x, y = int(x), int(y)
        def command():
            try:
                index = self.checkers_used_list.index((x, y))
            except ValueError:
                self.checkers_used_list.append((x, y))
                self.widgets_map[text]['background'] = self._active_background
                self.widgets_map[text]['foreground'] = self._active_font
            else:
                self.checkers_used_list.pop(index)
                self.widgets_map[text]['background'] = self._not_active_background
                self.widgets_map[text]['foreground'] = self._not_active_font
        return command

    def clear(self):
        for widget in self._widgets_list:
            self._remove_widget(widget)

    def get_input(self):
        output = self.checkers_used_list.copy()
        self.checkers_used_list = []
        return output


# main Application
class GUI:
    """ Represents GUI tkinter application. """

    def __init__(self, master):
        self.master = master
        self._define_frames()
        self._define_menu()
        self._define_field()

    def _define_frames(self):
        self.field_frame = Frame(self.master)
        self.menu_frame = Frame(self.master)
        # pack them
        self.field_frame.pack(side=LEFT)
        self.menu_frame.pack(side=RIGHT)

    def _define_menu(self):
        frame = self.menu_frame
        # init
        quit_button = Button(text='QUIT', fg='red', command=quit)
        draw_button = Button(text='Draw', command=self.draw_field)
        clear_button = Button(text='Clear', command=self.clear_field)
        calculate_button = Button(text='Calculate', command=self.calculate)
        # pack
        quit_button.pack(side=TOP)
        draw_button.pack(side=TOP)
        clear_button.pack(side=TOP)
        calculate_button.pack(side=TOP)
        # bind
        frame.quit = quit_button
        frame.draw = draw_button
        frame.clear = clear_button
        frame.calculate = calculate_button

    def _define_field(self):
        self.field = Field(self.field_frame)

    def draw_field(self):
        self.field.draw()

    def clear_field(self):
        self.field.clear()

    def calculate(self):
        input = self.field.get_input()
        output = calculate(input)
        print('{}\n\t{}'.format(input, output))


# main
def launch_gui():
    root = Tk()
    app = GUI(root)
    root.mainloop()
