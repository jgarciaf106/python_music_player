import random
import os
import time
import math

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from tkinter import ttk, font
from tkinter import *
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk


class Music_Player:

    # constructor
    def __init__(self, title):
        # player settings
        # player gui
        self.root = Tk()

        # title of the window
        self.root.title(title)

        # title icon
        self.root.iconbitmap(
            r"C:\Users\jgarc\OneDrive\Escritorio\Python\tarea_programada\py_music_player\src\assets\sound.ico"
        )

        # window dimension and position

        ## removes the maximize button
        self.root.resizable(0, 0)

        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")

        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family="Segoe UI", size=10, weight=font.BOLD)

        ## music player wigth and height
        self.window_width = 375
        self.window_height = 715

        # backend music
        pygame.init()

        # inite pygame mixer
        pygame.mixer.init()

        # interface
        self.canvas = Canvas(
            self.root,
            bg="#0A0A0A",
            height=715,
            width=375,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.prev_button = ImageTk.PhotoImage(
            Image.open("./src/assets/boton-de-previous.png").resize((37, 37))
        )
        self.play_button = ImageTk.PhotoImage(
            Image.open("./src/assets/boton-de-play.png").resize((37, 37))
        )
        self.pause_button = ImageTk.PhotoImage(
            Image.open("./src/assets/boton-de-pause.png").resize((37, 37))
        )
        self.resume_button = ImageTk.PhotoImage(
            Image.open("./src/assets/boton-de-resume.png").resize((37, 37))
        )
        self.next_button = ImageTk.PhotoImage(
            Image.open("./src/assets/boton-de-next.png").resize((37, 37))
        )
        self.open_track = ImageTk.PhotoImage(
            Image.open("./src/assets/song.png").resize((25, 25))
        )
        self.open_tracks = ImageTk.PhotoImage(
            Image.open("./src/assets/folder.png").resize((25, 25))
        )
        self.volume_up = ImageTk.PhotoImage(
            Image.open("./src/assets/plus.png").resize((25, 25))
        )
        self.volume_down = ImageTk.PhotoImage(
            Image.open("./src/assets/minus.png").resize((25, 25))
        )

        # Player information
        self.sleep_secs = 1
        self.player_name = title
        self.song_volume = 100
        self.volume = 1
        self.song_length = "00:00:00"
        self.music_progress = 0
        self.song_progress = "00:00:00"
        self.playing_status = "Not Playing"
        self.index_song = 0
        self.song_name = ""
        self.song_names = []

    # player functionalities
    def open_music_track(self):
        # self.root.withdraw()
        self.song_name = filedialog.askopenfilename()
        self.playing_status = "Playing"
        self.play_song()

    def open_music_tracks(self):

        folder_name = filedialog.askdirectory()
        song_names = []

        # get files from directory
        for file in os.listdir(folder_name):
            if file.endswith(".mp3"):
                song_names.append(folder_name + "/" + file)
        self.song_names = song_names
        self.play_list()

    def playing_song_ticker(self):

        song_name = self.song_name.split("/")[-1].split(".")[0]

        text_display_space = " " * 15
        playing = text_display_space + "Reproduciendo: " + song_name + text_display_space

        for char in range(len(playing)):
            # use string slicing to do the trick
            ticker_text = playing[char : char + 20]
            self.canvas.itemconfig(self.name, text=ticker_text)
            self.root.update()
            # delay by 0.15 seconds
            time.sleep(0.15)

    def set_time_progress(self):
        # song name
        song_name = self.song_name.split("/")[-1].split(".")[0]

        # start playing time
        start = time.time()

        # get music file
        song = pygame.mixer.Sound(self.song_name)

        # get music file length
        song_length_secs = song.get_length()
        progress_move = 100 / song_length_secs

        # time formatting
        song_length = time.strftime("%H:%M:%S", time.gmtime(song_length_secs))

        # update tkinter labels
        self.canvas.itemconfig(self.lenght, text=song_length)
        # loop start
        i=0
        counting = True
        while counting:
            # current playing time
            end = time.time()

            # elapsed playing time
            seconds_elapsed = end - start

            # get current played time
            played_time = pygame.mixer.music.get_pos() / 1000

            # format played time
            song_progress = time.strftime("%H:%M:%S", time.gmtime(played_time))

            # update played time labels
            self.canvas.itemconfig(self.playing, text=song_progress)

            # update song progress on bar
            self.progress_bar.step(progress_move)

            # display scolling label
            text_display_space = " " * 10
            playing = text_display_space  + "Reproduciendo: " + song_name + text_display_space
            
            # playing text message
            l = len(playing)
            # use string slicing to do the trick
            ticker_text = playing[i : i + 10]
            self.canvas.itemconfig(self.name, text=ticker_text)


            if i < l:
                i += 1
            else:
                i = 0
            

            time.sleep(self.sleep_secs)

            if seconds_elapsed > song_length_secs:
                counting = False

            self.root.update()
            
        # reset bar and labels
        self.progress_bar.stop()
        self.canvas.itemconfig(self.playing, text=self.song_progress)
        self.canvas.itemconfig(self.name, text="")

    def play_song(self):

        # load next song
        pygame.mixer.music.load(self.song_name)

        # update play button to pause icon
        self.pl_music_btn.configure(image=self.pause_button)

        # music starts playing
        pygame.mixer.music.play()
        
        # update playing progress
        self.set_time_progress()

        time.sleep(1)

    def play_list(self):
        # Playing the songs in the background
        playing = True
        while playing:
            if self.index_song <= len(self.song_names) - 1:
                self.song_name = self.song_names[self.index_song]
                self.play_song()
                self.index_song += 1
            else:
                playing = False

    def stop_music(self):
        self.playing_status = "Not Playing"
        pygame.mixer.music.stop()

    def pause_music(self):
        self.canvas.itemconfig(self.player, text="Reproducion Pausada")
        pygame.mixer.music.pause()
        self.playing_status = "Paused"
        self.pl_music_btn.configure(image=self.resume_button)
        self.sleep_secs = 86400

    def resume_music(self):
        self.canvas.itemconfig(self.player, text="Reproduciendo")
        pygame.mixer.music.unpause()
        self.playing_status = "Playing"
        self.pl_music_btn.configure(image=self.pause_button)
        self.sleep_secs = 1

    def set_playing_status(self):
        if self.playing_status == "Playing":
            self.pause_music()
        elif self.playing_status == "Paused":
            self.resume_music()

    def set_volume_down(self):

        if self.volume > 0 and self.song_volume > 0:
            self.volume -= 0.1
            self.song_volume -= 10
            self.canvas.itemconfig(self.volume_label, text=str(self.song_volume) + "%")
            pygame.mixer.music.set_volume(self.volume)

    def set_volume_up(self):

        if self.volume < 1 and self.song_volume <= 100:
            self.volume += 0.1
            self.song_volume += 10
            self.canvas.itemconfig(self.volume_label, text=str(self.song_volume) + "%")
            pygame.mixer.music.set_volume(self.volume)

    def screen_display(self):
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # center screen
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # display screen dimensions
        self.root.geometry(
            f"{self.window_width}x{self.window_height - 30}+{center_x}+{center_y}"
        )

        self.canvas.place(x=0, y=0)

        # volume label
        self.volume_label = self.canvas.create_text(
            300,
            450,
            anchor="nw",
            text=str(self.song_volume) + "%",
            fill="#FFFFFF",
            font=("Segoe UI", 13 * -1),
        )

        # now playing
        self.player = self.canvas.create_text(
            127.0,
            34.240234375,
            anchor="nw",
            text=self.player_name,
            fill="#FFFFFF",
            font=("Segoe UI", 20 * -1),
        )

        # song name
        self.name = self.canvas.create_text(
            155.0,
            425,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            font=("Segoe UI", 20 * -1),
        )

        # song playing time
        self.playing = self.canvas.create_text(
            30.0,
            576.2227172851562,
            anchor="nw",
            text=self.song_progress,
            fill="#FFFFFF",
            font=("Segoe UI", 12 * -1),
        )

        # song length
        self.lenght = self.canvas.create_text(
            311.00048828125,
            576.2227172851562,
            anchor="nw",
            text=self.song_length,
            fill="#FFFFFF",
            font=("Segoe UI", 12 * -1),
        )

        s = ttk.Style()
        s.theme_use("clam")
        s.configure(
            "red.Horizontal.TProgressbar", foreground="black", background="black"
        )
        self.progress_bar = ttk.Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate",
            length=315,
            style="red.Horizontal.TProgressbar",
        )

        # place the progressbar
        self.progress_bar.grid(column=0, row=0, columnspan=2, padx=30, pady=545)

        # music controls prev
        prev_music_btn = Button(
            self.root,
            command=self.open_music_track,
            borderwidth=1,
            image=self.prev_button,
            bg="#0A0A0A",
        )
        prev_music_btn.place(x=100, y=619, height=45, width=50)

        # music controls play/plause
        self.pl_music_btn = Button(
            self.root,
            command=self.set_playing_status,
            borderwidth=1,
            image=self.play_button,
            bg="#0A0A0A",
        )
        self.pl_music_btn.place(x=161, y=619, height=45, width=50)

        # music controls next
        next_music_btn = Button(
            self.root,
            command=self.open_music_track,
            image=self.next_button,
            borderwidth=1,
            bg="#0A0A0A",
        )
        next_music_btn.place(x=221, y=619, height=45, width=50)

        # volume control
        volume_up_btn = Button(
            self.root,
            command=self.set_volume_up,
            borderwidth=1,
            image=self.volume_up,
            bg="#0A0A0A",
        )
        volume_up_btn.place(x=320, y=470, height=32, width=35)

        volume_down_btn = Button(
            self.root,
            command=self.set_volume_down,
            borderwidth=1,
            image=self.volume_down,
            bg="#0A0A0A",
        )
        volume_down_btn.place(x=280, y=470, height=32, width=35)

        # actions button open song/songs
        open_track_btn = Button(
            self.root,
            command=self.open_music_track,
            borderwidth=1,
            image=self.open_track,
            bg="#0A0A0A",
        )
        open_track_btn.place(x=27, y=470, height=32, width=35)

        # actions button open song/songs
        open_tracks_btn = Button(
            self.root,
            command=self.open_music_tracks,
            borderwidth=1,
            image=self.open_tracks,
            bg="#0A0A0A",
        )
        open_tracks_btn.place(x=68, y=470, height=32, width=35)

        # song equailizer
        self.canvas.create_rectangle(
            27.0, 100.0, 354.0, 379.0, fill="#FFFFFF", outline=""
        )

        # display app
        self.root.mainloop()

    def launch_player(self):
        self.screen_display()
