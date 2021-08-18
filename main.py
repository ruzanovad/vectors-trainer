from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import sys
import os
import random
import theory, practic, control


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Label(QtWidgets.QLabel):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()


class Frame(QtWidgets.QFrame):  # Рамка
    def __init__(self, title, color, parent, image, text):
        super().__init__()
        self.p = parent

        self.title = QtWidgets.QLabel(title)  # заголовок
        self.title.setFont(self.p.label_font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setScaledContents(True)

        self.setStyleSheet('background-color: {};'.format(color))
        self.layout = QtWidgets.QVBoxLayout()  # макет для вставки виджетов
        self.button = QtWidgets.QPushButton(text)
        if self.button.text() == '→Начать!←':
            self.button.clicked.connect(self.p.theory)
        elif self.button.text() == '↑Начать!↑':
            self.button.clicked.connect(self.p.practic)
        elif self.button.text() == '↓Начать!↓':
            self.button.clicked.connect(self.p.control)
        self.button.setStyleSheet('QPushButton{font-size: 15px}')
        self.pic = QtWidgets.QLabel()  # вставка картинки

        self.pic.setPixmap(QtGui.QPixmap(image))
        self.pic.setScaledContents(True)

        # вставка виджетов в макет

        self.layout.addWidget(self.title, 2)
        self.layout.addWidget(self.pic, 5)
        self.layout.addStretch(1)
        self.layout.addWidget(self.button, 1)
        self.setLayout(self.layout)  # вставка макета в рамку


class OpeningWindow(QtWidgets.QWidget):
    def __init__(self):  # инициализация
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Тренажер")
        self.setWindowIcon(QtGui.QIcon(resource_path(r'resourses\pictures\cartesiano.ico')))

        # установка фонового изображения и шрифта
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("resourses\Handelson-FourCYR.otf"))
        self.label_font = QtGui.QFont("Handelson FourCYR", 40)

        image = QtGui.QImage(resource_path(r'resourses\pictures\background.png'))
        self.mainPalette = QtGui.QPalette()
        self.mainPalette.setBrush(10, QtGui.QBrush(image))
        self.setPalette(self.mainPalette)

        # создание фреймов для кнопок и рисунков

        ff = Frame("Теория", 'rgb(211,200,211)', self, resource_path(r'resourses\pictures\theory.png'), '→Начать!←')
        sf = Frame("Практика", 'rgb(211,211,200)', self, resource_path(r'resourses\pictures\practice.png'), '↑Начать!↑')
        tf = Frame("Контроль", "rgb(200,211,211)", self, resource_path('resourses\pictures\control.png'), '↓Начать!↓')

        self.frames = QtWidgets.QHBoxLayout()
        self.frames.addStretch(5)
        self.frames.addWidget(ff)
        self.frames.addStretch(6)
        self.frames.addWidget(sf)
        self.frames.addStretch(6)
        self.frames.addWidget(tf)
        self.frames.addStretch(5)

        self.frame = QtWidgets.QWidget()
        self.frame.setLayout(self.frames)

        # макет для расположения фреймов

        self.setLayout(QtWidgets.QGridLayout())

        self.label = QtWidgets.QLabel('ТРЕНАЖЕР')
        self.label1 = QtWidgets.QLabel('ПО ТЕМЕ "ВЕКТОР"')
        self.label2 = QtWidgets.QLabel('"Математика, Информатика, Физика"')

        self.label.setFont(QtGui.QFont('Handelson FourCYR', 75))
        self.label1.setFont(QtGui.QFont('Handelson FourCYR', 40))
        self.label2.setFont(QtGui.QFont('Handelson FourCYR', 35))

        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)

        self.authors = QtWidgets.QLabel('БОУ г. Омска "СОШ № 109 с УИОП"', parent=self)
        self.authorsdown = QtWidgets.QLabel(
            'ВЫПОЛНИЛА: Рузанова Дарья Павловна,\nученица 11 «А» класса\nНАУЧНЫЕ РУКОВОДИТЕЛИ:\nГурова Л. М.,\nучитель русского языка и литературы\nЗахарова Е. С.,\nучитель информатики',
            parent=self)

        self.links = Label()
        self.links.setPixmap(QtGui.QPixmap(resource_path('resourses\pictures\links_icon.ico')))

        self.links.signal.connect(self.link)

        self.layout().addWidget(self.authors, 0, 0, 1, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.layout().addWidget(self.label, 0, 1, 1, 1)
        self.layout().addWidget(self.label1, 1, 0, 1, 3)
        self.layout().addWidget(self.label2, 2, 0, 1, 3)
        self.layout().addWidget(self.frame, 3, 0, 1, 3)
        self.layout().addWidget(self.authorsdown, 4, 0, 1, 1)
        self.layout().addWidget(self.links, 4, 2, 1, 1, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.theorywin = None
        self.practicwin = None

        self.showMaximized()

    def theory(self):
        self.theorywin = theory.TheoryWindow(self)
        self.theorywin.showMaximized()
        self.hide()

    def practic(self):
        self.practicwin = practic.PracticeWindow(self)
        self.practicwin.showMaximized()
        self.hide()

    def control(self):
        self.controlwin = control.ControlWindow(self)
        self.controlwin.showMaximized()
        self.hide()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, ' ', "Вы хотите выйти из программы?",
                                               QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if a0.x() >= self.links.x() and a0.x() <= self.links.x() + self.links.width() and a0.y() >= self.links.y() and a0.y() <= self.links.y() + self.links.height():
            self.links.signal.emit()

    def link(self):
        self.l = Links(self)
        self.l.show()
        self.hide()


class Links(QtWidgets.QWidget):
    def __init__(self, p):  # инициализация
        super(Links, self).__init__()
        self.p = p
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowTitle("Список литературы")
        self.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
        self.l = QtWidgets.QVBoxLayout()
        self.text = QtWebEngineWidgets.QWebEngineView()
        self.text.load(QtCore.QUrl.fromLocalFile(resource_path(r'resourses\literature.htm')))
        self.l.addWidget(self.text)
        self.setLayout(self.l)

    def closeEvent(self, event):
        self.p.show()
        event.accept()


if __name__ == '__main__':
    random.seed()
    app = QtWidgets.QApplication(sys.argv)

    # перевод
    translator = QtCore.QTranslator(app)
    translator.load('qt_ru',
                    resource_path(r'resourses'
                                  r'\trans'))
    app.installTranslator(translator)
    win = OpeningWindow()
    sys.exit(app.exec_())
