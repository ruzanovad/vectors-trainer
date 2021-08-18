from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
import sys
import os
import time
import csv
import importlib.util as util
import random


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.normcase(os.path.normpath(os.path.join(base_path, relative_path)))


def read_csv(path):
    with open(path, "r", newline='') as file:
        reader = csv.reader(file, delimiter=';', dialect=csv.excel)
        return list(reader)


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent=parent)

        self.setWindowTitle(' ')
        self.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))

        # listbox

        list_of_difficulties = ['Простой', 'Нормальный', 'Сложный']
        self.list_widget = QtWidgets.QListWidget()
        for i in list_of_difficulties:
            self.list_widget.addItem(i)
        self.list_widget.itemDoubleClicked.connect(self.doubleclicked)

        # label

        label = QtWidgets.QLabel('Выберите сложность:')

        # buttons

        self.buttons = QtWidgets.QDialogButtonBox()
        self.buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.rejected.connect(self.reject)
        self.buttons.accepted.connect(self.clicked)

        # layout

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addWidget(label, 1)
        vlayout.addWidget(self.list_widget, 3)
        vlayout.addWidget(self.buttons)

        self.setLayout(vlayout)

    def clicked(self):
        if self.list_widget.selectedItems() == []:
            warn = QtWidgets.QMessageBox.warning(self, 'Внимание', 'Вы не выбрали сложность', QtWidgets.QMessageBox.Ok)
        else:
            self.r = self.list_widget.currentItem().text()
            self.accept()

    def doubleclicked(self):
        self.r = self.list_widget.currentItem().text()
        self.accept()


class Label(QtWidgets.QLabel):
    signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()


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


