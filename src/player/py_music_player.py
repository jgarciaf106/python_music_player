# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt_ui/py_music_player.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import random
import os
import pygame
from tkinter import Tk
from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from qtwidgets import EqualizerBar


class Ui_Player(object):
    def setup_ui(self, Player):
        Player.setObjectName("Player")
        Player.resize(620, 400)
        Player.setMaximumSize(QtCore.QSize(620, 400))
        Player.setStyleSheet(
            'font: 10pt "Segoe UI";\n'
            "color: rgb(255, 255, 255);\n"
            "background-color: qlineargradient(spread:pad, x1:0.482, y1:0.4545, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"
        )

        # central widget
        self.centralwidget = QtWidgets.QWidget(Player)
        self.centralwidget.setObjectName("centralwidget")

        # equalizer widget
        # self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
        #                                    '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
        self.widget = EqualizerBar(
            5,
            [
                "#0C0786",
                "#40039C",
                "#6A00A7",
                "#8F0DA3",
                "#B02A8F",
                "#CA4678",
                "#E06461",
                "#F1824C",
                "#FCA635",
                "#FCCC25",
                "#EFF821",
            ],
        )
        self.widget.setGeometry(QtCore.QRect(10, 90, 601, 91))
        self.widget.setObjectName("equalizer")

        self._timer = QtCore.QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()

        # progress bar
        self.horizontalSliderProgress = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderProgress.setGeometry(QtCore.QRect(10, 270, 601, 22))
        self.horizontalSliderProgress.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderProgress.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSliderProgress.setObjectName("horizontalSliderProgress")

        # track name
        self.textBrowserTrackName = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserTrackName.setGeometry(QtCore.QRect(10, 200, 601, 51))
        self.textBrowserTrackName.setObjectName("textBrowserTrackName")

        # plan button
        self.pushButtonPlay = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPlay.setGeometry(QtCore.QRect(10, 20, 61, 51))
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.pushButtonPlay.setIcon(QtGui.QIcon("./src/assets/boton-de-play.png"))
        self.pushButtonPlay.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonPlay.clicked.connect(self.play_song)

        # pause button
        self.pushButtonPause = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPause.setGeometry(QtCore.QRect(100, 20, 61, 51))
        self.pushButtonPause.setMaximumSize(QtCore.QSize(16777215, 51))
        self.pushButtonPause.setObjectName("pushButtonPause")
        self.pushButtonPause.setIcon(QtGui.QIcon("./src/assets/boton-de-pause.png"))
        self.pushButtonPause.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonPause.clicked.connect(self.pause_music)

        # stop button
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setGeometry(QtCore.QRect(190, 20, 61, 51))
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.pushButtonStop.setIcon(QtGui.QIcon("./src/assets/boton-de-stop.png"))
        self.pushButtonStop.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonStop.clicked.connect(self.stop_music)

        # resume button
        self.pushButtonResume = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonResume.setGeometry(QtCore.QRect(280, 20, 61, 51))
        self.pushButtonResume.setObjectName("pushButtonResume")
        self.pushButtonResume.setIcon(QtGui.QIcon("./src/assets/boton-de-resume.png"))
        self.pushButtonResume.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonResume.clicked.connect(self.resume_music)

        # previous track button
        self.pushButtonPrev = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrev.setGeometry(QtCore.QRect(370, 20, 61, 51))
        self.pushButtonPrev.setObjectName("pushButtonPrev")
        self.pushButtonPrev.setIcon(QtGui.QIcon("./src/assets/boton-de-previous.png"))
        self.pushButtonPrev.setIconSize(QtCore.QSize(40, 55))

        # next track button
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNext.setGeometry(QtCore.QRect(460, 20, 61, 51))
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.pushButtonNext.setIcon(QtGui.QIcon("./src/assets/boton-de-next.png"))
        self.pushButtonNext.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonResume.clicked.connect(self.volume_music)

        # volume control
        self.horizontalSliderVolume = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderVolume.setGeometry(QtCore.QRect(10, 310, 61, 22))
        self.horizontalSliderVolume.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderVolume.setObjectName("horizontalSliderVolume")
        self.horizontalSliderVolume.setMinimum(0)
        self.horizontalSliderVolume.setMaximum(10)
        self.horizontalSliderVolume.setSingleStep(1)
        self.horizontalSliderVolume.setProperty("value", 10)
        self.horizontalSliderVolume.valueChanged.connect(self.volume_music)

        # play time
        self.labelTrackTime = QtWidgets.QLabel(self.centralwidget)
        self.labelTrackTime.setGeometry(QtCore.QRect(470, 300, 141, 21))
        self.labelTrackTime.setObjectName("labelTrackTime")

        #
        Player.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Player)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 29))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")

        #
        Player.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(Player)
        self.statusBar.setObjectName("statusBar")

        #
        Player.setStatusBar(self.statusBar)
        self.actionAbrir_Archivo = QtWidgets.QAction(Player)
        self.actionAbrir_Archivo.setObjectName("actionAbrir_Archivo")
        self.actionAbrir_Carpeta = QtWidgets.QAction(Player)
        self.actionAbrir_Carpeta.setObjectName("actionAbrir_Carpeta")
        self.actionAbrir_Archivo.triggered.connect(self.open_music_track)
        self.actionAbrir_Carpeta.triggered.connect(self.open_music_tracks)
        self.menuArchivo.addAction(self.actionAbrir_Archivo)
        self.menuArchivo.addAction(self.actionAbrir_Carpeta)
        self.menubar.addAction(self.menuArchivo.menuAction())

        #
        self.retranslate_ui(Player)
        QtCore.QMetaObject.connectSlotsByName(Player)

    def retranslate_ui(self, Player):
        _translate = QtCore.QCoreApplication.translate
        Player.setWindowTitle(_translate("Player", "Py Music Player"))
        Player.setWindowIcon(QtGui.QIcon("./src/assets/sound.png"))
        self.pushButtonPlay.setText(_translate("Player", ""))
        self.pushButtonPause.setText(_translate("Player", ""))
        self.pushButtonStop.setText(_translate("Player", ""))
        self.pushButtonResume.setText(_translate("Player", ""))
        self.pushButtonPrev.setText(_translate("Player", ""))
        self.pushButtonNext.setText(_translate("Player", ""))
        self.labelTrackTime.setText(_translate("Player", "00:00:00 / 00:00:00"))
        self.menuArchivo.setTitle(_translate("Player", "Archivo"))
        self.actionAbrir_Archivo.setText(_translate("Player", "Abrir Archivo"))
        self.actionAbrir_Carpeta.setText(_translate("Player", "Abrir Carpeta"))

    def update_values(self):
        self.widget.setValues(
            [
                min(100, v + random.randint(0, 50) if random.randint(0, 5) > 2 else v)
                for v in self.widget.values()
            ]
        )

    def set_playing_song(self, name):
        playing_song = "Reproduciendo: " + name
        self.textBrowserTrackName.setText(playing_song)

    def play_song(self, song):
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    def play_list(self, list):
        pygame.init()
        pygame.mixer.init()

        # Loading first audio file into our player
        pygame.mixer.music.load(list[0])

        first_song = list[0].split("/")[-1]
        self.set_playing_song(first_song)
        # Removing the loaded song from our list list
        list.pop(0)

        # Playing our music
        pygame.mixer.music.play()

        # Queueing next song into our player

        # arreglar reproduccion de lista
        pygame.mixer.music.queue(list[0])    


        list.pop(0)

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
                    if len(list) > 0:

                        # if song available then load it in player
                        # and remove from the player                        
                        current_song = list[0].split("/")[-1]
                        self.set_playing_song(current_song)
                        pygame.mixer.music.queue(list[0])
                        list.pop(0)

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

    def open_music_track(self):
        Tk().withdraw()
        file_name = filedialog.askopenfilename()
        song_name = file_name.split("/")[-1]
        self.set_playing_song(song_name)
        self.play_song(file_name)

    def open_music_tracks(self):
        Tk().withdraw()
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
