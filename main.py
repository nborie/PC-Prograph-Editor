#!/usr/bin/python3

"""
This module implement a small graphical application with tkinter to 
manipulate finite triangulations of the sphere build by hand.
"""
#*****************************************************************************
#  Copyright (C) 2021 Nicolas Borie <nicolas dot borie at univ-eiffel . fr>
#
#  Distributed under the terms of Creative Commons Attribution-ShareAlike 3.0
#  Creative Commons CC-by-SA 3.0
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  The full text of the CC-By-SA 3.0 is available at:
#
#            https://creativecommons.org/licenses/by-sa/3.0/
#            https://creativecommons.org/licenses/by-sa/3.0/fr/
#*****************************************************************************

import sys
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from enum import Enum

from SYT3lines import SYT3lines
from triangulation import Triangulation

class StatusAction(Enum):
    """
    A class whose instances model the different status of the application.
    """
    WAIT_ACTION = 1                 # Normal Status
    WAIT_NEW_POINT = 2              # Add a point in the triangulation
    WAIT_SELECT_POINT = 3           # Select a point in the triangulation
    WAIT_NEW_POINT_POSITION = 4     # Click a new position for a selected point
    WAIT_SELECT_EDGE = 5            # Select an edge in the triangulation
    WAIT_EDGE_ACTION = 6            # Flip down or up the selected edge

