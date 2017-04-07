""" This module contains all GUI needs. """
from tkinter import *
from tkinter import messagebox as tkmb
import settings as s
import app.algo as a


class Field:
    """ Represents Checkers field. """

    # store defaults
    _columns = s.COLUMNS
    _rows = s.ROWS
    _checkers = s.CHECKERS

    def __init__(self, frame):
        self.frame = frame
        DotButton.frame = frame
        DotButton.field = self
        # define attributes
        self.checkers = None
        self.rows = None
        self.columns = None
        self.checkers_left = None
        self.points = None
        self.checkers_used_list = []

    def draw(self, **kwargs):
        self.checkers = kwargs.get('checkers', self._checkers)
        self.rows = kwargs.get('rows', self._rows)
        self.columns = kwargs.get('columns', self._columns)
        # draw widgets
        for y in range(self.rows):
            for x in range(self.columns):
                DotButton(x, y)

    def clear(self):
        for item in DotButton.all:
            item.widget.grid_forget()
            del item.widget
            del item
        DotButton.all = []
        self.checkers_used_list = []

    def reset(self):
        for item in DotButton.all:
            item.deactivate()
        self.checkers_used_list = []

    def get_input(self):
        return self.checkers_used_list


class DotButton:
    all = []
    frame = None
    field = None
    # graphics
    _active_background = 'black'
    _not_active_background = 'white'
    _active_font = 'white'
    _not_active_font = 'black'
    _pad = 3
    _size = 2

    def __init__(self, x, y):
        text = '{},{}'.format(x,y)
        widget = Button(
            self.frame,
            text=text,
            background=self._not_active_background,
            foreground=self._not_active_font,
            height=self._size,
            width=self._size,
            command=self._press(text),
        )
        widget.grid(row=y, column=x,
                    padx=self._pad, pady=self._pad)
        self.widget = widget
        self.text = text
        self.all.append(self)

    def _press(self, text):
        x, y = text.split(',')
        x, y = int(x), int(y)
        def command():
            try:
                index = self.field.checkers_used_list.index((x, y))
            except ValueError:
                self.field.checkers_used_list.append((x, y))
                self.activate()
            else:
                self.field.checkers_used_list.pop(index)
                self.deactivate()
        return command

    def activate(self):
        self.widget['background'] = self._active_background
        self.widget['foreground'] = self._active_font

    def deactivate(self):
        self.widget['background'] = self._not_active_background
        self.widget['foreground'] = self._not_active_font


# main Application
class GUI:
    """ Represents GUI tkinter application. """

    _goal = s.GOAL

    def __init__(self, master):
        self.master = master
        self._define_frames()
        self._define_menu()
        self._define_field()
        self.goal = None

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
        reset_button = Button(text='Reset', command=self.reset_field)
        calculate_button = Button(text='Calculate', command=self.calculate)
        # pack
        quit_button.pack(side=TOP)
        draw_button.pack(side=TOP)
        clear_button.pack(side=TOP)
        reset_button.pack(side=TOP)
        calculate_button.pack(side=BOTTOM)
        # bind
        frame.quit = quit_button
        frame.draw = draw_button
        frame.clear = clear_button
        frame.reset = reset_button
        frame.calculate = calculate_button

    def _define_field(self):
        self.field = Field(self.field_frame)

    def draw_field(self):
        self.field.draw()

    def clear_field(self):
        self.field.clear()

    def reset_field(self):
        self.field.reset()

    def calculate(self):
        if not self.goal:
            self.goal = self._goal
        input = self.field.get_input()
        output = a.calculate(input, self.goal)
        self.show_points(output)
        # log it
        print('{}\n\t{}'.format(input, output))

    def show_points(self, points):
        tkmb.showinfo(title='Calculation', message='You have {} points!'.format(points))


# main
def launch_gui():
    root = Tk()
    app = GUI(root)
    root.mainloop()
