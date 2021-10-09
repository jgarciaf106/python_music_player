import random
import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from tkinter import *
from tkinter import filedialog


class Player:
    def __init__(self, title):
        # player gui
        self.root = Tk()

        # title of the window
        self.root.title(title)

        # title icon
        self.root.iconbitmap("./src/assets/sound.ico")

        # window dimension and position
        ## music player wigth and height
        self.window_width = 600
        self.window_height = 400

        # backend music
        pygame.init()
        # inite pygame mixer
        pygame.mixer.init()

    def open_music_track(self):
        self.root.withdraw()
        file_name = filedialog.askopenfilename()
        song_name = file_name.split("/")[-1]
        self.set_playing_song(song_name)
        self.play_song(file_name)

    def open_music_tracks(self):
        self.root.withdraw()
        folder_name = filedialog.askdirectory()
        song_names = []

        # get files from directory
        for file in os.listdir(folder_name):
            if file.endswith(".mp3"):
                song_names.append(folder_name + "/" + file)

        self.play_list(song_names)
        # play songs from directory
        # for song in song_names:
        #     song_name = song.split("/")[-1]
        #     self.set_playing_song(song_name)

    def set_playing_song(self, name):
        playing_song = "Reproduciendo: " + name
        self.textBrowserTrackName.setText(playing_song)

    def play_song(self, song):
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        song = pygame.mixer.Sound(song)
        song_length = time.strftime("%H:%M:%S", time.gmtime(song.get_length()))
        pygame.mixer.music.play()

        start = time.time()

        counting = True
        while counting:
            end = time.time()
            seconds_elapsed = end - start
            song_progress = time.strftime("%H:%M:%S", time.gmtime(seconds_elapsed))

            if seconds_elapsed <= song.get_length():
                self.labelTrackTime.setText(song_progress + "/" + song_length)
                QtWidgets.QApplication.processEvents()
            else:
                counting = False
                self.labelTrackTime.setText(song_progress + "/" + song_length)
                QtWidgets.QApplication.processEvents()

    def play_list(self, list):
        pygame.init()
        pygame.mixer.init()
        play_list = sorted(list)

        # Loading first audio file into our player
        first_song = play_list[0].split("/")[-1]
        pygame.mixer.music.load(play_list[0])

        # Removing the loaded song from our list
        play_list.pop(0)

        # Playing our music
        pygame.mixer.music.play()
        self.set_playing_song(first_song)

        # Queueing next song into our player
        pygame.mixer.music.queue(play_list[0])
        second_song = play_list[0].split("/")[-1]
        self.set_playing_song(second_song)

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
                        current_song = play_list[0].split("/")[-1]
                        self.set_playing_song(current_song)

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
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def volume_music(self):
        pygame.mixer.music.set_volume(self.horizontalSliderVolume.value() / 10)

    def screen_display(self):
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # center screen
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{center_x}+{center_y}"
        )

    def launch_player(self):
        self.screen_display()
        self.root.mainloop()
