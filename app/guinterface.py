""" This module contains all GUI needs. """
import tkinter as tk
from tkinter import messagebox as tkmb
from tkinter import simpledialog as tksd
from .algorithm import algo
import settings as s
import app.logger as lg


# DotButton
class DotButton:
    all = []
    # graphics
    _active_background = 'black'
    _active_font = 'white'

    _not_active_background = 'white'
    _not_active_font = 'black'

    _pad = s.DB_PAD
    _height = s.DB_HEIGHT
    _width = s.DB_WIDTH

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


# Frames
class Field:
    """ Represents Checkers field. """

    # graphics
    _background = s.FIELD_BACKGROUND

    def __init__(self, app, frame):
        self.app = app
        self.frame = frame
        # configure frame
        self.frame.configure(background=self._background)

    def draw(self, **kwargs):
        self.app.checkers = kwargs.get('checkers', self.app._checkers)
        self.app.rows = kwargs.get('rows', self.app._rows)
        self.app.columns = kwargs.get('columns', self.app._columns)
        # draw widgets
        for y in range(self.app.rows):
            for x in range(self.app.columns):
                DotButton(self.app, self, x, y)

    def reset(self):
        for item in DotButton.all:
            item.deactivate()
        self.app.checkers_used_list = []
        algo.clear()


class Menu:
    """ Represents Menu Frame. """

    _background = s.MENU_BACKGROUND
    _width = s.MENU_WIDTH
    _draw_bg = s.DRAW_BG
    _reset_bg = s.RESET_BG
    _save_height = s.SAVE_HIGHT
    _save_bg = s.SAVE_BG

    def __init__(self, app, frame):
        self.app = app
        self.frame = frame
        self.define_variables()
        # draw
        self.frame.configure(background=self._background)
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
        draw_button = tk.Button(text='Draw',
                                command=self.draw_field,
                                width=self._width,
                                bg=self._draw_bg)
        reset_button = tk.Button(text='Reset',
                                 command=self.reset_field,
                                 width=self._width,
                                 bg=self._reset_bg,)
        save_button = tk.Button(text='Save',
                                command=self.save,
                                width=self._width, height=self._save_height,
                                bg=self._save_bg)
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
        checkers_used_label = tk.Label(text='Checkers used: 0',
                                       width=self._width,)
        points_label = tk.Label(text='Points: 0',
                                width=self._width)
        # pack
        draw_button.pack(side=tk.TOP)
        columns_label.pack(side=tk.TOP)
        columns_entry.pack(side=tk.TOP)
        rows_label.pack(side=tk.TOP)
        rows_entry.pack(side=tk.TOP)
        checkers_label.pack(side=tk.TOP)
        checkers_entry.pack(side=tk.TOP)
        goal_label.pack(side=tk.TOP)
        goal_entry.pack(side=tk.TOP)
        coordinates_check.pack(side=tk.TOP)
        # bind
        self.frame.draw = draw_button
        self.frame.columns_label = columns_label
        self.frame.columns_entry = columns_entry
        self.frame.rows_label = rows_label
        self.frame.rows_entry = rows_entry
        self.frame.checkers_label = checkers_label
        self.frame.checkers_entry = checkers_entry
        self.frame.goal_label = goal_label
        self.frame.goal_entry = goal_entry
        self.frame.coordinates_check = coordinates_check
        self.frame.checkers_used = checkers_used_label
        self.frame.points = points_label
        self.frame.reset = reset_button
        self.frame.save = save_button

    def draw_field(self):
        self.clear_field()
        self.app.coordinates = self.coordinates_var.get()
        self.app.field.draw(
            columns=self.columns_var.get(),
            rows=self.rows_var.get(),
            checkers=self.checkers_var.get(),
        )
        algo.set_goal(self.goal_var.get())
        # Show hidden buttons
        self.frame.save.pack(side=tk.BOTTOM)
        self.frame.reset.pack(side=tk.BOTTOM)
        self.frame.points.pack(side=tk.BOTTOM)
        self.frame.checkers_used.pack(side=tk.BOTTOM)
        self.frame.draw.configure(text='Redraw')

    def clear_field(self):
        for item in DotButton.all:
            item.widget.grid_forget()
            del item.widget
            del item
        DotButton.all = []
        self.app.checkers_used_list = []
        algo.clear()
        self.update_points_label()
        self.update_chackers_used_label()

    def reset_field(self):
        self.app.field.reset()
        self.update_chackers_used_label()
        self.update_points_label()

    def save(self):
        lg.team_lg.info('Name: "{name}" Points: {points} Checkers: {checkers}'.format(
            name=self.save_dialog(),
            points=algo.get_points(),
            checkers=self.app.checkers_used_list,
        ))

    @staticmethod
    def save_dialog():
        return tksd.askstring(title='Saving',
                              prompt='You have {} points.\nEnter the name.'.format(
                                  algo.get_points()
                              ))

    def update_chackers_used_label(self):
        self.frame.checkers_used.configure(text='Checkers used: {}'.format(
            len(self.app.checkers_used_list)
        ))

    def update_points_label(self):
        self.frame.points.configure(text='Points: {}'.format(
            algo.get_points()
        ))


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
        self._define_frames()
        self._define_variables()

    def _define_frames(self):
        self._define_field_frame()
        # define Menu frame
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(side=tk.RIGHT)
        self.menu = Menu(self, self.menu_frame)

    def _define_field_frame(self):
        self.field_frame = tk.Frame(self.master)
        self.field_frame.pack(side=tk.LEFT)
        self.field = Field(self, self.field_frame)

    def _define_variables(self):
        self.checkers = None
        self.rows = None
        self.columns = None
        self.coordinates = None
        self.checkers_used_list = []

    def can_put(self):
        if len(self.checkers_used_list) < self.checkers:
            return True
        else:
            tkmb.showwarning(title='Rules Warning',
                             message='You cannot use more than {} checkers.'.format(self.checkers))

    def put(self, x, y):
        self.checkers_used_list.append((x, y))
        algo.new_dot(x, y)
        self.menu.update_chackers_used_label()
        self.menu.update_points_label()

    def remove(self, x, y):
        self.checkers_used_list.remove((x, y))
        algo.remove_dot(x, y)
        self.menu.update_chackers_used_label()
        self.menu.update_points_label()

    def is_used(self, x, y):
        try:
            index = self.checkers_used_list.index((x, y))
        except ValueError:
            return False
        else:
            return True


class TeamApp(App):
    """ Application for usage in olympiads. """

    def _define_frames(self):
        self._define_field_frame()
        # define Settings TopLevel
        self.settings_frame = tk.Toplevel(self.master)
        self.settings_frame.title('Game settings')
        self.settings = None

# main
def launch_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()


def launch_olymp():
    root = tk.Tk()
    TeamApp(root)
    root.mainloop()
