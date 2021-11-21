import random
import os
import time
import random

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from tkinter import ttk, font, filedialog, messagebox
from tkinter import *
from tkinter.tix import *
from PIL import Image, ImageTk


class Music_Player:

    # constructor
    def __init__(self, title):
        # player settings
        # player gui
        """
        constructor of the class and initializes the player
        set self variables to be used in the class
        Parameters
        ----------
        title : str
            The music player title
        """
        self.root = Tk()

        # title of the window
        self.root.title(title)

        # title icon
        self.root.iconbitmap(
            r".\src\assets\sound.ico"
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
        # Create a tooltip
        self.tip = Balloon(self.root)

        self.prev_button = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\boton-de-previous.png"
            ).resize((37, 37))
        )
        self.play_button = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\boton-de-play.png"
            ).resize((37, 37))
        )
        self.pause_button = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\boton-de-pause.png"
            ).resize((37, 37))
        )
        self.resume_button = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\boton-de-resume.png"
            ).resize((37, 37))
        )
        self.next_button = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\boton-de-next.png"
            ).resize((37, 37))
        )
        self.open_track = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\song.png"
            ).resize((25, 25))
        )
        self.open_tracks = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\folder.png"
            ).resize((25, 25))
        )
        self.volume_up = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\plus.png"
            ).resize((25, 25))
        )
        self.volume_down = ImageTk.PhotoImage(
            Image.open(
                r".\src\assets\minus.png"
            ).resize((25, 25))
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
        self.button_state = DISABLED
        self.color_list = [
            "#ED003C",
            "#3a7013",
            "#142341",
            "#15717D",
            "#F36633",
            "#BC1077",
            "#544f40",
        ]

    # player functionalities
    def open_music_track(self):
        """
        Opens a file dialog to select a music file
        Calls the play_music function
        Parameters
        ----------
        None
        """

        # self.root.withdraw()
        self.song_name = filedialog.askopenfilename()
        while self.song_name == "":
            response = messagebox.askquestion(
                "No file selected", "Are you sure you want to open the song?"
            )
            if response == "yes":
                self.song_name = filedialog.askopenfilename()
            else:
                return
        self.playing_status = "Playing"
        # update song number
        self.canvas.itemconfig(self.song_number, text="1/1")
        self.play_song()

    def open_music_tracks(self):
        """
        Open a file dialog to select multiple music files
        Calls the play_music function
        Parameters
        ----------
        None
        """
        folder_name = filedialog.askdirectory()

        while folder_name == "":
            response = messagebox.askquestion(
                "No folder selected", "Are you sure you want to open the play list?"
            )
            if response == "yes":
                folder_name = filedialog.askdirectory()
            else:
                return

        song_names = []

        # get files from directory
        for file in os.listdir(folder_name):
            if file.endswith(".mp3"):
                song_names.append(folder_name + "/" + file)
        self.song_names = song_names
        self.playing_status = "Playing"
        self.play_list()

    def set_time_progress(self):
        """
        Show song progress, time and name while playing
        Parameters
        ----------
        None
        """
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
        i = 0
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
            self.eq_updater()

            # display scolling label
            text_display_space = " " * 3
            playing = (
                text_display_space + "Reproduciendo: " + song_name + text_display_space
            )

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
        """
        Plays a song using pygame
        Parameters
        ----------
        None
        """
        # enable action buttons
        self.prev_music_btn["state"] = NORMAL
        self.pl_music_btn["state"] = NORMAL
        self.next_music_btn["state"] = NORMAL

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
        """
        Plays a list of songs using pygame
        Parameters
        ----------
        None
        """
        # Playing the songs in the background
        playing = True
        while playing:
            if self.index_song <= len(self.song_names) - 1:
                self.song_name = self.song_names[self.index_song]
                self.canvas.itemconfig(
                    self.song_number,
                    text=f"{self.index_song + 1}/{len(self.song_names)}",
                )
                self.play_song()
                self.index_song += 1
            else:
                playing = False

    def stop_music(self):
        """
        Stops the music
        Parameters
        ----------
        None
        """
        pygame.mixer.music.stop()
        self.playing_status = "Not Playing"

    def pause_music(self):
        """
        Pauses the current music
        Parameters
        ----------
        None
        """
        pygame.mixer.music.pause()
        self.playing_status = "Paused"
        self.pl_music_btn.configure(image=self.resume_button)
        # get current played time
        played_time = pygame.mixer.music.get_pos() / 1000

        # format played time
        song_progress = time.strftime("%H:%M:%S", time.gmtime(played_time))

        # update played time labels
        self.canvas.itemconfig(self.playing, text=song_progress)

    def resume_music(self):
        """
        Resumes the current music
        Parameters
        ----------
        None
        """
        pygame.mixer.music.unpause()
        self.playing_status = "Playing"
        self.pl_music_btn.configure(image=self.pause_button)
        self.sleep_secs = 1

    def next_song(self):
        """
        Selects the next song
        Parameters
        ----------
        None
        """
        if len(self.song_names) != 0:
            if self.index_song != len(self.song_names) - 1:
                self.index_song += 1
                self.song_name = self.song_names[self.index_song]
                self.canvas.itemconfig(
                    self.song_number,
                    text=f"{self.index_song + 1}/{len(self.song_names)}",
                )
            self.progress_bar.stop()
            self.play_song()

    def prev_song(self):
        """
        Selects the previous song
        Parameters
        ----------
        None
        """
        if self.index_song > 0:
            self.index_song -= 1
            self.song_name = self.song_names[self.index_song]
            self.canvas.itemconfig(
                self.song_number, text=f"{self.index_song + 1}/{len(self.song_names)}"
            )
            self.progress_bar.stop()
            self.play_song()
        elif self.index_song == 0:
            self.song_name = self.song_names[self.index_song]
            self.progress_bar.stop()
            self.play_song()

    def set_playing_status(self):
        """
        Sets paths to specific locations, input, output, queries
        Parameters
        ----------
        path_type : str
            Whether the path is for an input, output or query location
        path : str
            Path to the specific directory location
        """
        if self.playing_status == "Playing":
            self.pause_music()
        elif self.playing_status == "Paused":
            self.resume_music()

    def set_volume_down(self):
        """
        Turns down the volume
        Parameters
        ----------
        None
        """

        if self.volume > 0 and self.song_volume > 0:
            self.volume -= 0.1
            self.song_volume -= 10
            self.canvas.itemconfig(self.volume_label, text=str(self.song_volume) + "%")
            pygame.mixer.music.set_volume(self.volume)

    def set_volume_up(self):
        """
        Turns up the volume
        Parameters
        ----------
        None
        """
        if self.volume < 1 and self.song_volume <= 100:
            self.volume += 0.1
            self.song_volume += 10
            self.canvas.itemconfig(self.volume_label, text=str(self.song_volume) + "%")
            pygame.mixer.music.set_volume(self.volume)

    def progress_bar_add(self, x_move, color):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(f"{color}.Vertical.TProgressbar", foreground=color, background=color)
        eq_bar = ttk.Progressbar(
            self.root,
            orient="vertical",
            mode="determinate",
            length=300,
            style=f"{color}.Vertical.TProgressbar",
        )

        # place the progressbar
        eq_bar.place(x=27 + x_move, y=80)

    def eq_updater(self):

        for p_bar in sorted(
            [
                child
                for child in self.root.winfo_children()
                if "progressbar" in str(child) and str(child) != ".!progressbar"
            ],
            key=lambda _: random.random(),
        ):
            random_number = random.randint(1, 180)
            p_bar.step(random_number)

    def screen_display(self):
        """
        Displays the player interface
        Parameters
        ----------
        None
        """
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

        # song number
        self.song_number = self.canvas.create_text(
            175.0,
            400,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            font=("Segoe UI", 15 * -1),
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
        self.prev_music_btn = Button(
            self.root,
            command=self.prev_song,
            borderwidth=1,
            image=self.prev_button,
            bg="#0A0A0A",
        )

        self.prev_music_btn.place(x=100, y=619, height=45, width=50)
        self.prev_music_btn["state"] = self.button_state

        # music controls play/plause
        self.pl_music_btn = Button(
            self.root,
            command=self.set_playing_status,
            borderwidth=1,
            image=self.play_button,
            bg="#0A0A0A",
        )
        self.pl_music_btn.place(x=161, y=619, height=45, width=50)
        self.pl_music_btn["state"] = self.button_state

        # music controls next
        self.next_music_btn = Button(
            self.root,
            command=self.next_song,
            image=self.next_button,
            borderwidth=1,
            bg="#0A0A0A",
        )
        self.next_music_btn.place(x=221, y=619, height=45, width=50)
        self.next_music_btn["state"] = self.button_state

        # volume control
        volume_up_btn = Button(
            self.root,
            command=self.set_volume_up,
            borderwidth=1,
            image=self.volume_up,
            bg="#0A0A0A",
        )
        volume_up_btn.place(x=320, y=470, height=32, width=35)
        # tooltip for open tracks button
        self.tip.bind_widget(volume_up_btn, balloonmsg="Volume Up")

        volume_down_btn = Button(
            self.root,
            command=self.set_volume_down,
            borderwidth=1,
            image=self.volume_down,
            bg="#0A0A0A",
        )
        volume_down_btn.place(x=280, y=470, height=32, width=35)
        # tooltip for open tracks button
        self.tip.bind_widget(volume_down_btn, balloonmsg="Volume Down")

        # actions button open song/songs
        open_track_btn = Button(
            self.root,
            command=self.open_music_track,
            borderwidth=1,
            image=self.open_track,
            bg="#0A0A0A",
        )
        open_track_btn.place(x=27, y=470, height=32, width=35)
        # tooltip for open track button
        self.tip.bind_widget(open_track_btn, balloonmsg="Open Song")

        # actions button open song/songs
        open_tracks_btn = Button(
            self.root,
            command=self.open_music_tracks,
            borderwidth=1,
            image=self.open_tracks,
            bg="#0A0A0A",
        )
        open_tracks_btn.place(x=68, y=470, height=32, width=35)
        # tooltip for open tracks button
        self.tip.bind_widget(open_tracks_btn, balloonmsg="Open Play List")

        # # equalizer demo
        move = 0
        for x in range(18):
            randnum = random.randint(0, 6)
            self.progress_bar_add(move, self.color_list[randnum])
            move += 18

        # display app
        self.root.mainloop()

    def launch_player(self):
        """
        Calls the screen_display function that displays the GUI
        Parameters
        ----------
        None
        """
        self.screen_display()
