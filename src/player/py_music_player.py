import random
import os
import time

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
        self.defaultFont.configure(family="Segoe UI",
                                   size=10,
                                   weight=font.BOLD)

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

        # Player information
        self.player_name = title
        self.song_volume = 10
        self.song_length = "00:00:00"
        self.music_progress = 0
        self.song_progress = "00:00:00"
        self.playing_status = "Not Playing"

    # player functionalities
    def open_music_track(self):
        # self.root.withdraw()
        file_name = filedialog.askopenfilename()        
        self.playing_status = "Playing"
        self.play_song(file_name)
        self.pl_music_btn.configure(image=self.pause_button)

    def open_music_tracks(self):
        # self.root.withdraw()

        folder_name = filedialog.askdirectory()
        song_names = []

        # get files from directory
        for file in os.listdir(folder_name):
            if file.endswith(".mp3"):
                song_names.append(folder_name + "/" + file)

        self.play_list(song_names)

    def set_playing_song(self, name):
        text_player = "Reproduciendo"
        text_display_space = " " * 15
        playing = text_display_space + text_player + text_display_space
        song_playing = text_display_space + name + text_display_space
        # playing text message
        for k in range(len(playing)):
            # use string slicing to do the trick
            ticker_text = playing[k : k + 20]
            self.canvas.itemconfig(self.player, text=ticker_text)
            # delay by 0.15 seconds
            time.sleep(0.15)
            self.root.update()

        # playing song text message
        for k in range(len(song_playing)):
            # use string slicing to do the trick
            ticker_text = song_playing[k : k + 20]
            self.canvas.itemconfig(self.name, text=ticker_text)
            # delay by 0.15 seconds
            time.sleep(0.15)
            self.root.update()

    def set_playing_progress(self, song_time, song_progress):

        progress_move = 100 // song_time
        song_length = time.strftime("%H:%M:%S", time.gmtime(song_time))
        self.canvas.itemconfig(self.lenght, text=song_length)
        self.canvas.itemconfig(self.playing, text=song_progress)
        self.progress_bar.step(progress_move)
        
    def set_time_progress(self, song_input):

        self.canvas.itemconfig(self.player, text="Reproduciendo")
        song = pygame.mixer.Sound(song_input)
        song_length_secs = song.get_length()
        song_name = song_input.split("/")[-1].split(".")[0]
        start = time.time()
        counting = True
        i=0
        
        while counting:
            end = time.time()
            seconds_elapsed = end - start
            song_progress = time.strftime("%H:%M:%S", time.gmtime(seconds_elapsed))
            self.set_playing_progress(song_length_secs, song_progress)

            text_display_space = " " * 15
            playing = text_display_space + song_name + text_display_space
            
            # playing text message
            l = len(playing)
            # use string slicing to do the trick
            ticker_text = playing[i : i + 20]
            self.canvas.itemconfig(self.name, text=ticker_text)
            # delay by 0.15 seconds
            time.sleep(1)

            if i < l:
                i += 1
            else:
                i = 0
   
            if seconds_elapsed > song_length_secs:
                counting = False
            
            self.root.update()
            # self.root.deiconify()

    def play_song(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.set_time_progress(song)

    def play_list(self, list):
        pygame.init()
        pygame.mixer.init()
        play_list = sorted(list)

        # Loading first audio file into our player
        pygame.mixer.music.load(play_list[0])

        # Removing the loaded song from our list
        play_list.pop(0)

        # Playing our music
        pygame.mixer.music.play()

        # Queueing next song into our player
        pygame.mixer.music.queue(play_list[0])

        # Removing the loaded song from our list list
        play_list.pop(0)

        # setting up an end event which host an event
        # after the end of every song
        MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END)

        # Playing the songs in the background
        playing = True
        while playing:

            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():

                # A event will be hosted
                # after the end of every song
                if event.type == MUSIC_END:
                    # print("Song Finished")

                    # Checking our list
                    # that if any song exist or
                    # it is empty
                    if len(play_list) > 0:

                        # if song available then load it in player
                        # and remove from the player
                        time.sleep(2)
                        pygame.mixer.music.queue(play_list[0])

                        play_list.pop(0)

                # Checking whether the
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy():
                    # print("list completed")

                    # When the list has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    playing = False
                    break

    def stop_music(self):
        self.playing_status = "Not Playing"
        pygame.mixer.music.stop()

    def pause_music(self):
        self.canvas.itemconfig(self.player, text="Reproducion Pausada")
        pygame.mixer.music.pause()        
        self.playing_status = "Paused"        
        self.pl_music_btn.configure(image=self.resume_button)

    def resume_music(self):
        self.canvas.itemconfig(self.player, text="Reproduciendo")
        pygame.mixer.music.unpause()        
        self.playing_status = "Playing"
        self.pl_music_btn.configure(image=self.pause_button)

    def set_playing_status(self):
        if self.playing_status == "Playing":
            self.pause_music()
        elif self.playing_status == "Paused":
            self.resume_music()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(int(value) / 10)

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
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='black', background='black')
        self.progress_bar = ttk.Progressbar(
                self.root,
                orient='horizontal',
                mode = 'determinate',
                length=315,
                style="red.Horizontal.TProgressbar"
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
        volume_music_ctl = Scale(
            self.root,
            highlightthickness=0,
            relief="ridge",
            label="Volumen",
            bg="#0A0A0A",
            fg="#FFFFFF",
            from_=0,
            to=10,
            orient=HORIZONTAL,
            command=self.set_volume,
        )
        volume_music_ctl.place(x=28, y=470, height=60, width=100)
        volume_music_ctl.set(self.song_volume)

        # actions button open song/songs
        open_track_btn = Button(
            self.root,
            command=self.open_music_track,
            borderwidth=1,
            image=self.open_track,
            bg="#0A0A0A",
        )
        open_track_btn.place(x=24, y=10, height=32, width=35)

        # actions button open song/songs
        open_tracks_btn = Button(
            self.root,
            command=self.open_music_tracks,
            borderwidth=1,
            image=self.open_tracks,
            bg="#0A0A0A",
        )
        open_tracks_btn.place(x=65, y=10, height=32, width=35)

        # song equailizer
        self.canvas.create_rectangle(
            27.0, 100.0, 354.0, 379.0, fill="#FFFFFF", outline=""
        )

        # display app
        self.root.mainloop()

    def launch_player(self):
        self.screen_display()
