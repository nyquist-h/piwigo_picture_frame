import configparser
import glob
import os
import configparser
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Digital picture frame'
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1080

        self.load_pictures()
        self.initUI()
        print(self.pic_memories)

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.frame = QLabel(self)
        pixmap = QPixmap(self.pic_memories[self.pic_memories_index])
        self.frame.setPixmap(pixmap)
        self.resize(1920,1080)

        self.mytimer = QTimer()
        self.mytimer.timeout.connect(self.change_picture)
        self.mytimer.start(1000)

        self.show()

    def load_pictures(self):
        print('loading pictures')
        config = configparser.ConfigParser()
        config.read('piwigo.ini')
        base_location = config.get('pictures','location')
        memories_location = os.path.join(base_location, "memories/resized/*")
        self.pic_memories = glob.glob(memories_location)
        self.pic_memories_index = 0

    def change_picture(self):
          self.pic_memories_index += 1
          if (self.pic_memories_index >= len(self.pic_memories)):
              self.load_pictures()

          pixmap = QPixmap(self.pic_memories[self.pic_memories_index])
          self.frame.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

