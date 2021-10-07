# library import
from PyQt5.QtWidgets import QApplication, QMainWindow
import player.py_music_player as pl
import sys

# run app interface
app = QApplication(sys.argv)
player = QMainWindow()
ui = pl.Ui_Player()
ui.setup_ui(player)
player.show()
sys.exit(app.exec_())
