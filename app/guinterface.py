""" This module contains all GUI needs. """
from tkinter import *
from settings import *
from .algo import calculate


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
        pass

    def draw_field(self):
        print('Drawing field...')

    def clear_field(self):
        print('Clearing field...')

    def calculate(self):
        print('Calculating...')


# main
def launch_gui():
    root = Tk()
    app = GUI(root)
    root.mainloop()
