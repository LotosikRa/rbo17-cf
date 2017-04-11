""" This module contains all GUI needs. """
import tkinter as tk
from tkinter import messagebox as tkmb
from tkinter import simpledialog as tksd
from .algorithm import algo
import settings as s
import app.logger as lg


CHECKERS_COLUMN = 1
GOAL_COLUMN = 2
COLUMNS_COLUMN = 3
ROWS_COLUMN = 4


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


# Stage helper
class Stage:
    _checkers_column = CHECKERS_COLUMN
    _goal_column = GOAL_COLUMN
    _columns_column = COLUMNS_COLUMN
    _rows_column = ROWS_COLUMN
    _element_width = 6

    _goal_values = tuple(range(3, 5+1))
    _checkers_values = tuple(range(12, 20+1))
    _columns_values = tuple(range(4, 15+1))
    _rows_values = tuple(range(4, 15+1))

    _goal_default = s.GOAL
    _checkers_default = s.CHECKERS
    _columns_default = s.COLUMNS
    _rows_default = s.ROWS

    def __init__(self, frame, row):
        self.frame = frame
        self.row = row
        self._draw()

    def _draw(self):
        self.checkers_spinbox = tk.Spinbox(
            self.frame,
            values=self._checkers_values,
            width=self._element_width,
        )
        self.goal_spinbox = tk.Spinbox(
            self.frame,
            values=self._goal_values,
            width=self._element_width,
        )
        self.columns_spinbox = tk.Spinbox(
            self.frame,
            values=self._columns_values,
            width=self._element_width,
        )
        self.rows_spinbox = tk.Spinbox(
            self.frame,
            values=self._rows_values,
            width=self._element_width,
        )
        '''
        # select defaults
        self.checkers_spinbox.icursor(
            self._checkers_values.index(self._checkers_default))
        self.goal_spinbox.selection_adjust(
            self._goal_values.index(self._goal_default))
        self.columns_spinbox.selection_adjust(
            self._columns_values.index(self._columns_default))
        self.rows_spinbox.selection_adjust(
            self._rows_values.index(self._rows_default))
        '''
        # grid
        self.checkers_spinbox.grid(row=self.row, column=self._checkers_column)
        self.goal_spinbox.grid(row=self.row, column=self._goal_column)
        self.columns_spinbox.grid(row=self.row, column=self._columns_column)
        self.rows_spinbox.grid(row=self.row, column=self._rows_column)

    def destroy(self):
        self.checkers_spinbox.grid_forget()
        self.goal_spinbox.grid_forget()
        self.columns_spinbox.grid_forget()
        self.rows_spinbox.grid_forget()
        del self

    @property
    def goal(self):
        return self.goal_spinbox.get()

    @property
    def checkers(self):
        return self.checkers_spinbox.get()

    @property
    def columns(self):
        return self.columns_spinbox.get()

    @property
    def rows(self):
        return self.rows_spinbox.get()


# Frames
class FieldFrame:
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
        self.app.clear()


class MenuFrame:
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
        self.frame._draw = draw_button
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
        self.app.set_goal(self.goal_var.get())
        self.app.coordinates = self.coordinates_var.get()
        self.app.field._draw(
            columns=self.columns_var.get(),
            rows=self.rows_var.get(),
            checkers=self.checkers_var.get(),
        )
        # Show hidden buttons
        self.frame.save.pack(side=tk.BOTTOM)
        self.frame.reset.pack(side=tk.BOTTOM)
        self.frame.points.pack(side=tk.BOTTOM)
        self.frame.checkers_used.pack(side=tk.BOTTOM)
        self.frame._draw.configure(text='Redraw')

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
        self.app.save()

    def update_chackers_used_label(self):
        self.frame.checkers_used.configure(text='Checkers used: {}'.format(
            len(self.app.checkers_used_list)
        ))

    def update_points_label(self):
        self.frame.points.configure(text='Points: {}'.format(
            self.app.points
        ))


