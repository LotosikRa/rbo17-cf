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

    def draw(self):
        # draw widgets
        for y in range(self.app.rows):
            for x in range(self.app.columns):
                DotButton(self.app, self, x, y)

    def reset(self):
        for item in DotButton.all:
            item.deactivate()
        self.app.clear()


class Menu:
    """ Represents Menu Frame. """

    _background = s.MENU_BACKGROUND
    _width = s.MENU_WIDTH
    _draw_bg = s.DRAW_BG
    _reset_bg = s.RESET_BG
    _save_height = s.SAVE_HIGHT
    _save_bg = s.SAVE_BG

    _save_dialog_tmp = \
        ''' Do you want to save this record?
        
            Name: {name}
            Points: {points}'''

    _goal_values = tuple(range(3, 5 + 1))
    _checkers_values = tuple(range(12, 20 + 1))
    _columns_values = tuple(range(4, 15 + 1))
    _rows_values = tuple(range(4, 15 + 1))

    def __init__(self, app, frame):
        self.app = app
        self.frame = frame
        self._define_variables()
        # draw
        self.frame.configure(background=self._background)
        self.draw()

    def _define_variables(self):
        self.coordinates_var = tk.BooleanVar()
        self.name_var = tk.StringVar()
        # set defaults
        # TODO: use self-attributes
        self.coordinates_var.set(self.app._coordinates)
        self.name_var.set(self.app._name)

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
        columns_spinbox = tk.Spinbox(
            values=self._columns_values,
            width=self._width,
        )
        rows_label = tk.Label(text='Rows:',
                              width=self._width)
        rows_spinbox = tk.Spinbox(
            values=self._rows_values,
            width=self._width,
        )
        checkers_label = tk.Label(text='Checkers:',
                                  width=self._width)
        checkers_spinbox = tk.Spinbox(
            values=self._checkers_values,
            width=self._width,
        )
        goal_label = tk.Label(text='Goal:',
                              width=self._width)
        goal_spinbox = tk.Spinbox(
            values=self._goal_values,
            width=self._width,
        )
        name_label = tk.Label(text='Name:',
                              width=self._width,)
        name_entry = tk.Entry(textvariable=self.name_var,
                              width=self._width,)
        coordinates_check = tk.Checkbutton(text='Show coordinates?',
                                           width=self._width,
                                           variable=self.coordinates_var,
                                           onvalue=True, offvalue=False,)
        # TODO: use secure entries instead of labels
        checkers_used_label = tk.Label(text='Checkers used: 0',
                                       width=self._width,)
        points_label = tk.Label(text='Points: 0',
                                width=self._width)
        # pack
        # TODO: use grid instead + use new width (6 , 3)
        draw_button.pack(side=tk.TOP)
        columns_label.pack(side=tk.TOP)
        columns_spinbox.pack(side=tk.TOP)
        rows_label.pack(side=tk.TOP)
        rows_spinbox.pack(side=tk.TOP)
        checkers_label.pack(side=tk.TOP)
        checkers_spinbox.pack(side=tk.TOP)
        goal_label.pack(side=tk.TOP)
        goal_spinbox.pack(side=tk.TOP)
        coordinates_check.pack(side=tk.TOP)
        # bind
        self.frame.draw = draw_button
        self.frame.columns_label = columns_label
        self.frame.columns_spinbox = columns_spinbox
        self.frame.rows_label = rows_label
        self.frame.rows_spinbox = rows_spinbox
        self.frame.checkers_label = checkers_label
        self.frame.checkers_spinbox = checkers_spinbox
        self.frame.goal_label = goal_label
        self.frame.goal_spinbox = goal_spinbox
        self.frame.name_label = name_label
        self.frame.name_entry = name_entry
        self.frame.coordinates_check = coordinates_check
        self.frame.checkers_used = checkers_used_label
        self.frame.points = points_label
        self.frame.reset = reset_button
        self.frame.save = save_button

    def draw_field(self):
        self.clear_field()
        self.update_app_variables()
        self.app.field.draw()
        # Show hidden buttons
        self.show_bottom_panel()

    def update_app_variables(self):
        self.app.columns = int(self.frame.columns_spinbox.get())
        self.app.rows = int(self.frame.rows_spinbox.get())
        self.app.coordinates = self.coordinates_var.get()

    def show_bottom_panel(self):
        # TODO: pack them only on start
        self.frame.save.pack(side=tk.BOTTOM)
        self.frame.reset.pack(side=tk.BOTTOM)
        self.frame.points.pack(side=tk.BOTTOM)
        self.frame.checkers_used.pack(side=tk.BOTTOM)
        self.frame.name_entry.pack(side=tk.BOTTOM)
        self.frame.name_label.pack(side=tk.BOTTOM)
        self.frame.draw.configure(text='Redraw')

    def clear_field(self):
        for item in DotButton.all:
            item.widget.grid_forget()
            del item.widget
            del item
        DotButton.all = []
        self.app.clear()
        self.update_points_label()
        self.update_chackers_used_label()

    def reset_field(self):
        self.app.field.reset()
        self.app.clear()
        self.update_chackers_used_label()
        self.update_points_label()

    def save(self):
        self.app.name = self.name_var.get()
        if self.save_dialog():
            self.app.save()

    def update_chackers_used_label(self):
        self.frame.checkers_used.configure(text='Checkers used: {}'.format(
            len(self.app.checkers_used_list)
        ))

    def update_points_label(self):
        self.frame.points.configure(text='Points: {}'.format(
            self.app.points
        ))

    def save_dialog(self):
        return tkmb.askquestion(
            title='Saving',
            message=self._save_dialog_tmp.format(
                name=self.app.name,
                points=self.app.points,
            )
        )

    def get_checkers(self):
        return int(self.frame.checkers_spinbox.get())


# main Application
class App:
    """ Represents GUI tkinter application. """

    # store defaults
    _columns = s.COLUMNS
    _rows = s.ROWS
    _checkers = s.CHECKERS
    _goal = s.GOAL
    _coordinates = s.COORDINATES
    _name = '---'

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
        self.points = None
        self.name = None

    def update_goal(self):
        self.goal = int(self.menu.frame.goal_spinbox.get())

    def can_put(self):
        self.checkers = self.menu.get_checkers()
        if len(self.checkers_used_list) < self.checkers:
            return True
        else:
            tkmb.showwarning(title='Rules Warning',
                             message='You cannot use more than {} checkers.'.format(self.checkers))

    def put(self, x, y):
        self.checkers_used_list.append((x, y))
        self.points = self._calculate()
        self.menu.update_chackers_used_label()
        self.menu.update_points_label()

    def remove(self, x, y):
        self.checkers_used_list.remove((x, y))
        self.points = self._calculate()
        self.menu.update_chackers_used_label()
        self.menu.update_points_label()

    def clear(self):
        self.checkers_used_list = []
        self.points = 0
        algo.clear()

    def is_used(self, x, y):
        try:
            self.checkers_used_list.index((x, y))
        except ValueError:
            return False
        else:
            return True

    def save(self):
        lg.team_lg.info('Name: "{name}" Points: {points} Checkers: {checkers}'.format(
            name=self.name,
            points=self.points,
            checkers=self.checkers_used_list,
        ))

    def _calculate(self):
        self.update_goal()
        return algo.calculate(self.checkers_used_list, self.goal)


# main
def launch_tkinter_gui():
    root = tk.Tk()
    App(root)
    root.mainloop()
