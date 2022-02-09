"""
An application for creating and managing questions and building exams and similar documents.
..  :copyright: (c) 2022 by Thiago Marcilon.
..  :license: GPL 3, see LICENSE for more details.
"""
import sys
from gui.main_window import *
import asyncio
import qasync
import common.settings as setts


def run():
    setts.load()
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()


if __name__ == '__main__':
    run()
