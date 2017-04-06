""" This module contains all GUI needs. """
from tkinter import *
import settings as s
from .algo import calculate


class Field:
    """ Represents Checkers field. """
    def __init__(self, frame):
        self.frame = frame
        # store defaults
        self._columns = s.COLUMNS
        self._rows = s.ROWS
        self._checkers = s.CHECKERS
        self._goal = s.GOAL
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
                widget = Button(self.frame,
                                text='{},{}'.format(x,y),
                                background='white',
                                height=2, width=2,
                                command=self._press(x, y),)
                widget.grid(row=y, column=x, padx=5, pady=5)
                self._widgets_list.append(widget)

    def _press(self, x, y):
        def command():
            index = self.checkers_used_list.index((x, y))
            if index != -1:
                self.checkers_used_list.pop(index)
            else:
                self.checkers_used_list.append((x, y))
        return command

    def clear(self):
        for widget in self._widgets_list:
            widget.grid_forget()
            del widget

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
        print('Drawing field...')
        self.field.draw()

    def clear_field(self):
        print('Clearing field...')
        self.field.clear()

    def calculate(self):
        print('Calculating...')


# main
def launch_gui():
    root = Tk()
    app = GUI(root)
    root.mainloop()
