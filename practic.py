from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import random
import sys
import os
import csv


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def read_csv(path):
    with open(path, "r", newline='') as file:
        reader = csv.reader(file, delimiter=';', dialect=csv.excel)
        return list(reader)


class PracticeWindow(QtWidgets.QWidget):
    def __init__(self, cls):
        super().__init__()
        self.cls = cls
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Тренажер: Практика")
        self.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))

        # установка фонового изображения и шрифта

        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("resourses\Handelson-FourCYR.otf"))
        self.label_font = QtGui.QFont("Handelson FourCYR", 20)

        image = QtGui.QImage(resource_path(r'resourses\pictures\background.png'))
        self.mainPalette = QtGui.QPalette()
        self.mainPalette.setBrush(10, QtGui.QBrush(image))
        self.setPalette(self.mainPalette)

        self.mlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mlayout)

        self.tab = QtWidgets.QTabWidget()
        self.mlayout.addWidget(self.tab)

        # первая вкладка

        self.mainquestion = QtWidgets.QWidget()
        self.layout1 = QtWidgets.QHBoxLayout()
        self.mainquestion.setLayout(self.layout1)
        self.leftframe1 = QtWidgets.QFrame()

        self.tab1 = QtWidgets.QTreeWidget()
        self.layout1.addWidget(self.leftframe1, 6)
        self.layout1.addWidget(self.tab1, 1)

        self.vlayout1 = QtWidgets.QVBoxLayout()
        self.leftframe1.setLayout(self.vlayout1)
        self.text1 = QtWebEngineWidgets.QWebEngineView()
        self.text2 = QtWebEngineWidgets.QWebEngineView()

        self.text1.load(QtCore.QUrl.fromLocalFile(resource_path(r'resourses\приветствие1.htm')))
        self.text2.load(QtCore.QUrl.fromLocalFile(resource_path(r'resourses\приветствие2.htm')))

        self.line = QtWidgets.QLineEdit()
        self.line.setDisabled(True)
        self.check = QtWidgets.QListWidget()
        self.check.setDisabled(True)

        self.answerframe = QtWidgets.QFrame()
        self.anslayout = QtWidgets.QHBoxLayout()
        self.anslayout.addWidget(self.line)
        self.anslayout.addWidget(self.check)
        self.answerframe.setLayout(self.anslayout)

        # масштаб
        self.zoomframe = QtWidgets.QFrame()

        self.label = QtWidgets.QLabel(text='Масштаб')
        self.label.setFont(self.label_font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(40)
        self.slider.setMaximum(250)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.sliderMoved)

        self.zoomslider = QtWidgets.QHBoxLayout()
        self.zoomslider.addWidget(self.label, 1)
        self.zoomslider.addWidget(self.slider, 6)

        self.zoomframe.setLayout(self.zoomslider)

        self.btn1 = QtWidgets.QPushButton('Назад')
        self.btn2 = QtWidgets.QPushButton('Проверить')
        self.btn3 = QtWidgets.QPushButton('Пропустить')
        self.btn4 = QtWidgets.QPushButton('Вперед')

        self.btn1.clicked.connect(self.backward)
        self.btn2.clicked.connect(self.checking)
        self.btn3.clicked.connect(self.inactiveIndicator)
        self.btn4.clicked.connect(self.forward)

        self.btnlayout = QtWidgets.QHBoxLayout()
        self.btnlayout.addStretch(1)
        self.btnlayout.addWidget(self.btn1)
        self.btnlayout.addStretch(1)
        self.btnlayout.addWidget(self.btn2)
        self.btnlayout.addStretch(1)
        self.btnlayout.addWidget(self.btn3)
        self.btnlayout.addStretch(1)
        self.btnlayout.addWidget(self.btn4)
        self.btnlayout.addStretch(1)

        self.btnframe = QtWidgets.QFrame()
        self.btnframe.setLayout(self.btnlayout)

        self.vlayout1.addWidget(self.text1)
        self.vlayout1.addWidget(self.zoomframe)
        self.vlayout1.addWidget(self.answerframe)
        self.vlayout1.addWidget(self.btnframe)
        self.vlayout1.addWidget(self.text2)

        #  настройка дерева

        self.tab1.setHeaderLabel('Материалы')
        self.tab1.header().setStretchLastSection(False)
        self.tab1.header().setSectionResizeMode(3)

        for x in os.listdir(resource_path(r'resourses\practise\Теория')):
            parent = QtWidgets.QTreeWidgetItem(self.tab1)
            parent.setText(0, x)
            for y in [f for f in os.listdir(resource_path(r'resourses\practise\Теория\{}'.format(x)))]:
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, y)
        self.tab1.itemClicked.connect(self.onItemClicked)

        #  вторая вкладка

        self.leftframe = QtWidgets.QFrame()
        self.centerframe = QtWidgets.QFrame()
        self.rightframe = QtWidgets.QFrame()

        self.tablayout = QtWidgets.QHBoxLayout()

        self.tablayout.addWidget(self.leftframe)
        self.tablayout.addWidget(self.centerframe)
        self.tablayout.addWidget(self.rightframe)

        self.tree = QtWidgets.QTreeWidget(self.leftframe)
        self.text = QtWebEngineWidgets.QWebEngineView(self.rightframe)
        self.widget = QtWidgets.QWidget()
        self.panel = QtWidgets.QFrame()

        self.vlayout = QtWidgets.QVBoxLayout()
        self.centerframe.setLayout(self.vlayout)
        self.vlayout.addWidget(self.widget)
        self.vlayout.addWidget(self.panel)

        self.testtab = QtWidgets.QWidget()
        #  self.testtab.setLayout(self.tablayout)

        # вставка виджетов в TabWidget

        self.tab.addTab(self.mainquestion, 'Вопросы')
        # self.tab.addTab(self.testtab, 'Задачи') todo second tab

        self.indicator = '0'
        self.number = None
        self.settings = None

        self.previous = None
        self.count = None

    def closeEvent(self, event):
        if self.indicator == 'passive' or self.indicator == '0':
            reply = QtWidgets.QMessageBox.question(self, 'Вы уверены?', "Весь прогресс будет сброшен.",
                                                   QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                self.cls.show()
                event.accept()
            else:
                event.ignore()
        else:
            warn = QtWidgets.QMessageBox.warning(self, 'Вы не можете выйти сейчас!',
                                                 'Решите задание или нажмите "Пропустить".', QtWidgets.QMessageBox.Ok)
            if warn == QtWidgets.QMessageBox.Ok:
                event.ignore()

    def sliderMoved(self):
        self.text1.setZoomFactor(self.slider.value() / 100)
        self.text2.setZoomFactor(self.slider.value() / 100)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, it):
        if self.indicator == 'passive' or self.indicator == '0':
            if it.text(0) not in os.listdir(resource_path(r'resourses\practise\Теория')):
                self.activeIndicator()
                self.settings = read_csv(
                    resource_path(r'resourses\practise\Теория\{}\{}\settings.csv'.format(it.parent().text(0),
                                                                                         it.text(0))))

                self.number = random.randint(0, len(self.settings) - 2)
                self.text1.load(QtCore.QUrl.fromLocalFile(
                    resource_path(r'resourses\practise\Теория\{}\{}\test{}.htm'.format(it.parent().text(0), it.text(0),
                                                                                       self.number))))

                if self.settings[self.number + 1][1] == 'line':
                    self.line.setDisabled(False)
                if self.settings[self.number + 1][1] == 'check':
                    self.check.setDisabled(False)
                    number = random.randint(len(self.settings[self.number + 1][2].split(',')) // 2,
                                            len(self.settings[self.number + 1][2].split(',')))
                    choice = list(set(random.choices(self.settings[self.number + 1][2].split(','), k=number)))
                    c = random.choice(self.settings[self.number + 1][3].split(','))
                    if c not in choice:
                        choice.append(c)
                    for i in choice:
                        j = QtWidgets.QListWidgetItem()
                        j.setText(i)
                        j.setFlags(j.flags() | QtCore.Qt.ItemIsUserCheckable)
                        j.setCheckState(QtCore.Qt.Unchecked)
                        self.check.addItem(j)

        else:
            if it.text(0) not in os.listdir(resource_path(r'resourses\practise\Теория')):
                if it.text(0) == self.text1.url().toLocalFile().split('/')[-2]:
                    return (None)
                self.warning()

    def warning(self):
        self.warn = QtWidgets.QMessageBox(None)
        self.warn.setIcon(QtWidgets.QMessageBox.Warning)
        self.warn.setText('Чтобы перейти к другому заданию, сперва нажмите "Пропустить".')
        self.warn.setWindowTitle('Задание еще не выполнено!')
        self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.warn.exec_()

    def inactiveIndicator(self):
        #  if self.tab.currentIndex() == 0:
        self.btn1.setDisabled(False)
        self.btn4.setDisabled(False)
        # self.tab.setTabEnabled(1, True)
        self.line.setDisabled(True)
        self.check.setDisabled(True)
        self.indicator = 'passive'

    def activeIndicator(self):
        #  if self.tab.currentIndex() == 0:
        self.btn1.setDisabled(True)
        self.btn4.setDisabled(True)
        self.text2.load(QtCore.QUrl.fromLocalFile(resource_path(r'resourses\приветствие2.htm')))
        # self.tab.setTabEnabled(1, False)
        self.line.setText('')
        self.check.clear()
        self.indicator = 'active'

    def checking(self):
        if self.line.isEnabled():
            if self.line.text() is '':
                self.warn = QtWidgets.QMessageBox(None)
                self.warn.setIcon(QtWidgets.QMessageBox.Warning)
                self.warn.setText('Пустая строка!')
                self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.warn.exec_()
            else:
                if self.line.text() == self.settings[self.number + 1][3]:
                    self.warn = QtWidgets.QMessageBox(None)
                    self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                    self.warn.setIcon(QtWidgets.QMessageBox.Information)
                    self.warn.setText('Все верно!')
                    self.warn.setWindowTitle('Ура!')
                    self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.warn.exec_()
                    locale = self.text1.url().toLocalFile().split('/')[0:-1]
                    locale.append(self.text1.url().fileName().replace('test', 'answer'))
                    self.text2.load(QtCore.QUrl.fromLocalFile('/'.join(locale)))
                    self.inactiveIndicator()
                else:
                    if self.indicator == '0':
                        pass
                    if self.previous == self.text1.url():
                        self.count += 1
                    else:
                        self.count = 0
                    self.previous = self.text1.url()
                    if self.count != 3:
                        self.warn = QtWidgets.QMessageBox(None)
                        self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                        self.warn.setIcon(QtWidgets.QMessageBox.Critical)
                        self.warn.setText('Попробуйте повторить теорию.')
                        self.warn.setWindowTitle('Что-то не так...')
                        self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.warn.exec_()
                    else:
                        self.warn = QtWidgets.QMessageBox(None)
                        self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                        self.warn.setIcon(QtWidgets.QMessageBox.Information)
                        self.warn.setText('Кажется, вы попали в тупик...')
                        self.warn.setWindowTitle('Что-то не так...')
                        self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.warn.exec_()
                        locale = self.text1.url().toLocalFile().split('/')[0:-1]
                        locale.append(self.text1.url().fileName().replace('test', 'answer'))
                        self.text2.load(QtCore.QUrl.fromLocalFile('/'.join(locale)))
                        self.inactiveIndicator()
                        self.count = 0

        elif self.check.isEnabled():
            answer = self.settings[self.number + 1][3].split(',')
            items = []
            for i in range(self.check.count()):
                if self.check.item(i).checkState() == 2:
                    items.append(self.check.item(i).text())

            if any(elem in items for elem in answer):
                self.warn = QtWidgets.QMessageBox(None)
                self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                self.warn.setIcon(QtWidgets.QMessageBox.Information)
                self.warn.setText('Все верно!')
                self.warn.setWindowTitle('Ура!')
                self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.warn.exec_()
                locale = self.text1.url().toLocalFile().split('/')[0:-1]
                locale.append(self.text1.url().fileName().replace('test', 'answer'))
                self.text2.load(QtCore.QUrl.fromLocalFile('/'.join(locale)))
                self.inactiveIndicator()
            else:
                if self.indicator == '0':
                    pass
                if self.previous == self.text1.url():
                    self.count += 1
                else:
                    self.count = 0
                self.previous = self.text1.url()
                if self.count != 3:
                    self.warn = QtWidgets.QMessageBox(None)
                    self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                    self.warn.setIcon(QtWidgets.QMessageBox.Critical)
                    self.warn.setText('Попробуйте повторить теорию.')
                    self.warn.setWindowTitle('Что-то не так...')
                    self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.warn.exec_()
                else:
                    self.warn = QtWidgets.QMessageBox(None)
                    self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
                    self.warn.setIcon(QtWidgets.QMessageBox.Information)
                    self.warn.setText('Кажется, вы попали в тупик...')
                    self.warn.setWindowTitle('Что-то не так...')
                    self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.warn.exec_()
                    locale = self.text1.url().toLocalFile().split('/')[0:-1]
                    locale.append(self.text1.url().fileName().replace('test', 'answer'))
                    self.text2.load(QtCore.QUrl.fromLocalFile('/'.join(locale)))
                    self.inactiveIndicator()
                    self.count = 0



    def forward(self):
        if self.indicator == '0':
            return False
        elif self.indicator == 'passive':
            if self.tab1.currentItem().childCount() == 0 and self.tab1.itemBelow(
                    self.tab1.currentItem()).childCount() == 0:
                if self.tab1.currentItem().parent() == self.tab1.itemBelow(self.tab1.currentItem()).parent():
                    self.tab1.setCurrentItem(self.tab1.itemBelow(self.tab1.currentItem()))
                    self.onItemClicked(self.tab1.currentItem())

    def backward(self):
        if self.indicator == '0':
            return False
        elif self.indicator == 'passive':
            if self.tab1.currentItem().childCount() == 0 and self.tab1.itemAbove(
                    self.tab1.currentItem()).childCount() == 0:
                if self.tab1.currentItem().parent() == self.tab1.itemAbove(self.tab1.currentItem()).parent():
                    self.tab1.setCurrentItem(self.tab1.itemAbove(self.tab1.currentItem()))
                    self.onItemClicked(self.tab1.currentItem())


if __name__ == '__main__':
    random.seed()
    app = QtWidgets.QApplication(sys.argv)
    win = PracticeWindow(None)
    win.showMaximized()
    sys.exit(app.exec_())