class Control(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Control, self).__init__(parent=parent)

    def setupUI(self):
        self.tasks_answers_html = self.parent().tasks_answers_html

        # установка фонового изображения и шрифта

        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("resourses\Handelson-FourCYR.otf"))
        self.label_font = QtGui.QFont("Handelson FourCYR", 40)

        self.hlayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout)

        self.leftframe = QtWidgets.QFrame()
        self.rightframe = QtWidgets.QFrame()

        self.rightframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rightframe.setFrameStyle(QtWidgets.QFrame.Raised)
        self.rightframe.setStyleSheet('background-color: rgb(211,200,211);')

        self.hlayout.addWidget(self.leftframe, stretch=5)
        self.hlayout.addWidget(self.rightframe, stretch=1)

        self.leftlayout = QtWidgets.QVBoxLayout()

        self.leftframe.setLayout(self.leftlayout)
        self.text = QtWebEngineWidgets.QWebEngineView()

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(40)
        self.slider.setMaximum(250)
        self.slider.setValue(100)

        self.slider.valueChanged.connect(self.sliderMoved)

        self.btnframe = QtWidgets.QFrame()
        self.btnlayout = QtWidgets.QHBoxLayout()
        self.btnframe.setLayout(self.btnlayout)

        self.btn1 = QtWidgets.QPushButton('Назад')
        self.btn4 = QtWidgets.QPushButton('Вперед')
        self.label = QtWidgets.QLineEdit()
        self.label.setReadOnly(True)
        self.label0 = QtWidgets.QLabel()
        self.label0.setFont(QtGui.QFont('Handelson FourCYR', 50))

        self.btn1.clicked.connect(self.backward)
        self.btn4.clicked.connect(self.forward)

        self.btnlayout.addStretch(1)
        self.btnlayout.addWidget(self.btn1)
        self.btnlayout.addWidget(self.label)
        self.btnlayout.addWidget(self.btn4)
        self.btnlayout.addWidget(self.label0)

        self.btnlayout.addStretch(1)

        self.leftlayout.addWidget(self.text)
        self.leftlayout.addWidget(self.slider)
        self.leftlayout.addWidget(self.btnframe)

        self.rightlayout = QtWidgets.QVBoxLayout()

        self.rightframe.setLayout(self.rightlayout)

        self.label1 = QtWidgets.QLabel()
        self.grade = QtWidgets.QLabel()
        self.motivation = QtWidgets.QLabel()
        self.listw = QtWidgets.QListWidget()
        self.links = Label()

        self.links.setPixmap(QtGui.QPixmap(resource_path('resourses\pictures\links_icon.ico')))
        self.links.signal.connect(self.link)

        self.parameter = 0

        for j in self.parent().tasks:
            a = QtWidgets.QListWidgetItem()
            if self.parent().answers[self.parent().tasks.index(j)] == j.answer:
                a.setForeground(QtGui.QColor(QtCore.Qt.darkGreen))
                self.parameter += 1
            else:
                a.setForeground(QtGui.QColor(QtCore.Qt.red))
            a.setText('{}){}'.format(j.number_of_task, j.taskname))
            self.listw.addItem(a)
        self.listw.itemClicked.connect(self.selected)

        self.rightlayout.addWidget(self.listw)
        self.rightlayout.addWidget(self.label1)
        self.rightlayout.addWidget(self.grade)
        self.rightlayout.addWidget(self.motivation)
        self.rightlayout.addWidget(self.links)

        self.text.load(QtCore.QUrl.fromLocalFile(self.tasks_answers_html[0]))
        if self.parent().answers[0] != self.parent().tasks[0].answer:
            palette = QtGui.QPalette()
            palette.setBrush(QtGui.QPalette.Text, QtGui.QColor(QtCore.Qt.red))
            self.label.setPalette(palette)
        else:
            palette = QtGui.QPalette()
            palette.setBrush(QtGui.QPalette.Text, QtGui.QColor(QtCore.Qt.darkGreen))
            self.label.setPalette(palette)

        self.label.setText(self.parent().answers[0])
        self.label1.setText('Вы набрали {}/{} баллов.'.format(self.parameter, str(self.parent().n)))
        self.label1.setFont(self.label_font)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        g = self.parameter * 5 // self.parent().n
        if g < 2:
            g = 2

        self.grade.setText('Оценка {}'.format(g))
        self.grade.setFont(QtGui.QFont("Handelson FourCYR", 60))
        self.grade.setAlignment(QtCore.Qt.AlignCenter)

        t = ['Не расстраивайтесь! У Вас все получится!', 'Попробуйте еще раз. У Вас все получится!',
             'Неплохой результат!', 'Отлично! Так держать!']
        self.motivation.setFont(self.label_font)
        self.motivation.setText(t[g - 2])
        self.motivation.setAlignment(QtCore.Qt.AlignCenter)

        self.links.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label0.setText(str(self.parent().tasks[0].number_of_task))

        self.tasks, self.tasks_html, self.answers = self.parent().tasks, self.parent().tasks_html, self.parent().answers

    def sliderMoved(self):
        self.text.setZoomFactor(self.slider.value() / 100)

    def forward(self):
        url = os.path.normcase(os.path.normpath(self.text.url().toLocalFile()))
        if url in self.parent().tasks_html:
            if self.tasks_html.index(url) != len(self.tasks) - 1:
                self.text.load(
                    QtCore.QUrl.fromLocalFile(self.tasks_html[self.tasks_html.index(url) + 1]))
                self.label0.setText(str(self.tasks[self.tasks_html.index(url) + 1].number_of_task))
                self.label.setText(self.answers[self.tasks_html.index(url) + 1])
        else:
            if self.tasks_answers_html.index(url) != len(self.tasks) - 1:
                self.text.load(
                    QtCore.QUrl.fromLocalFile(self.tasks_answers_html[self.tasks_answers_html.index(url) + 1]))
                self.label0.setText(str(self.tasks[self.tasks_answers_html.index(url) + 1].number_of_task))
                self.label.setText(self.answers[self.tasks_answers_html.index(url) + 1])


    def backward(self):
        url = os.path.normcase(os.path.normpath(self.text.url().toLocalFile()))
        if url in self.parent().tasks_html:
            if self.tasks_html.index(url) != 0:
                self.text.load(
                    QtCore.QUrl.fromLocalFile(self.tasks_html[self.tasks_html.index(url) - 1]))
                self.label0.setText(str(self.tasks[self.tasks_html.index(url) - 1].number_of_task))
                self.label.setText(self.answers[self.tasks_html.index(url) - 1])
        else:
            if self.tasks_answers_html.index(url) != 0:
                self.text.load(
                    QtCore.QUrl.fromLocalFile(self.tasks_answers_html[self.tasks_answers_html.index(url) - 1]))
                self.label0.setText(str(self.tasks[self.tasks_answers_html.index(url) - 1].number_of_task))
                self.label.setText(self.answers[self.tasks_answers_html.index(url) - 1])

    def selected(self, it):
        number, taskname = it.text().split(')')
        self.label.setText(self.answers[int(number)-1])
        for i in range(len(self.tasks)):
            if self.tasks[i].taskname == taskname and str(self.tasks[i].number_of_task) == str(number):
                self.text.load(QtCore.QUrl.fromLocalFile(self.tasks_answers_html[i]))
                self.label0.setText(number)

    def change(self):
        a = self.text.url().toLocalFile()
        if a in self.tasks_answers_html:
            b = self.tasks_answers_html.index(a)
            self.text.load(self.parent().tasks_html[b])
        else:
            b = self.parent().tasks_html.index(a)
            self.text.load(self.tasks_answers_html[b])

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if a0.x() >= self.width() - self.links.x() - self.links.height() and a0.x() <= self.width() - self.links.x() and a0.y() >= self.links.y() and a0.y() <= self.links.y() + self.links.height():
            self.links.signal.emit()

    def link(self):
        self.l = Links(self.parent())
        self.l.show()
        self.parent().hide()