#####################################################################
#                       TKINTER APPLICATION                         #
#####################################################################
class prographApp():
    def __init__(self, size_x=None, size_y=None):
        """
        Initialize the small graphical application to build, manipulate and 
        view PC prograph.
        """
        self._ws = tk.Tk()
        if size_x is None:
            self.screen_width = self._ws.winfo_screenwidth()
        else:
            self.screen_width = int(size_x)
        if size_y is None:
            self.screen_height = self._ws.winfo_screenheight()
        else:
            self.screen_height = int(size_y)
        self._ws.geometry( str(self.screen_width) + 'x' + str(self.screen_height) )
        self._ws.title("Product-Coproduct Prograph Viewer Editor")
        self._canvas_size = ((self.screen_width//2)-13, self.screen_height-250)
        self._message = tk.StringVar()
        self._message.set("Message : waiting for a new action...")
        self._syt = tk.StringVar()
        self._syt.set(str(SYT3lines([[3],[2],[1]])))
        self._triangulation = Triangulation(*self._canvas_size)
        self._canvas = None
        self._dual_canvas = None
        self._status_action = StatusAction.WAIT_ACTION
        self._index_selected_point = None
        self._selected_edge = None
        self._button_flip_up = None
        self._button_flip_down = None
        self._overlay_active = False

    def window(self):
        """
        Return the main and actually unique windows of the application.
        """
        return self._ws

    def window_size(self):
        """
        Return the size of the 
        """
        return (self.window().winfo_screenwidth(), 
                self.window().winfo_screenheight())

    def canvas_size(self):
        """
        Return the size of the two canvas.
        """
        return self._canvas_size

    def message(self):
        """
        Return the current message from the application to the user.
        """
        return self._message

    def set_message(self):
        """
        Set the application's message for the user according the status
        of the waited action.
        """
        if self._status_action is StatusAction.WAIT_ACTION:
            self._message.set("Message : waiting for a new action...")
        elif self._status_action is StatusAction.WAIT_NEW_POINT:
            self._message.set("Message : waiting for a new point in the triangulation.")
        elif self._status_action is StatusAction.WAIT_SELECT_POINT:
            self._message.set("Message : select a point in the triangulation.")
        elif self._status_action is StatusAction.WAIT_NEW_POINT_POSITION:
            self._message.set("Message : select a new position for the point.")
        elif self._status_action is StatusAction.WAIT_SELECT_EDGE:
            self._message.set("Message : select an edge in the triangulation.")
        elif self._status_action is StatusAction.WAIT_EDGE_ACTION:
            self._message.set("Message : select a flip action for the edge.")
        else:
            self._message.set("Message : incoherent status... Restart the application.")
        self._overlay_active = False

    def triangulation(self):
        """
        Return the current triangulation in the application.
        """
        return self._triangulation

    def add_message(self):
        """
        Add a mini frame just for the message
        """
        self._frame_message = tk.Frame(self.window(), padx=5, pady=5, 
                                   bg='gray85', 
                                   width=(self.window_size()[0]//2)-15)
        self._frame_message.grid(row=0, column=1, sticky="ns")
        tk.Label(self._frame_message, textvariable=self._message, font='Helvetica 12 bold').pack()

    def add_menu(self):
        """
        Add a menu frame to `self`.
        """
        self._frame_menu = tk.Frame(self.window(), padx=5, pady=5, 
                                   bg='gray85', 
                                   width=(self.window_size()[0]//2)-15)
        self._frame_menu.grid(row=1, column=1, sticky="ns")
        tk.Button(self._frame_menu, text='Reset', 
               command = lambda:self.reset_action()).grid(row=0, column=1, 
                                                          padx=5, pady=5)
        tk.Button(self._frame_menu, text='Add point', 
               command = lambda:self.add_point_action()).grid(row=0, column=2, 
                                                              padx=5, pady=5)
        tk.Button(self._frame_menu, text='Move point', 
               command = lambda:self.move_point_action()).grid(row=0, column=3, 
                                                               padx=5, pady=5)
        tk.Button(self._frame_menu, text='Overlay dual', 
               command = lambda:self.overlay_dual()).grid(row=0, column=4, 
                                                               padx=5, pady=5)
        tk.Button(self._frame_menu, text='Schützenberger', 
               command = lambda:self.schutzenberger_involution()).grid(row=0, column=5, 
                                                               padx=5, pady=5)
        tk.Button(self._frame_menu, text='Select edge', 
               command = lambda:self.select_edge_action()).grid(row=1, column=1, 
                                                                padx=5, pady=5)
        self._button_flip_up = tk.Button(self._frame_menu, 
                                        text='Flip up', 
                                        background='gray30')
        self._button_flip_up.grid(row=1, column=2, padx=5, pady=5)
        self._button_flip_down = tk.Button(self._frame_menu, 
                                           text='Flip down', 
                                           background='gray30', 
                                           command=lambda: self.flip_down_action())
        self._button_flip_down.grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self._frame_menu, text='Exit', 
                  command = self.window().destroy).grid(row=1, column=4, 
                                                        padx=5, pady=5)
        tk.Button(self._frame_menu, text='Doc/Help/About', 
                  command = lambda:self.about()).grid(row=1, column=5, 
                                                        padx=5, pady=5)

    def add_young_tableau(self):
        """
        Add a 3 line Standard Young Tableau frame for the current PC prograph.
        """
        self._frame_syt = tk.Frame(self.window(), padx=5, pady=5, 
                                   width=(self.window_size()[0]//2)-15)
        self._frame_syt.grid(row=0, rowspan=2, column=2)
        tk.Label(self._frame_syt, textvariable=self._syt, 
                 font='Courier 12 bold').pack()

    def add_canvas_triangulation(self):
        """
        Add a canvas on the triangulation side action.
        """
        color = 'white'
        self._frame_cane = tk.Frame(self.window(), padx=5, pady=5, bg=color)
        self._frame_cane.grid(row=2, column=1)
        tk.Label(self._frame_cane, text="Triangulation of the sphere", bg=color).pack()
        canva = tk.Canvas(self._frame_cane, width=self.canvas_size()[0], 
                          height=self.canvas_size()[1], bg=color)
        self.triangulation().draw_all(canva)
        canva.pack()
        canva.bind("<Button-1>", lambda x: self.wait_click(x, canva))
        # Register one for all the canvas for triangulation
        self._canvas = canva

    def add_canevas_prograph(self):
        """
        Add a canvas on the PC prograph side.
        """
        color = 'white'
        self._frame_gen = tk.Frame(self.window(), padx=5, pady=5, bg=color)
        self._frame_gen.grid(row=2, column=2)
        tk.Label(self._frame_gen, text="Product Coproduct Prograph", 
                 bg=color).pack()
        canva = tk.Canvas(self._frame_gen, width=self.canvas_size()[0], 
                          height=self.canvas_size()[1], bg=color)
        self.triangulation().draw_all_dual(canva)
        canva.pack()
        # Register one for all the canvas for prograph
        self._dual_canvas = canva

    def wait_click(self, event, canvas):
        """
        This method binded to the left click of mouse by tkinter deal
        with each left click on the triangulation according the user
        intentions.
        """
        x, y = event.x, event.y
        if self._status_action is StatusAction.WAIT_NEW_POINT:
            self.triangulation().add_point(x, y, canvas)
            ans = self.triangulation().to_standard_young_tableau()
            self._syt.set(str(SYT3lines(ans)))
            self.triangulation().draw_all_dual(self._dual_canvas)
            self._status_action = StatusAction.WAIT_ACTION
        elif self._status_action is StatusAction.WAIT_SELECT_POINT:
            self._index_selected_point = self.triangulation().find_closest_point(x, y)
            self.triangulation().draw_selected_point(self._index_selected_point, self._canvas)
            self._status_action = StatusAction.WAIT_NEW_POINT_POSITION
        elif self._status_action is StatusAction.WAIT_NEW_POINT_POSITION:
            self.triangulation().points[self._index_selected_point] = [x, y]
            self.triangulation().update_dual_points()
            self._index_selected_point = None
            self.triangulation().draw_all_dual(self._dual_canvas)
            self.triangulation().draw_all(self._canvas)
            self._status_action = StatusAction.WAIT_ACTION
        elif self._status_action is StatusAction.WAIT_SELECT_EDGE:
            o, e = self.triangulation().find_closest_edge(x, y)
            self._selected_edge = (o, e)
            self.triangulation().draw_all(self._canvas)
            self.triangulation().draw_selected_edge(o, e, self._canvas)
            self.triangulation().draw_edges(self._canvas)
            self.triangulation().draw_edges_orientation(self._canvas)
            self.triangulation().draw_points(self._canvas)
            self._status_action = StatusAction.WAIT_EDGE_ACTION
            # time to customize buttons if flipable up or down
            if self.triangulation().is_flipable_down(o, e):
                self._button_flip_down.configure(background='yellow')
            if self.triangulation().is_flipable_up(o, e):
                self._button_flip_up.configure(background='sea green')
        self.set_message()
        return(x, y)
    
    def reset_action(self):
        """
        Manage a click on the reset button. The action consist in
        overwriting triangulation by a fresh new one.
        """
        sizex, sizey = self.canvas_size()
        self._triangulation = Triangulation(sizex, sizey)
        self._triangulation.draw_all(self._canvas)
        self._triangulation.draw_all_dual(self._dual_canvas)
        self._syt.set(str(SYT3lines([[3],[2],[1]])))
        self._index_selected_point = None
        self._selected_edge = None
        self._button_flip_down.configure(background='gray30')
        self._button_flip_up.configure(background='gray30')
        self._status_action = StatusAction.WAIT_ACTION

    def add_point_action(self):
        """
        Manage a click on the add point button.
        """
        if self._status_action is StatusAction.WAIT_ACTION:
            self._status_action = StatusAction.WAIT_NEW_POINT
        elif self._status_action is StatusAction.WAIT_NEW_POINT:
            self._status_action = StatusAction.WAIT_ACTION
        self.set_message()

    def move_point_action(self):
        """
        Manage a click on the move point button.
        """
        if self._status_action is StatusAction.WAIT_ACTION:
            self._status_action = StatusAction.WAIT_SELECT_POINT
        elif self._status_action is StatusAction.WAIT_SELECT_POINT:
            self._status_action = StatusAction.WAIT_ACTION
        self.set_message()

    def overlay_dual(self):
        """
        Draw the dual graph over the triangulation.
        """
        if self._overlay_active:
            self._canvas.delete('all')
            self.triangulation().draw_all(self._canvas)
            self._overlay_active = False
        else:
            self.triangulation().draw_edge_dual(self._canvas)
            self.triangulation().draw_operators(self._canvas)
            self._overlay_active = True
    
    def schutzenberger_involution(self):
        """
        Apply the Schützenberger involution on the triangulation, 
        the dual and the Standard Young Tableau
        """
        self.triangulation().schutzenberger_involution()
        ans = self.triangulation().to_standard_young_tableau()
        self._syt.set(str(SYT3lines(ans)))
        self._triangulation.draw_all(self._canvas)
        self._triangulation.draw_all_dual(self._dual_canvas)

    def select_edge_action(self):
        """
        Manage a click on the add point button.
        """
        if self._status_action is StatusAction.WAIT_ACTION:
            self._status_action = StatusAction.WAIT_SELECT_EDGE
            self.triangulation().draw_middle_edge(self._canvas)
        elif self._status_action is StatusAction.WAIT_SELECT_EDGE or self._status_action is StatusAction.WAIT_EDGE_ACTION:
            self._status_action = StatusAction.WAIT_ACTION
            self._selected_edge = None
            self.triangulation().draw_all(self._canvas)
        self._button_flip_down.configure(background='gray30')
        self._button_flip_up.configure(background='gray30')
        self.set_message()

    def launch(self):
        """
        Add all graphic element in the main window then launch the 
        application by triggering the main loop.
        """
        # We first add all graphic elements
        self.add_message()
        self.add_menu()
        self.add_young_tableau()
        self.add_canvas_triangulation()
        self.add_canevas_prograph()
        # Then trigger main loop
        self.window().mainloop()

    def about(self):
        """
        Open a new windows with the Doc / Help / About this application.
        """
        new_win = tk.Toplevel(self._ws)
        new_win.title("About the P-C Prograph Viewer Editor")
        new_win.geometry("1200x800")
        img=ImageTk.PhotoImage(file="IMG/LIGM-RVB-couleurs-72dpi.png")
        img2=ImageTk.PhotoImage(file="IMG/logo_univ_gustave_eiffel_rvb.png")
        img3=ImageTk.PhotoImage(file="IMG/Esiee_Paris_small.png")
        label = tk.Label(new_win, image=img)
        label2 = tk.Label(new_win, image=img2)
        label3 = tk.Label(new_win, image=img3)
        label.image=img
        label2.image=img2
        label3.image=img3
        label.grid(row=0, column=0, padx=20)
        label2.grid(row=0, column=1, padx=20)
        label3.grid(row=0, column=2, padx=20)
        tk.Label(new_win, text="Welcome on the PC Prograph Viewer Editor",
                 font=('Helvetica', '24', 'bold italic')).grid(row=1, column=0, columnspan=3)
        long_text="""A small application that will help you to understand the bijection 
        between triangulations of the sphere and Product Coproduct prographs.
        By Nicolas Borie (<nicolas dot borie at univ-eiffel redot fr>)."""
        tk.Label(new_win, text=long_text).grid(row=2, column=0, columnspan=3)
        tk.Label(new_win, text="Last version of sources",
                 font=('Helvetica', '24', 'bold italic')).grid(row=3, column=0, columnspan=3)
        long_text="""To get the last version of sources, you should go to the github
        repository : https://github.com/nborie/PC-Prograph-Editor"""
        tk.Label(new_win, text=long_text).grid(row=4, column=0, columnspan=3)
        tk.Label(new_win, text="Documentation",
                 font=('Helvetica', '24', 'bold italic')).grid(row=5, column=0, columnspan=3)
        long_text="""Most of the documentation is available online here 
        https://github.com/nborie/PC-Prograph-Editor#readme"""
        tk.Label(new_win, text=long_text).grid(row=6, column=0, columnspan=3)
        tk.Label(new_win, text="References",
                 font=('Helvetica', '24', 'bold italic')).grid(row=7, column=0, columnspan=3)
        # long_text="""TODO references..."""
        # tk.Label(new_win, text=long_text).grid(row=8, column=0, columnspan=3)
        def callback_url(url):
            webbrowser.open_new(url)
        long_text="""Three-dimensional Catalan numbers and product-coproduct prographs"""
        article1 = tk.Label(new_win, text=long_text, fg="blue", cursor="hand2")
        article1.grid(row=9, column=0, columnspan=3)
        article1.bind("<Button-1>", lambda e: callback_url("https://arxiv.org/abs/1704.00212"))
        long_text="""Product-Coproduct Prographs and Triangulations of the Sphere"""
        article2 = tk.Label(new_win, text=long_text, fg="blue", cursor="hand2")
        article2.grid(row=10, column=0, columnspan=3)
        article2.bind("<Button-1>", lambda e: callback_url("https://arxiv.org/abs/2202.05757"))


#####################################################################
#                SET AND LAUNCH THE APPLICATION                     #
#####################################################################

# Here is the programm. The windows sizes are set to use the
# whole screen unless user has specifyed a size
if __name__ == "__main__":
    size_x = None
    size_y = None
    args_list = sys.argv[1:]
    if len(args_list) >= 2:
        size_x = args_list[0]
        size_y = args_list[1]
    App = prographApp(size_x=size_x, size_y=size_y)
    App.launch()

