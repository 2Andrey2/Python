import sys
import asyncio
from functools import partial
from os import mkdir

#import pylab
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from downloader import downloader_async
from mainwin import Ui_MainWindow



def size_format(num):
    for prefix in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "{:.2f}{}B".format(num, prefix)
        num /= 1024.0
    return "{:2f}{}B".format(num, 'Y')


def time_format(time):
    s, ms = str(time).split('.')
    return '{}s {}m'.format(s, ms[:3])


class MyForm(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # для удобства помещаем элементы интерфейса
        # в массив
        self.progress_bars = (self.ui.progress1,
                              self.ui.progress2,
                              self.ui.progress3)

        self.url_edits = (self.ui.url1,
                          self.ui.url2,
                          self.ui.url3)

    def start_downloading(self):
        self.prepare_downloads_dir()
        # получаем URL-адреса из текстовых полей
        urls = [e.text() for e in self.url_edits]
        self.enable_progress_bars()
        self.init_downloaders(urls)
        self.start_downloaders()
        self.show_statistics()

    def update(self, progress_bar, percentage):
        progress_bar.setProperty('value', percentage * 100)
        pass

    def show_statistics(self):
        # два подграфика
        f, (ax1, ax2) = pylab.subplots(1, 2)
        # устанавливаем размеры фигуры (окна вывода)
        f.set_size_inches((10, 6))

        # получаем прошедшее время для каждого загрузчика
        timedeltas = [t.timedelta.total_seconds()
                      for t in self.downloaders]
        # столбчатая диаграмма с 0..len по оси x
        # и временем по оси y
        ax1.bar(range(len(self.downloaders)), timedeltas)

        # устанавливаем метки с названиями файлов для 0..len по оси x
        ax1.set_xticks(range(len(self.downloaders)))
        ax1.set_xticklabels([t.filename for t in self.downloaders])
        ax1.set_yticks(timedeltas)
        ax1.set_yticklabels(map(time_format, timedeltas))
        # название графика
        ax1.set_title('Download time plot')
        # подписи
        ax1.set_xlabel('Files')
        ax1.set_ylabel('Download time')

        # секторная диаграмма
        ax2.pie([t.file_size for t in self.downloaders],
                labels=['{}\n[{}]'.format(t.filename,
                                          size_format(t.file_size))
                for t in self.downloaders])
        ax2.set_title('File size')

        # отображаем фигуру
        f.show()
        # закрываем окно загрузки
        self.close()

    def prepare_downloads_dir(self):
        try:
            mkdir('downloads')
        except FileExistsError:
            pass

    def enable_progress_bars(self):
        for p in self.progress_bars:
            p.setEnabled(True)

    def init_downloaders(self, urls):
        self.downloaders = [downloader_async(url,
                                             partial(self.update,
                                                     progress_bar))
                            for url, progress_bar
                            in zip(urls, self.progress_bars)]

    def start_downloaders(self):
        tasks = [t() for t in self.downloaders]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        form = MyForm()
        form.show()
    except Exception as be:
        print(be)
    try:
        sys.exit(app.exec_())
    except SystemExit as se:
        print('Program has exited with code {}'.format(se))
