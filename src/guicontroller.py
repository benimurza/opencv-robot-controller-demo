import cv2
import tkinter as tk
from PIL import Image
# Set up GUI
from PIL import ImageTk
import logging

logger = logging.getLogger("GuiController")

class GuiController:

    def __init__(self):
        self.window = tk.Tk()  # Makes main window
        self.window.attributes("-fullscreen", True)
        # Not important, since game is played in full screen
        self.window.wm_title("CS1: Dornbirn")

        # Black background
        self.window.config(background="#000000")

        # Graphics window
        self.imageFrame = tk.Frame(self.window, width=600, height=500)
        self.imageFrame.config(background="#2aff00")
        self.imageFrame.grid(row=0, column=0, padx=10, pady=2)

        # Capture video frames
        self.main_label = tk.Label(self.imageFrame)
        self.main_label.config(background="#2aff00")
        self.main_label.grid(row=0, column=0)

        self.console_window_frame = tk.Frame(self.window, bg="#000000", width=600, height=500)
        self.console_window_frame.grid(row=0, column=1, padx=10, pady=2)
        self.console_window_frame.columnconfigure(1, weight=1)
        self.text_frame = tk.Text(self.console_window_frame, height=40, width=60, bg="#000000", fg="#2aff00")
        self.text_frame.grid(row=1, column=0)

        # Some text for show
        self.text_frame.insert(tk.END, "Logging in...\n")
        self.text_frame.insert(tk.END, "User:     CS1DORNBIRN\n")
        self.text_frame.insert(tk.END, "Password: ***********\n")
        self.text_frame.insert(tk.END, "Logged in.\n")

        # Disable any text input by default
        self.text_frame.configure(state="disabled")
        self.input_frame = tk.Frame(self.console_window_frame, bg="#000000")
        self.input_frame.grid(row=2, column=0)
        self.input_label = tk.Label(self.input_frame, text="Console: ", bg="#000000", fg="#2aff00")
        self.input_label.grid(row=0, column=0)
        self.entry_frame = tk.Entry(self.input_frame, bg="#000000", fg="#2aff00")
        self.entry_frame.grid(row=0, column=1)
        self.entry_frame.bind('<Return>', self.enter_callback)

        self.has_game_started = False
        self.window.bind('p', self.game_start_callback)

        # External callbacks
        self.callback_enter_pressed = None
        self.callback_game_begin = None

    def game_start_callback(self, event=None):
        if not self.has_game_started:
            if self.callback_game_begin is not None:
                self.has_game_started = True
                self.write_text_in_console_box("Police chase starting.")
                self.callback_game_begin()
            else:
                logger.error("Game was started but no callback for game start!")

    def write_text_in_console_box(self, text):
        # Enable input
        self.text_frame.configure(state="normal")
        self.text_frame.insert(tk.END, text + "\n")
        # Auto-scroll down
        self.text_frame.see('end')
        # Disable again
        self.text_frame.configure(state="disabled")

    # Callback when enter pressed (update console textbox). Must have 2 arguments.
    def enter_callback(self, event=None):
        text = self.entry_frame.get()
        if text != "":
            # Callback
            if self.callback_enter_pressed is not None:
                self.write_text_in_console_box(self.callback_enter_pressed(text)[1])

            # Clear input box
            self.entry_frame.delete(0, 'end')

    # Helper function to get set TkInter image in GUI from an opencv frame
    def set_frame_in_gui(self, opencv_frame):
        frame_copy = opencv_frame.copy()
        frame_copy = cv2.resize(frame_copy, None, fx=1, fy=1)
        cv2image = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.main_label.imgtk = imgtk
        self.main_label.configure(image=imgtk)

    def update_gui(self, opencv_frame):
        self.set_frame_in_gui(opencv_frame)
        self.window.update_idletasks()
        self.window.update()


'''
# Quick example usage
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
gc = GuiController()
while True:
    _, frame = cap.read()
    gc.update_gui(frame)
'''
