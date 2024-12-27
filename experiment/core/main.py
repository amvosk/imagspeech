# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from config import create_config
from event_manager import EventManager
from interface import MainWindow
from PyQt6 import QtWidgets

def main():
    em = EventManager()
    conf = create_config(em)
    # config.receiver.lsl_stream_name = 'GeneratorLSL'

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(conf, em)
    sys.exit(app.exec())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
