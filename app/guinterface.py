""" This module contains all GUI needs. """
import tkinter as tk
from tkinter import messagebox as tkmb
import settings as s
import app.algo as a


class Field:
    """ Represents Checkers field. """

    # graphics
    _background = 'grey70'

    def __init__(self, app, frame):
        self.app = app
        self.frame = frame
        self.visible = False
        # configure frame
        self.frame.configure(background=self._background)

    def draw(self, **kwargs):
        if self.visible:
            self.clear()
        self.app.checkers = kwargs.get('checkers', self.app._checkers)
        self.app.rows = kwargs.get('rows', self.app._rows)
        self.app.columns = kwargs.get('columns', self.app._columns)
        # draw widgets
        for y in range(self.app.rows):
            for x in range(self.app.columns):
                DotButton(self.app, self, x, y)
        self.visible = True

    def clear(self):
        for item in DotButton.all:
            item.widget.grid_forget()
            del item.widget
            del item
        DotButton.all = []
        self.app.checkers_used_list = []
        self.visible = False

    def reset(self):
        for item in DotButton.all:
            item.deactivate()
        self.app.checkers_used_list = []


class Menu:
    """ Represents Menu Frame. """

    _width = s.MENU_WIDTH
    _quit_fg = s.QUIT_FG
    _quit_bg = s.QUIT_BG
    _calculate_height = s.CALCULATE_HIGHT
    _calculate_bg = s.CALCULATE_BG
    _reset_bg = s.RESET_BG

    def __init__(self, app, frame):
        self.app = app
        self.frame = frame
        self.define_variables()
        # draw
        self.draw()

    def define_variables(self):
        self.columns_var = tk.IntVar()
        self.rows_var = tk.IntVar()
        self.checkers_var = tk.IntVar()
        self.goal_var = tk.IntVar()
        self.coordinates_var = tk.BooleanVar()
        # set defaults
        self.columns_var.set(self.app._columns)
        self.rows_var.set(self.app._rows)
        self.checkers_var.set(self.app._checkers)
        self.goal_var.set(self.app._goal)
        self.coordinates_var.set(self.app._coordinates)

    def draw(self):
        # init
        quit_button = tk.Button(text='QUIT',
                                command=quit,
                                width=self._width,
                                fg=self._quit_fg, bg=self._quit_bg)
        draw_button = tk.Button(text='Draw',
                                command=self.draw_field,
                                width=self._width)
        clear_button = tk.Button(text='Clear',
                                 command=self.clear_field,
                                 width=self._width)
        reset_button = tk.Button(text='Reset',
                                 command=self.reset_field,
                                 width=self._width,
                                 bg=self._reset_bg,)
        calculate_button = tk.Button(text='Calculate',
                                     command=self.calculate,
                                     height=self._calculate_height,
                                     width=self._width,
                                     bg=self._calculate_bg)
        columns_label = tk.Label(text='Columns:',
                                 width=self._width)
        columns_entry = tk.Entry(textvariable=self.columns_var,
                                 width=self._width)
        rows_label = tk.Label(text='Rows:',
                              width=self._width)
        rows_entry = tk.Entry(textvariable=self.rows_var,
                              width=self._width,)
        checkers_label = tk.Label(text='Checkers:',
                                  width=self._width)
        checkers_entry = tk.Entry(textvariable=self.checkers_var,
                                  width=self._width,)
        goal_label = tk.Label(text='Goal:',
                              width=self._width)
        goal_entry = tk.Entry(textvariable=self.goal_var,
                              width=self._width,)
        coordinates_check = tk.Checkbutton(text='Show coordinates?',
                                           width=self._width,
                                           variable=self.coordinates_var,
                                           onvalue=True, offvalue=False,)
        # pack
        quit_button.pack(side=tk.TOP)
        draw_button.pack(side=tk.TOP)
        clear_button.pack(side=tk.TOP)
        columns_label.pack()
        columns_entry.pack()
        rows_label.pack()
        rows_entry.pack()
        checkers_label.pack()
        checkers_entry.pack()
        goal_label.pack()
        goal_entry.pack()
        coordinates_check.pack()
        calculate_button.pack(side=tk.BOTTOM)
        reset_button.pack(side=tk.BOTTOM)
        # bind
        self.frame.quit = quit_button
        self.frame.draw = draw_button
        self.frame.clear = clear_button
        self.frame.reset = reset_button
        self.frame.columns_label = columns_label
        self.frame.columns_entry = columns_entry
        self.frame.rows_label = rows_label
        self.frame.rows_entry = rows_entry
        self.frame.checkers_label = checkers_label
        self.frame.checkers_entry = checkers_entry
        self.frame.goal_label = goal_label
        self.frame.goal_entry = goal_entry
        self.frame.coordinates_check = coordinates_check
        self.frame.calculate = calculate_button

    def draw_field(self):
        self.app.coordinates = self.coordinates_var.get()
        self.app.field.draw(
            columns=self.columns_var.get(),
            rows=self.rows_var.get(),
            checkers=self.checkers_var.get(),
        )
        self.app.goal = self.goal_var.get()

    def clear_field(self):
        self.app.field.clear()

    def reset_field(self):
        self.app.field.reset()

    def calculate(self):
        points = a.calculate(self.app.checkers_used_list, self.app.goal)
        self.app.show_points(points)


