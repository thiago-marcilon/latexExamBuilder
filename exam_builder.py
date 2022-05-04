"""
An application for creating and managing questions and building exams and similar documents.
..  :copyright: (c) 2022 by Thiago Marcilon.
..  :license: GPL 3, see LICENSE for more details.
"""
import shutil
import sys
from gui.main_window import *
import asyncio
import qasync
import common.settings as setts


def cleanup_temp_dirs():
    for obj in os.listdir():
        if obj.startswith('temp_') and obj.endswith('_dir'):
            shutil.rmtree(obj, True)


def run():
    cleanup_temp_dirs()
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
