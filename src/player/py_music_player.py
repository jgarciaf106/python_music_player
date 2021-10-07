# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyqt_ui/py_music_player.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import random
import pygame
from tkinter import Tk
from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from .py_equalizer_interface import EqualizerBar

track = ""
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
        self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
        self.equalizer.setGeometry(QtCore.QRect(10, 90, 601, 91))
        self.equalizer.setObjectName("equalizer")

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
        self.pushButtonPlay.setGeometry(QtCore.QRect(100, 20, 61, 51))
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.pushButtonPlay.setIcon(QtGui.QIcon("./assets/boton-de-play.png"))
        self.pushButtonPlay.setIconSize(QtCore.QSize(40, 55))        
        self.pushButtonPlay.clicked.connect(self.play_music)

        # pause button
        self.pushButtonPause = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPause.setGeometry(QtCore.QRect(190, 20, 61, 51))
        self.pushButtonPause.setMaximumSize(QtCore.QSize(16777215, 51))
        self.pushButtonPause.setObjectName("pushButtonPause") 
        self.pushButtonPause.setIcon(QtGui.QIcon("./assets/boton-de-pause.png"))
        self.pushButtonPause.setIconSize(QtCore.QSize(40, 55))
        

        # stop button
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setGeometry(QtCore.QRect(280, 20, 61, 51))
        self.pushButtonStop.setObjectName("pushButtonStop")        
        self.pushButtonStop.setIcon(QtGui.QIcon("./assets/boton-de-stop.png"))
        self.pushButtonStop.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonStop.clicked.connect(self.stop_music)

        # resume button
        self.pushButtonResume = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonResume.setGeometry(QtCore.QRect(370, 20, 61, 51))
        self.pushButtonResume.setObjectName("pushButtonResume")
        self.pushButtonResume.setIcon(QtGui.QIcon("./assets/boton-de-resume.png"))
        self.pushButtonResume.setIconSize(QtCore.QSize(40, 55))

        # previous track button
        self.pushButtonPrev = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrev.setGeometry(QtCore.QRect(460, 20, 61, 51))
        self.pushButtonPrev.setObjectName("pushButtonPrev")        
        self.pushButtonPrev.setIcon(QtGui.QIcon("./assets/boton-de-previous.png"))
        self.pushButtonPrev.setIconSize(QtCore.QSize(40, 55))

        # next track button
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNext.setGeometry(QtCore.QRect(550, 20, 61, 51))
        self.pushButtonNext.setObjectName("pushButtonNext")        
        self.pushButtonNext.setIcon(QtGui.QIcon("./assets/boton-de-next.png"))
        self.pushButtonNext.setIconSize(QtCore.QSize(40, 55))

        # open folder button
        self.pushButtonChoose = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoose.setGeometry(QtCore.QRect(10, 20, 61, 51))
        self.pushButtonChoose.setObjectName("pushButtonChoose")        
        self.pushButtonChoose.setIcon(QtGui.QIcon("./assets/boton-de-choose.png"))
        self.pushButtonChoose.setIconSize(QtCore.QSize(40, 55))
        self.pushButtonChoose.clicked.connect(self.open_music_track)

        # volume control
        self.horizontalSliderVolume = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderVolume.setGeometry(QtCore.QRect(10, 310, 61, 22))
        self.horizontalSliderVolume.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderVolume.setObjectName("horizontalSliderVolume")

        # play time
        self.labelTrackTime = QtWidgets.QLabel(self.centralwidget)
        self.labelTrackTime.setGeometry(QtCore.QRect(470, 300, 141, 21))
        self.labelTrackTime.setObjectName("labelTrackTime")

        #
        Player.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Player)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 29))
        self.menubar.setObjectName("menubar")

        #
        Player.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(Player)
        self.statusBar.setObjectName("statusBar")

        #
        Player.setStatusBar(self.statusBar)

        self.retranslate_ui(Player)
        QtCore.QMetaObject.connectSlotsByName(Player)

    def retranslate_ui(self, Player):
        _translate = QtCore.QCoreApplication.translate
        Player.setWindowTitle(_translate("Player", "Py Music Player"))
        self.pushButtonPlay.setText(_translate("Player", ""))
        self.pushButtonPause.setText(_translate("Player", ""))
        self.pushButtonStop.setText(_translate("Player", ""))
        self.pushButtonResume.setText(_translate("Player", ""))
        self.pushButtonPrev.setText(_translate("Player", ""))
        self.pushButtonNext.setText(_translate("Player", ""))
        self.pushButtonChoose.setText(_translate("Player", ""))
        self.labelTrackTime.setText(_translate("Player", "00:00:00 / 00:00:00"))

    def update_values(self):
        self.equalizer.setValues([
            min(100, v+random.randint(0, 50) if random.randint(0, 5) > 2 else v)
            for v in self.equalizer.values()
            ])

    def set_playing_song(self, name):
        playing_song = "Reproduciendo: " + name
        self.textBrowserTrackName.append(playing_song)

    def play_music(self, song):
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def open_music_track(self):
        Tk().withdraw() 
        file_name = filedialog.askopenfilename()
        song_name = file_name.split("/")[-1]
        self.set_playing_song(song_name)
        global track
        track = file_name

    