class Test(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent=parent)

    def setupUI(self):

        self.testlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.testlayout)

        self.text = QtWebEngineWidgets.QWebEngineView()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        self.progresstimer = QtCore.QTimer()
        self.progresstimer.timeout.connect(self.Progress)
        self.progresstimer.start({0: 5, 1: 6, 2: 8}[self.parent().complexity] * 600 * self.parent().n)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        self.progress.setStyleSheet('QProgressBar::chunk { background: rgb(255,255,255); }')
        self.colorred = 255

        self.lcd = QtWidgets.QLCDNumber(5)
        self.lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)

        palette = QtGui.QPalette()
        palette.setColor(palette.WindowText, QtGui.QColor(255, 85, 255))
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        palette.setColor(palette.Light, QtGui.QColor(255, 0, 0))
        palette.setColor(palette.Dark, QtGui.QColor(0, 255, 0))

        self.lcd.setPalette(palette)

        self.lcd.setStyleSheet('background-color: rgb(0,20,20);')
        self.lcd.display('{}:00'.format(str({0: 5, 1: 6, 2: 8}[self.parent().complexity] * self.parent().n)))
        self.time = time.time()

        self.timeframe = QtWidgets.QFrame()
        self.timeframelayout = QtWidgets.QHBoxLayout()
        self.timeframelayout.addStretch(9)
        self.timeframelayout.addWidget(self.lcd)
        self.timeframelayout.addStretch(9)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(40)
        self.slider.setMaximum(250)
        self.slider.setValue(100)

        self.slider.valueChanged.connect(self.sliderMoved)

        self.btnframe = QtWidgets.QFrame()
        self.btnlayout = QtWidgets.QHBoxLayout()
        self.btnframe.setLayout(self.btnlayout)

        self.btn1 = QtWidgets.QPushButton('Назад')
        self.line = QtWidgets.QLineEdit()
        self.btn4 = QtWidgets.QPushButton('Вперед')
        self.label = QtWidgets.QLabel()
        self.label.setFont(QtGui.QFont('Handelson FourCYR', 50))

        self.btn1.clicked.connect(self.backward)
        self.btn4.clicked.connect(self.forward)

        self.btnlayout.addStretch()
        self.btnlayout.addWidget(self.btn1)
        self.btnlayout.addWidget(self.line)
        self.btnlayout.addWidget(self.btn4)
        self.btnlayout.addWidget(self.label)
        self.btnlayout.addStretch()

        self.controlbtn = QtWidgets.QPushButton('Завершить тест')
        self.controlbtn.setFlat(True)
        self.controlbtn.clicked.connect(self.checking)

        self.testlayout.addWidget(self.text)
        self.testlayout.addWidget(self.progress)
        self.testlayout.addWidget(self.lcd)
        self.testlayout.addWidget(self.slider)
        self.testlayout.addWidget(self.btnframe)
        self.testlayout.addWidget(self.controlbtn)

        self.tasks = self.parent().tasks

        self.tasks_html = self.parent().tasks_html

        self.answers = ['' for i in range(self.parent().n)]

        self.text.load(QtCore.QUrl.fromLocalFile(self.tasks_html[0]))

        self.label.setText('1')
        self.parent().indicator = 'active'

    def sliderMoved(self):
        self.text.setZoomFactor(self.slider.value() / 100)

    def Time(self):
        t = time.gmtime({0: 5, 1: 6, 2: 8}[self.parent().complexity] * 60 * self.parent().n + self.time - time.time())
        a, b = str(t.tm_min), str(t.tm_sec)
        if t.tm_min < 10: a = '0' + a
        if t.tm_sec < 10: b = '0' + b
        self.lcd.display(a + ':' + b)
        if a == '00' and b == '00':
            self.timer.stop()
            self.timer1.stop()
            self.timer2.stop()
            self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
            self.warn.setIcon(QtWidgets.QMessageBox.Critical)
            self.warn.setText('Время вышло!')
            self.warn.setWindowTitle(' ')
            self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.warn.exec_()
            self.parent().ControlUI(self.tasks, self.tasks_html, self.answers)

    def Progress(self):
        self.progress.setStyleSheet(
            'QProgressBar::chunk { background: rgb(255,%s,%s); }' % ((str(self.colorred - 1)), str(self.colorred - 1)))
        self.colorred -= 1
        self.progress.setValue(self.progress.value() + 1)

    def forward(self):
        url = os.path.normcase(os.path.normpath(self.text.url().toLocalFile()))
        if self.tasks_html.index(url) != len(self.tasks) - 1:
            self.answers[self.tasks_html.index(url)] = self.line.text()
            self.line.setText(self.answers[self.tasks_html.index(url) + 1])
            self.text.load(
                QtCore.QUrl.fromLocalFile(self.tasks_html[self.tasks_html.index(url) + 1]))
            self.label.setText(str(self.tasks[self.tasks_html.index(url) + 1].number_of_task))

    def backward(self):
        url = os.path.normcase(os.path.normpath(self.text.url().toLocalFile()))
        if self.tasks_html.index(url) != 0:
            self.answers[self.tasks_html.index(url)] = self.line.text()
            self.line.setText(self.answers[self.tasks_html.index(url) - 1])
            self.text.load(
                QtCore.QUrl.fromLocalFile(self.tasks_html[self.tasks_html.index(url) - 1]))
            self.label.setText(str(self.tasks[self.tasks_html.index(url) - 1].number_of_task))

    def checking(self):
        warn = QtWidgets.QMessageBox.warning(self, 'Вы уверены?',
                                             'Хотите закончить тест прямо сейчас?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if warn == QtWidgets.QMessageBox.Yes:
            url = os.path.normcase(os.path.normpath(self.text.url().toLocalFile()))
            self.answers[self.tasks_html.index(url)] = self.line.text()
            self.parent().ControlUI(self.tasks, self.tasks_html, self.answers)


class Opening(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Opening, self).__init__(parent)

    def setupUI(self):
        self.openinglayout = QtWidgets.QGridLayout()

        self.openingframe = QtWidgets.QFrame()

        self.openingframe.setFrameShape(QtWidgets.QFrame.Box)
        self.vframe = QtWidgets.QVBoxLayout()
        self.clock = QtWidgets.QLCDNumber(5)
        self.clock.display('40:00')
        self.list = QtWidgets.QListWidget()

        self.btn = QtWidgets.QPushButton('Начать')

        for x in os.listdir(resource_path(r'resourses\control')):
            item = QtWidgets.QListWidgetItem(self.list)
            item.setText(x)

        self.openingframe.setStyleSheet('background-color: rgb(211,200,211);')
        self.btn.setStyleSheet('background-color: rgb(255,255,255);')
        self.clock.setStyleSheet('background-color: rgb(0,20,20);')

        self.openingframe.setLayout(self.vframe)
        self.vframe.addWidget(self.clock)
        self.vframe.addWidget(self.list)
        self.vframe.addWidget(self.btn)

        self.openinglayout.setRowStretch(0, 1)
        self.openinglayout.setRowStretch(2, 1)
        self.openinglayout.setColumnStretch(0, 1)
        self.openinglayout.setColumnStretch(2, 1)

        self.openinglayout.addWidget(self.openingframe, 1, 1)

        self.setLayout(self.openinglayout)


class ControlWindow(QtWidgets.QMainWindow):
    def __init__(self, cls):  # инициализация
        super().__init__()
        self.cls = cls
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Тренажер: Контроль")
        self.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))

        # установка фонового изображения и шрифта
        font_db = QtGui.QFontDatabase()
        font_id = font_db.addApplicationFont(resource_path("resourses\Handelson-FourCYR.otf"))
        self.label_font = QtGui.QFont("Handelson FourCYR", 20)

        image = QtGui.QImage(resource_path(r'resourses\pictures\background.png'))
        self.mainPalette = QtGui.QPalette()
        self.mainPalette.setBrush(10, QtGui.QBrush(image))
        self.setPalette(self.mainPalette)

        self.Opening = Opening(self)
        self.Test = Test(self)
        self.Control = Control(self)
        self.OpeningUI()

        self.indicator = 'passive'

    def beginTest(self):
        if self.Opening.list.selectedItems() != []:
            self.t = self.Opening.list.currentItem().text()
            dialog = Ui_Dialog()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.complexity = {'Простой': 0, 'Нормальный': 1, 'Сложный': 2}[dialog.r]
                self.indicator = 'active'
                self.n = {0: 4, 1: 5, 2: 6}[self.complexity]

                # import module

                spec = util.spec_from_file_location('production',
                                                    resource_path("resourses/control/{}/production.py".format(self.t)))
                self.module = util.module_from_spec(spec)
                spec.loader.exec_module(self.module)

                self.tasks = [self.module.Task(self.complexity, random.choice(self.module.TASKS), x)
                              for x in range(1, self.n + 1)]

                for i in self.tasks:
                    i.produce()
                    i.solve()
                    i.display()

                self.tasks_html = [resource_path(
                    r'resourses\control\{}\{}_{}.html'.format(self.t, i.taskname, i.number_of_task)) for i in
                                   self.tasks]

                self.tasks_answers_html = [
                    resource_path(
                        r'resourses\control\{}\{}_answer_{}.html'.format(self.t, i.taskname, i.number_of_task))
                    for
                    i in self.tasks]


                self.TestUI()
        else:
            self.warn = QtWidgets.QMessageBox(None)
            self.warn.setWindowIcon(QtGui.QIcon(resource_path('resourses\pictures\cartesiano.ico')))
            self.warn.setIcon(QtWidgets.QMessageBox.Critical)
            self.warn.setText('Сперва выберите тест!')
            self.warn.setWindowTitle('Что-то не так...')
            self.warn.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.warn.exec_()

    def closeEvent(self, event):
        if self.indicator == 'active':
            warn = QtWidgets.QMessageBox.warning(self, 'Вы уверены?',
                                                 'Хотите ли вы выйти из программы?',
                                                 QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if warn == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            else:
                if hasattr(self, 'tasks_html') == True:
                    for i in self.tasks_html:
                        if os.path.isfile(i) == True:
                            os.remove(i)
                            svg = os.path.splitext(i)[0] + '.svg'
                            if os.path.isfile(svg) == True:
                                os.remove(svg)
                if hasattr(self, 'tasks_answers_html') == True:
                    for j in self.tasks_answers_html:
                        if os.path.isfile(j) == True:
                            os.remove(j)
                self.cls.show()
                event.accept()

    def OpeningUI(self):
        self.setCentralWidget(self.Opening)
        self.Opening.setupUI()
        self.Opening.btn.clicked.connect(self.beginTest)
        self.showMaximized()

    def TestUI(self):
        self.setCentralWidget(self.Test)
        self.Test.setupUI()
        self.showMaximized()

    def ControlUI(self, t, t_h, a):
        self.tasks = t
        self.tasks_html = t_h
        self.answers = a
        self.setCentralWidget(self.Control)
        self.Control.setupUI()
        self.showMaximized()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = ControlWindow(None)
    try:
        sys.exit(app.exec_())
    except Exception:
        if hasattr(win, 'tasks_html') == True:
            for i in win.tasks_html:
                if os.path.isfile(i) == True:
                    os.remove(i)
                    svg = os.path.splitext(i)[0] + '.svg'
                    if os.path.isfile(svg) == True:
                        os.remove(svg)
        if hasattr(win, 'tasks_answers_html') == True:
            for j in win.tasks_answers_html:
                if os.path.isfile(j) == True:
                    os.remove(j)
        sys.exit()
