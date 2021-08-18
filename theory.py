from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class TheoryWindow(QtWidgets.QWidget):
    def __init__(self, cls):  # инициализация
        super().__init__()
        self.cls = cls
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Тренажер: Теория")
        self.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))

        # установка фонового изображения и шрифта
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("resourses\Handelson-FourCYR.otf"))
        self.label_font = QtGui.QFont("Handelson FourCYR", 20)

        image = QtGui.QImage(resource_path(r'resourses\pictures\background.png'))
        self.mainPalette = QtGui.QPalette()
        self.mainPalette.setBrush(10, QtGui.QBrush(image))
        self.setPalette(self.mainPalette)

        #  левая панель

        self.leftframe = QtWidgets.QFrame()
        self.maintext = QtWebEngineWidgets.QWebEngineView()
        self.maintext.load(QtCore.QUrl.fromLocalFile(resource_path(r'resourses\приветствие.htm')))
        self.panel = QtWidgets.QFrame()
        self.panel.setStyleSheet('background-color: rgb(211,200,211);')

        #  правая панель

        self.rightframe = QtWidgets.QFrame()
        self.tree = QtWidgets.QTreeWidget()

        #  дерево

        self.tree.setHeaderLabel('Материалы')
        self.tree.itemClicked.connect(self.onItemClicked)
        for x in os.listdir(resource_path(r'resourses\theory')):
            parent = QtWidgets.QTreeWidgetItem(self.tree)
            parent.setText(0, x)
            for y in [f for f in os.listdir(
                    resource_path(r'resourses\theory\{}'.format(x))) if
                      os.path.isfile(os.path.join(
                          resource_path(r'resourses\theory\{}'.format(x)), f))]:
                if y.split('.')[-1] == 'htm':
                    child = QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0, y[0:-4])

        #  scrollbar
        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(3)

        #  ползунок с масштабом + подпись

        self.label = QtWidgets.QLabel(text='Масштаб')
        self.label.setFont(self.label_font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(40)
        self.slider.setMaximum(250)
        self.slider.setValue(100)

        self.slider.valueChanged.connect(self.sliderMoved)

        #  макеты

        self.mainlayout = QtWidgets.QHBoxLayout()
        self.first_vlayout = QtWidgets.QVBoxLayout()
        self.second_vlayout = QtWidgets.QVBoxLayout()
        self.minilayout = QtWidgets.QHBoxLayout()

        #  установка виджетов в макеты

        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.leftframe, 6)
        self.mainlayout.addWidget(self.rightframe, 2)

        self.leftframe.setLayout(self.first_vlayout)
        self.rightframe.setLayout(self.second_vlayout)

        self.first_vlayout.addWidget(self.maintext)
        self.first_vlayout.addWidget(self.panel)
        self.panel.setLayout(self.minilayout)
        self.minilayout.addWidget(self.label, 1)
        self.minilayout.addWidget(self.slider, 6)

        self.second_vlayout.addWidget(self.tree)

    def sliderMoved(self):
        self.maintext.setZoomFactor(self.slider.value() / 100)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it):
        if it.text(0) not in os.listdir(resource_path(r'resourses\theory')):
            local = QtCore.QUrl.fromLocalFile(
                resource_path(r'resourses\theory\{}\{}.htm'.format(it.parent().text(0), it.text(0))))
            self.maintext.load(local)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Вы уверены?', "Весь прогресс будет сброшен.",
                                               QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.cls.show()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = TheoryWindow(None)
    win.showMaximized()
    sys.exit(app.exec_())