class DotButton:
    all = []
    # graphics
    _active_background = 'black'
    _active_font = 'white'

    _not_active_background = 'white'
    _not_active_font = 'black'

    _pad = 3
    _height = s.HEIGHT
    _width = s.WIDTH

    def __init__(self, app, field, x, y):
        self.app = app
        self.field = field
        widget = tk.Button(
            self.field.frame,
            background=self._not_active_background,
            foreground=self._not_active_font,
            height=self._height,
            width=self._width,
            command=self._press(x, y),
        )
        if self.app.coordinates:
            widget.configure(text='{},{}'.format(x,y),
                             width=self._width*2, height=self._height*2)
        widget.grid(row=y, column=x,
                    padx=self._pad, pady=self._pad)
        self.widget = widget
        self.all.append(self)

    def _press(self, x, y):
        def command():
            if self.app.is_used(x, y):
                self.app.remove(x, y)
                self.deactivate()
            elif self.app.can_put():
                self.app.put(x, y)
                self.activate()
        return command

    def activate(self):
        self.widget['background'] = self._active_background
        self.widget['foreground'] = self._active_font

    def deactivate(self):
        self.widget['background'] = self._not_active_background
        self.widget['foreground'] = self._not_active_font


# main Application
class App:
    """ Represents GUI tkinter application. """

    # store defaults
    _columns = s.COLUMNS
    _rows = s.ROWS
    _checkers = s.CHECKERS
    _goal = s.GOAL
    _coordinates = s.COORDINATES

    def __init__(self, master):
        self.master = master

        self.field_frame = tk.Frame(self.master)
        self.menu_frame = tk.Frame(self.master)
        # pack frames
        self.field_frame.pack(side=tk.LEFT)
        self.menu_frame.pack(side=tk.RIGHT)

        self.menu = Menu(self, self.menu_frame)
        self.field = Field(self, self.field_frame)

        # define attributes
        self.checkers = None
        self.rows = None
        self.columns = None
        self.goal = None
        self.coordinates = None
        self.checkers_used_list = []

    @staticmethod
    def show_points(points):
        tkmb.showinfo(title='Calculation', message='You have {} points!'.format(points))

    def can_put(self):
        if len(self.checkers_used_list) < self.checkers:
            return True
        else:
            tkmb.showwarning(title='Rules Warning',
                             message='You cannot use more than {} checkers.'.format(self.checkers))

    def put(self, x, y):
        self.checkers_used_list.append((x, y))

    def remove(self, x, y):
        self.checkers_used_list.remove((x, y))

    def is_used(self, x, y):
        try:
            index = self.checkers_used_list.index((x, y))
        except ValueError:
            return False
        else:
            return True


# main
def launch_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()