class SettingsFrame:

    _width = 60

    _button_column = 0
    _checkers_column = CHECKERS_COLUMN
    _goal_column = GOAL_COLUMN
    _columns_column = COLUMNS_COLUMN
    _rows_column = ROWS_COLUMN
    _start_row = 8
    _start_column_span = 5

    _max_stages = 7

    def __init__(self, frame):
        self.frame = frame
        # variables
        self.game_settings = []
        self.stages = []
        self.del_buttons = [None, ]
        # draw
        self.draw()

    def draw(self):
        # configure frame
        self.frame.title('Game settings')
        # define widgets
        start_button = tk.Button(self.frame, text='Start',
                                 width=self._width,
                                 command=self.start)
        add_new_stage_button = tk.Button(self.frame, text='Add new stage',
                                         command=self.add_new_stage)
        checkers_label = tk.Label(self.frame, text='Checkers')
        goal_label = tk.Label(self.frame, text='Goal')
        columns_label = tk.Label(self.frame, text='Columns')
        rows_label = tk.Label(self.frame, text='Rows')
        # pack
        start_button.grid(column=0, row=self._start_row,
                          columnspan=self._start_column_span)
        add_new_stage_button.grid(column=self._button_column, row=0)
        checkers_label.grid(column=self._checkers_column, row=0)
        goal_label.grid(column=self._goal_column, row=0)
        columns_label.grid(column=self._columns_column, row=0)
        rows_label.grid(column=self._rows_column, row=0)
        # add first row
        self.add_new_stage(is_first=True)

    def start(self):
        pass

    def add_new_stage(self, is_first=False):
        number = len(self.stages)
        row = number + 1
        if len(self.stages) != self._max_stages:
            self._add_new_stage(row)
        if not is_first:
            self._add_del_button(row, number)

    def _add_new_stage(self, row):
        stage = Stage(self.frame, row=row)
        self.stages.append(stage)

    def _add_del_button(self, row, number):
        del_button = tk.Button(
            self.frame,
            text='delete',
            command=self.destroy_stage(number)
        )
        del_button.grid(column=self._button_column, row=row)
        self.del_buttons.append(del_button)

    def _destroy_del_button(self, number: int):
        self.del_buttons[number].grid_forget()

    def destroy_stage(self, number: int):
        def wrapped():
            self.stages[number].destroy()
            self._destroy_del_button(number)
        return wrapped


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
        self._define_field_frame()
        self._define_frames()
        self._define_common_variables()
        self._define_variables()

    def _define_frames(self):
        raise NotImplementedError()

    def _define_field_frame(self):
        self.field_frame = tk.Frame(self.master)
        self.field_frame.pack(side=tk.LEFT)
        self.field = FieldFrame(self, self.field_frame)

    def _define_common_variables(self):
        self.checkers = None
        self.rows = None
        self.columns = None
        self.goal = None
        self.coordinates = None
        self.checkers_used_list = []
        self.points = 0

    def _define_variables(self):
        return NotImplementedError()

    def set_goal(self, goal: int):
        self.goal = goal

    def can_put(self):
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

    def _calculate(self):
        return algo.calculate(self.checkers_used_list, self.goal)


class SingleApp(App):

    def _define_frames(self):
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(side=tk.RIGHT)
        self.menu = MenuFrame(self, self.menu_frame)

    def _define_variables(self):
        pass

    def save_dialog(self):
        return tksd.askstring(title='Saving',
                              prompt='You have {} points.\nEnter the name.'.format(
                                  self.points
                              ))

    def save(self):
        lg.team_lg.info('Name: "{name}" Points: {points} Checkers: {checkers}'.format(
            name=self.save_dialog(),
            points=self.points,
            checkers=self.checkers_used_list,
        ))


class OlympApp(App):
    """ Application for usage in olympiads. """

    def _define_frames(self):
        self._define_field_frame()
        # define Settings TopLevel
        self.settings_frame = tk.Toplevel(self.master)
        self.setting = SettingsFrame(self.settings_frame)

    def _define_variables(self):
        pass


# main
def launch_single():
    root = tk.Tk()
    SingleApp(root)
    root.mainloop()


def launch_olymp():
    root = tk.Tk()
    OlympApp(root)
    root.mainloop()
