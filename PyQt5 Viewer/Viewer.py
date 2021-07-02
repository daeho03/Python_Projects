import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.extension = QComboBox()
        self.extension.addItem("gif")
        self.extension.addItem("img")
        self.extension.addItem("jpg")
        self.extension.addItem("jpeg")
        self.extension.addItem("png")

        self.search = QPushButton("폴더선택")
        self.search.clicked.connect(self.OpenDir)
        
        self.open = QPushButton("선택파일 열기")
        self.open.clicked.connect(self.Open)
        
        self.cb = QComboBox()
        
        self.result = QPlainTextEdit("")

        self.img = QLabel("")

        self.prev = QPushButton("이전")
        self.prev.clicked.connect(self.Prev)

        self.next = QPushButton("다음")
        self.next.clicked.connect(self.Next)

        grid.addWidget(self.cb, 0, 0, 1, 4) # 파일콤보박스
        grid.addWidget(self.open, 1, 0, 1, 4) # 선택
        grid.addWidget(self.prev, 2, 0, 1, 2) # 2칸 버튼
        grid.addWidget(self.next, 2, 2, 1, 2) # 2칸 버튼
        grid.addWidget(self.img, 3, 0, 1, 4) # 출력

        grid.addWidget(QLabel("확장자 선택"), 4, 0) # 라벨
        grid.addWidget(self.extension, 4, 1, 1, 3) # 확장자 콤보박스
        grid.addWidget(self.search, 5, 0, 1, 4) # 폴더 열기

        self.setWindowTitle("뷰어")
        self.setGeometry(400, 400, 200, 100)
        self.show()

    def OpenDir(self):
        self.index = 0
        self.cb.clear()

        try:
            self.dirName = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), "./",
                                                    QFileDialog.ShowDirsOnly)
        except FileNotFoundError:
            self.img.setText(" *경로를 찾을 수 없습니다*")
        else:
            extension = self.extension.currentText()
            path = str(self.dirName)
            self.file_list = os.listdir(path)
            self.file_list = [file for file in self.file_list if file.endswith(".{}".format(extension))]
            self.file_list = sorted(self.file_list)

            for file in self.file_list:
                self.cb.addItem(file)
            if len(self.file_list) > 0:
                img = QPixmap("{}/{}".format(str(self.dirName), str(self.file_list[0])))
                img = img.scaledToHeight(700)
                self.img.setPixmap(img)
                self.index = 0
            else:
                self.img.setText(" *파일을 찾을 수 없습니다*")

    def Open(self):
        if len(self.file_list) > 0:
            img = QPixmap("{}/{}".format(str(self.dirName), str(self.cb.currentText())))
            img = img.scaledToHeight(700)
            self.img.setPixmap(img)
            self.index = self.file_list.index(self.cb.currentText())

    def Prev(self):
        if len(self.file_list) > 0 and self.index > 0:
            self.index -= 1
            img = QPixmap("{}/{}".format(str(self.dirName), str(self.file_list[self.index])))
            img = img.scaledToHeight(700)
            self.img.setPixmap(img)

    def Next(self):
        if len(self.file_list) > 0 and self.index < len(self.file_list):
            self.index += 1
            img = QPixmap("{}/{}".format(str(self.dirName), str(self.file_list[self.index])))
            img = img.scaledToHeight(700)
            self.img.setPixmap(img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    main.show()
    sys.exit(app.exec_())
