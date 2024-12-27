import copy
import sys
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
# from vispy import scene
from functools import partial
from experiment import Experiment
# from gui.canvas_timeseries import TimeSeriesCanvas
# from gui.canvas_pictures import PicturesCanvas
# from config import LocalConfig


class MainWindow(QtWidgets.QMainWindow):
    timer_process = None

    def __init__(self, config, em):
        super().__init__()
        self.config = config
        self.em = em
        self.experiment = Experiment(config, em)

        self.setWindowTitle("Imaginary Speech")
        # Create the canvases

        self.create_menu_bar()


        # self.control_widget = self.create_control_widget()
        # self.canvas_ecog = scene.SceneCanvas(keys='interactive')

        # widget_brain_lines = QtWidgets.QTabWidget()
        # widget_brain_lines.addTab(self.timeseries.canvas.native, "Time-Series")
        # widget_brain_lines.addTab(self.canvas_spectrum.native, "Spectrum")
        #
        # layout_brain = QtWidgets.QHBoxLayout()
        # widget_brain = QtWidgets.QWidget()
        # widget_brain.setLayout(layout_brain)
        #
        # self.layout_brain_checkbox = QtWidgets.QVBoxLayout()
        # self.widget_brain_checkbox = QtWidgets.QWidget()
        # self.widget_brain_checkbox.setLayout(self.layout_brain_checkbox)
        # self.brain_checkbox = []
        # self.create_brain_checkbox()
        # self.em.register_handler('update config.receiver.channels', self.update_brain_checkbox)
        # # self.em.register_handler('update config.recorder.channels_bad', self._update_parameters)
        # self.em.register_handler('update_brain_checkbox_height', self.update_brain_checkbox_height)
        #
        # # self.widget_brain_checkbox_tab = QtWidgets.QTabWidget()
        # # self.widget_brain_checkbox_tab.addTab(self.widget_brain_checkbox, "Goods")
        #
        # # update_layout_brain_height
        # # self.widget_brain_checkbox.setFixedHeight(1000)
        #
        # widget_splitter_timeseries = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        # # layout_brain.addWidget(widget_checkboxes)
        # # layout_brain.addWidget(list_widget)
        #
        # # widget_results = QtWidgets.QTabWidget()
        # # widget_results.addTab(self.canvas_raster_start.native, "Start")
        # splitter_checkboxes_ecog = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        # splitter_checkboxes_ecog.addWidget(self.widget_brain_checkbox)
        # splitter_checkboxes_ecog.addWidget(widget_brain_lines)
        # scroll_area = QtWidgets.QScrollArea()
        # scroll_area.setWidget(splitter_checkboxes_ecog)
        # scroll_area.setWidgetResizable(True)
        # layout_brain.addWidget(scroll_area)
        #
        # widget_splitter_timeseries.addWidget(widget_brain)
        # widget_splitter_timeseries.addWidget(self.canvas_sound.native)
        # size_brain = int(widget_splitter_timeseries.size().width() * 0.8)
        # size_sound = widget_splitter_timeseries.size().width() - size_brain
        # widget_splitter_timeseries.setSizes([size_brain, size_sound])
        #
        # widget_splitter_images = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        # widget_results = QtWidgets.QTabWidget()
        # widget_results.addTab(self.canvas_raster_start.native, "Start")
        # widget_results.addTab(self.canvas_raster_voice.native, "Voice")
        # widget_splitter_images.addWidget(self.canvas_pictures.canvas.native)
        # widget_splitter_images.addWidget(widget_results)
        # part_pictures = int(widget_splitter_images.size().height() * 0.4)
        # part_results = widget_splitter_images.size().height() - part_pictures
        # widget_splitter_images.setSizes([part_pictures, part_results])
        #
        # widget_splitter_canvases = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        # widget_splitter_canvases.addWidget(widget_splitter_timeseries)
        # widget_splitter_canvases.addWidget(widget_splitter_images)
        # size_timeseries = int(widget_splitter_canvases.size().width() * 0.6)
        # size_results = widget_splitter_canvases.size().width() - size_timeseries
        # widget_splitter_canvases.setSizes([size_timeseries, size_results])

        layout_main = QtWidgets.QVBoxLayout()
        widget_control = self.create_widget_control()
        layout_main.addWidget(widget_control)
        widget_contrast = self.create_widget_contrast()
        layout_main.addWidget(widget_contrast)
        widget_stimulus = self.create_widget_stimulus()
        layout_main.addWidget(widget_stimulus)
        widget_subsets = self.create_widget_subsets()
        layout_main.addWidget(widget_subsets)

        widget_central = QtWidgets.QWidget()
        widget_central.setLayout(layout_main)

        self.setCentralWidget(widget_central)
        # self.showMaximized()
        self.show()




    def create_widget_control(self):
        layout_buttons_control = QtWidgets.QHBoxLayout()
        widget_buttons_control = QtWidgets.QWidget()
        widget_buttons_control.setLayout(layout_buttons_control)

        widget_buttons_modality = self.create_widget_modality()
        layout_buttons_control.addWidget(widget_buttons_modality)

        widget_buttons_voice_type = self.create_widget_voice_type()
        layout_buttons_control.addWidget(widget_buttons_voice_type)

        widget_buttons_voice_speed = self.create_widget_voice_speed()
        layout_buttons_control.addWidget(widget_buttons_voice_speed)


        widget_experiment_design = self.create_widget_experiment_design()
        layout_buttons_control.addWidget(widget_experiment_design)

        layout_experiment_parameters = QtWidgets.QHBoxLayout()
        widget_experiment_parameters = QtWidgets.QWidget()
        widget_experiment_parameters.setLayout(layout_experiment_parameters)
        layout_experiment_parameters.addWidget(self.create_widget_experiment_parameters_context())
        layout_experiment_parameters.addWidget(self.create_widget_experiment_parameters_words())
        layout_buttons_control.addWidget(widget_experiment_parameters)

        widget_window_parameters = self.create_widget_window_parameters()
        layout_buttons_control.addWidget(widget_window_parameters)

        return widget_buttons_control

    def create_widget_modality(self):
        layout_buttons_modality = QtWidgets.QVBoxLayout()
        widget_buttons_modality = QtWidgets.QWidget()
        widget_buttons_modality.setLayout(layout_buttons_modality)

        radio_button_test = QtWidgets.QRadioButton("Test")
        radio_button_ecog = QtWidgets.QRadioButton("ECoG")
        radio_button_meg = QtWidgets.QRadioButton("MEG")

        # Add the radio buttons to the button group
        self.button_group_modality = QtWidgets.QButtonGroup()
        self.button_group_modality.addButton(radio_button_test)
        self.button_group_modality.addButton(radio_button_ecog)
        self.button_group_modality.addButton(radio_button_meg)
        self.button_group_modality.buttonClicked.connect(self.handle_button_group_modality_buttonClicked)
        self.button_group_modality.setExclusive(True)
        radio_button_test.setChecked(True)
        # Set the default button to radio_button_ecog

        layout_buttons_modality.addWidget(radio_button_test)
        layout_buttons_modality.addWidget(radio_button_ecog)
        layout_buttons_modality.addWidget(radio_button_meg)
        return widget_buttons_modality

    def handle_button_group_modality_buttonClicked(self, button):
        self.em.trigger('update_modality', str.lower(button.text()))
        print(self.config.modality)
        print("Button {} was clicked".format(button.text()))



    def create_widget_voice_type(self):
        # layout_buttons_voice_type = QtWidgets.QVBoxLayout()
        layout_buttons_voice_type = QtWidgets.QGridLayout()
        widget_buttons_voice_type = QtWidgets.QWidget()
        widget_buttons_voice_type.setLayout(layout_buttons_voice_type)

        self.button_group_voice_type = QtWidgets.QButtonGroup()
        voice_types_sber = ['Борис', 'Марфа']
        # voice_types_sber = ['Марфа', 'Наталья', 'Борис', 'Тарас', 'Александра', 'Сергей']
        # voice_types_yandex = ['Алена', 'Филипп', 'Ермил', 'Женя', 'Мадирус', 'Оммаж', 'Захар']
        voice_types_yandex = ['Филипп', 'Женя']
        for i, voice_type in enumerate(voice_types_yandex):
            radio_button_voice_type = QtWidgets.QRadioButton(voice_type)
            self.button_group_voice_type.addButton(radio_button_voice_type)
            layout_buttons_voice_type.addWidget(radio_button_voice_type, i, 0)
        for i, voice_type in enumerate(voice_types_sber):
            radio_button_voice_type = QtWidgets.QRadioButton(voice_type)
            self.button_group_voice_type.addButton(radio_button_voice_type)
            layout_buttons_voice_type.addWidget(radio_button_voice_type, i, 1)
        self.button_group_voice_type.buttons()[0].setChecked(True)
        self.button_group_voice_type.buttonClicked.connect(self.handle_button_group_voice_type_buttonClicked)

        return widget_buttons_voice_type

    def handle_button_group_voice_type_buttonClicked(self, button):
        self.em.trigger('update_voice_type', button.text())
        print(self.config.voice_type)
        print("Button {} was clicked".format(button.text()))

    def create_widget_voice_speed(self):
        layout_buttons_voice_speed = QtWidgets.QVBoxLayout()
        widget_buttons_voice_speed = QtWidgets.QWidget()
        widget_buttons_voice_speed.setLayout(layout_buttons_voice_speed)

        self.button_group_voice_speed = QtWidgets.QButtonGroup()
        # voice_speeds = ['0.5', '0.6', '0.7', '0.8', '0.9', '1']
        voice_speeds = ['0.7', '0.8', '0.9', '1']
        # radio_button_voice_speeds = []
        for voice_speed in voice_speeds:
            radio_button_voice_speed = QtWidgets.QRadioButton(voice_speed)
            # radio_button_voice_speeds.append(radio_button_voice_speed)
            self.button_group_voice_speed.addButton(radio_button_voice_speed)
            layout_buttons_voice_speed.addWidget(radio_button_voice_speed)
        self.button_group_voice_speed.buttonClicked.connect(self.handle_button_group_voice_speed_buttonClicked)
        # radio_button_voice_speeds[0].setChecked(True)
        # self.button_group_voice_type.buttons()[0].setChecked(True)
        self.button_group_voice_speed.buttons()[1].setChecked(True)
        return widget_buttons_voice_speed

    def handle_button_group_voice_speed_buttonClicked(self, button):
        self.em.trigger('update_voice_speed', button.text())
        print("Button {} was clicked".format(button.text()))


    def create_widget_experiment_design(self):
        layout_experiment_design = QtWidgets.QVBoxLayout()
        widget_experiment_design = QtWidgets.QWidget()
        widget_experiment_design.setLayout(layout_experiment_design)

        checkbox_stimulus_audial = QtWidgets.QCheckBox("audial stimulus")
        checkbox_stimulus_audial.setChecked(self.config.stimulus_audial)
        checkbox_stimulus_audial.stateChanged.connect(self.handle_checkbox_stimulus_audial_stateChanged)
        layout_experiment_design.addWidget(checkbox_stimulus_audial)

        checkbox_stimulus_visual = QtWidgets.QCheckBox("visual stimulus")
        checkbox_stimulus_visual.setChecked(self.config.stimulus_visual)
        checkbox_stimulus_visual.stateChanged.connect(self.handle_checkbox_stimulus_visual_stateChanged)
        layout_experiment_design.addWidget(checkbox_stimulus_visual)

        checkbox_word_overt_use = QtWidgets.QCheckBox("overt")
        checkbox_word_overt_use.setChecked(self.config.word_overt_use)
        checkbox_word_overt_use.stateChanged.connect(self.handle_checkbox_word_overt_use_stateChanged)
        layout_experiment_design.addWidget(checkbox_word_overt_use)

        return widget_experiment_design

    def handle_checkbox_stimulus_audial_stateChanged(self, state):
        self.em.trigger('update_audio_stimulus', state)

    def handle_checkbox_stimulus_visual_stateChanged(self, state):
        self.em.trigger('update_video_stimulus', state)

    def handle_checkbox_word_overt_use_stateChanged(self, state):
        self.em.trigger('update_word_overt_use', state)



    def create_widget_experiment_parameters_context(self):
        layout_experiment_parameters_context = QtWidgets.QVBoxLayout()
        widget_experiment_parameters_context = QtWidgets.QWidget()
        widget_experiment_parameters_context.setLayout(layout_experiment_parameters_context)
        return widget_experiment_parameters_context


    def create_widget_experiment_parameters_words(self):
        layout_experiment_parameters_words = QtWidgets.QVBoxLayout()
        widget_experiment_parameters_words = QtWidgets.QWidget()
        widget_experiment_parameters_words.setLayout(layout_experiment_parameters_words)


        layout_form = QtWidgets.QFormLayout()
        widget_form = QtWidgets.QWidget()
        widget_form.setLayout(layout_form)
        widget_form.setFixedWidth(200)
        layout_experiment_parameters_words.addWidget(widget_form)

        line_word_rest_time = QtWidgets.QLineEdit()
        line_word_rest_time.setText(str(self.config.word_rest_time))
        line_word_rest_time.textChanged.connect(
            partial(self.handle_line_word_rest_time_textChanged, line_word_rest_time)
        )
        layout_form.addRow("word rest time", line_word_rest_time)

        line_word_latency_time = QtWidgets.QLineEdit()
        line_word_latency_time.setText(str(self.config.word_latency_time))
        line_word_latency_time.textChanged.connect(
            partial(self.handle_line_word_latency_time_textChanged, line_word_latency_time)
        )
        layout_form.addRow("word latency time", line_word_latency_time)


        line_time_cross_stimulus = QtWidgets.QLineEdit()
        line_time_cross_stimulus.setText(str(self.config.time_cross_stimulus))
        line_time_cross_stimulus.textChanged.connect(
            partial(self.handle_line_time_cross_stimulus_textChanged, line_time_cross_stimulus)
        )
        layout_form.addRow("cross stimulus", line_time_cross_stimulus)

        line_time_word_hold_covert = QtWidgets.QLineEdit()
        line_time_word_hold_covert.setText(str(self.config.time_word_hold_covert))
        line_time_word_hold_covert.textChanged.connect(
            partial(self.handle_line_time_word_hold_covert_textChanged, line_time_word_hold_covert)
        )
        layout_form.addRow("pause covert", line_time_word_hold_covert)

        line_time_cross_covert = QtWidgets.QLineEdit()
        line_time_cross_covert.setText(str(self.config.time_cross_covert))
        line_time_cross_covert.textChanged.connect(
            partial(self.handle_line_time_cross_covert_textChanged, line_time_cross_covert)
        )
        layout_form.addRow("cross covert", line_time_cross_covert)

        line_time_word_covert = QtWidgets.QLineEdit()
        line_time_word_covert.setText(str(self.config.time_word_covert))
        line_time_word_covert.textChanged.connect(
            partial(self.handle_line_time_word_covert_textChanged, line_time_word_covert)
        )
        layout_form.addRow("rect covert", line_time_word_covert)

        line_time_word_hold_overt = QtWidgets.QLineEdit()
        line_time_word_hold_overt.setText(str(self.config.time_word_hold_overt))
        line_time_word_hold_overt.textChanged.connect(
            partial(self.handle_line_time_word_hold_overt_textChanged, line_time_word_hold_overt)
        )
        layout_form.addRow("pause overt", line_time_word_hold_overt)

        line_time_cross_overt = QtWidgets.QLineEdit()
        line_time_cross_overt.setText(str(self.config.time_cross_overt))
        line_time_cross_overt.textChanged.connect(
            partial(self.handle_line_time_cross_overt_textChanged, line_time_cross_overt)
        )
        layout_form.addRow("cross overt", line_time_cross_overt)

        line_time_word_overt = QtWidgets.QLineEdit()
        line_time_word_overt.setText(str(self.config.time_word_overt))
        line_time_word_overt.textChanged.connect(
            partial(self.handle_line_time_word_overt_textChanged, line_time_word_overt)
        )
        layout_form.addRow("rect overt", line_time_word_overt)

        # line_word_imag_time = QtWidgets.QLineEdit()
        # line_word_imag_time.setText(str(self.config.word_imag_time))
        # line_word_imag_time.textChanged.connect(
        #     partial(self.handle_line_word_imag_time_textChanged, line_word_imag_time)
        # )
        # layout_form.addRow("word imag time", line_word_imag_time)

        return widget_experiment_parameters_words

    def handle_line_word_rest_time_textChanged(self, word_rest_time):
        self.em.trigger('update_word_rest_time', word_rest_time.text())

    def handle_line_word_latency_time_textChanged(self, word_latency_time):
        self.em.trigger('update_word_latency_time', word_latency_time.text())

    def handle_line_time_cross_stimulus_textChanged(self, line_time_cross_stimulus):
        self.em.trigger('update_time_cross_stimulus', line_time_cross_stimulus.text())

    def handle_line_time_word_hold_covert_textChanged(self, line_time_word_hold_covert):
        self.em.trigger('update_time_word_hold_covert', line_time_word_hold_covert.text())

    def handle_line_time_cross_covert_textChanged(self, line_time_cross_covert):
        self.em.trigger('update_time_cross_covert', line_time_cross_covert.text())

    def handle_line_time_word_covert_textChanged(self, line_time_word_covert):
        self.em.trigger('update_time_word_covert', line_time_word_covert.text())

    def handle_line_time_word_hold_overt_textChanged(self, line_time_word_hold_overt):
        self.em.trigger('update_time_word_hold_overt', line_time_word_hold_overt.text())

    def handle_line_time_cross_overt_textChanged(self, line_time_cross_overt):
        self.em.trigger('update_time_cross_overt', line_time_cross_overt.text())

    def handle_line_time_word_overt_textChanged(self, line_time_word_overt):
        self.em.trigger('update_time_word_overt', line_time_word_overt.text())



    def create_widget_window_parameters(self):
        layout_window_parameters = QtWidgets.QVBoxLayout()
        widget_window_parameters = QtWidgets.QWidget()
        widget_window_parameters.setLayout(layout_window_parameters)

        checkbox_fullscreen = QtWidgets.QCheckBox("fullscreen")
        checkbox_fullscreen.setChecked(self.config.full_screen)
        checkbox_fullscreen.stateChanged.connect(self.handle_checkbox_fullscreen_stateChanged)
        layout_window_parameters.addWidget(checkbox_fullscreen)

        checkbox_mainscreen = QtWidgets.QCheckBox("main screen")
        checkbox_mainscreen.setChecked(self.config.main_screen)
        checkbox_mainscreen.stateChanged.connect(self.handle_checkbox_mainscreen_stateChanged)
        layout_window_parameters.addWidget(checkbox_mainscreen)


        layout_form = QtWidgets.QFormLayout()
        widget_form = QtWidgets.QWidget()
        widget_form.setLayout(layout_form)
        layout_window_parameters.addWidget(widget_form)

        line_visual_size = QtWidgets.QLineEdit()
        line_visual_size.setText(str(self.config.visual_size))
        line_visual_size.textChanged.connect(partial(self.handle_line_visual_size_textChanged,line_visual_size))
        layout_form.addRow("size", line_visual_size)

        widget_window_parameters.setFixedWidth(200)
        return widget_window_parameters


    def handle_checkbox_fullscreen_stateChanged(self, state):
        self.em.trigger('update_full_screen', state)

    def handle_checkbox_mainscreen_stateChanged(self, state):
        self.em.trigger('update_main_screen', state)

    def handle_line_visual_size_textChanged(self, line_visual_size):
        self.em.trigger('update_visual_size', line_visual_size.text())



    def create_widget_contrast(self):
        layout_buttons_contrast = QtWidgets.QGridLayout()
        widget_buttons_contrast = QtWidgets.QWidget()
        widget_buttons_contrast.setLayout(layout_buttons_contrast)

        # for i in range(4):
        i = 0
        for j in range(6):
            block_index = j
            button_contrast = QtWidgets.QPushButton("Text {}".format(block_index + 1))
            button_contrast.setCheckable(True)
            button_contrast.setChecked(False)
            self.em.register_handler(
                'buttons_uncheck',
                partial(self.handle_buttons_uncheck, button_contrast)
            )
            button_contrast.toggled.connect(
                partial(self.handle_button_contrast_toggled, button_contrast, block_index)
            )
            layout_buttons_contrast.addWidget(button_contrast, i, j)
        return widget_buttons_contrast


    def create_widget_subsets(self):
        layout_buttons_subsets = QtWidgets.QVBoxLayout()
        widget_buttons_subsets = QtWidgets.QWidget()
        widget_buttons_subsets.setLayout(layout_buttons_subsets)

        button_subset5 = QtWidgets.QPushButton("Text {}".format(5))
        button_subset5.setCheckable(True)
        button_subset5.setChecked(False)
        self.em.register_handler(
            'buttons_uncheck',
            partial(self.handle_buttons_uncheck, button_subset5)
        )
        button_subset5.toggled.connect(
            partial(self.handle_button_subset5_toggled, button_subset5)
        )
        layout_buttons_subsets.addWidget(button_subset5)

        button_subset20 = QtWidgets.QPushButton("Text {}".format(20))
        button_subset20.setCheckable(True)
        button_subset20.setChecked(False)
        self.em.register_handler(
            'buttons_uncheck',
            partial(self.handle_buttons_uncheck, button_subset20)
        )
        button_subset20.toggled.connect(
            partial(self.handle_button_subset20_toggled, button_subset20)
        )
        layout_buttons_subsets.addWidget(button_subset20)

        return widget_buttons_subsets


    def handle_button_contrast_toggled(self, button, block_index, checked):
        if checked:
            self.em.trigger('experiment.stop')
            self.em.trigger('buttons_uncheck', button)
            button.setStyleSheet("background-color: blue; color: white;")
            print('Text {}'.format(block_index + 1))
            self.em.trigger('update_experiment_type', 'text_full')
            self.em.trigger('update_block_index', block_index)
            self.em.trigger('experiment.start')
        else:
            button.setStyleSheet("")
            self.em.trigger('experiment.stop')

    def handle_button_subset5_toggled(self, button, checked):
        if checked:
            self.em.trigger('experiment.stop')
            self.em.trigger('buttons_uncheck', button)
            button.setStyleSheet("background-color: blue; color: white;")
            print('Subset {}'.format(1))
            self.em.trigger('update_experiment_type', 'subset5')
            self.em.trigger('update_block_index', 0)
            self.em.trigger('experiment.start')
        else:
            button.setStyleSheet("")
            self.em.trigger('experiment.stop')

    def handle_button_subset20_toggled(self, button, checked):
        if checked:
            self.em.trigger('experiment.stop')
            self.em.trigger('buttons_uncheck', button)
            button.setStyleSheet("background-color: blue; color: white;")
            print('Subset {}'.format(1))
            self.em.trigger('update_experiment_type', 'subset20')
            self.em.trigger('update_block_index', 0)
            self.em.trigger('experiment.start')
        else:
            button.setStyleSheet("")
            self.em.trigger('experiment.stop')


    def create_widget_stimulus(self):
        layout_buttons_stimulus = QtWidgets.QGridLayout()
        widget_buttons_stimulus = QtWidgets.QWidget()
        widget_buttons_stimulus.setLayout(layout_buttons_stimulus)

        for i in range(4):
            for j in range(5):
                block_index = i*5 + j
                button_stimulus = QtWidgets.QPushButton("Words {}".format(block_index + 1))
                button_stimulus.setCheckable(True)
                button_stimulus.setChecked(False)
                self.em.register_handler(
                    'buttons_uncheck',
                    partial(self.handle_buttons_uncheck, button_stimulus)
                )
                button_stimulus.toggled.connect(
                    partial(self.handle_button_stimulus_toggled, button_stimulus, block_index)
                )
                layout_buttons_stimulus.addWidget(button_stimulus, i, j)
        return widget_buttons_stimulus

    def handle_buttons_uncheck(self, button, button_trigger):
        if button.isChecked() and button != button_trigger:
            button.setChecked(False)

    def handle_button_stimulus_toggled(self, button, block_index, checked):
        if checked:
            self.em.trigger('experiment.stop')
            self.em.trigger('buttons_uncheck', button)
            button.setStyleSheet("background-color: blue; color: white;")
            print('Words {}'.format(block_index+1))
            self.em.trigger('update_experiment_type', 'words')
            self.em.trigger('update_block_index', block_index)
            self.em.trigger('experiment.start')
        else:
            button.setStyleSheet("")
            self.em.trigger('experiment.stop')



    # def closeEvent(self, event):
    #     # Call your function here
    #     if self.receiver is not None:
    #         self.receiver.disconnect()
    #     if self.generator_lsl is not None:
    #         self.generator_lsl.stop()
    #     # Accept the close event to close the window
    #     event.accept()

    def handle_currentTextChanged_amplifier(self, field_ip_address, amplifier):
        if amplifier.currentText() == "EBNeuro_BePLusLTM":
            field_ip_address.setVisible(True)
        else:
            field_ip_address.setVisible(False)
        # self.config.receiver.update_amplifier(self.em, amplifier.currentText())
        # print('handle_currentTextChanged_amplifier')
        self.em.trigger('update config.receiver.amplifier', amplifier.currentText())
        # print(self.em.handlers['update config.receiver.amplifier'])

    def handle_textChanged_ip_address(self, ip_address):
        # self.config.receiver.update_amplifier_ip(ip_address.text())
        self.em.trigger('update config.receiver.amplifier_ip', ip_address.text())

    def handle_textChanged_fs(self, fs):
        # self.config.receiver.update_fs(self.em, fs.text())
        self.em.trigger('update config.receiver.fs', fs.text())

    # def handle_buttonClicked_debug_mode(self, button, debug_mode):
    #     self.config.general.update_debug_mode(debug_mode)

    def create_brain_checkbox(self):
        while self.layout_brain_checkbox.count():
            child = self.layout_brain_checkbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.brain_checkbox = []
        for index, state in enumerate(self.config.receiver.channels):
            if state:
                checkbox = QtWidgets.QCheckBox("{}".format(index + 1))
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(
                    lambda state, index=index: self.handle_stateChanged_brain_checkbox(state, index)
                )
                # checkbox.stateChanged.connect(lambda state, index=i: self.handle_checkbox_state_changed(state, index))
                self.brain_checkbox.append(checkbox)
                self.layout_brain_checkbox.addWidget(checkbox)

    def update_brain_checkbox(self, args):
        # self.config.receiver = copy.deepcopy(config_receiver)
        for i, state in enumerate(self.config.receiver.channels):
            checkbox = self.brain_checkbox[i]
            # checkbox.setChecked(state)
            checkbox.setVisible(state)
            # if not self.config.recorder.channels_bad[i]:

    # def _update_parameters(self, config_recorder):
    #     self.config.recorder = copy.deepcopy(config_recorder)
    # print(self.config.recorder.channels_bad)

    def handle_stateChanged_brain_checkbox(self, state, index):
        # self.config.recorder.update_channels_bad(self.em, index, state)
        self.em.trigger('update config.recorder.channels_bad', (index, state))
        # print(self.config.recorder.channels_bad)

    def update_brain_checkbox_height(self, height):
        self.widget_brain_checkbox.setFixedHeight(height)

    def handle_button_generator_lsl(self, button, checked):
        if checked:
            button.setStyleSheet("background-color: blue; color: white;")
            self.generator_lsl = GeneratorLSL(self.config, self.em)
            self.generator_lsl.start()
        else:
            button.setStyleSheet("")
            self.generator_lsl.stop()
            self.generator_lsl = None

    def handle_button_connect(self, button, layout_receiver, checked):
        if checked:
            button.setStyleSheet("background-color: blue; color: white;")
            for i in range(layout_receiver.count()):
                widget = layout_receiver.itemAt(i).widget()
                if widget.objectName() not in ["connect_button", 'receiver_label']:
                    widget.setDisabled(True)
            self.receiver = Receiver(self.config, self.em)
            self.receiver.connect()

            self.processor.set_receiver_queue_input(self.receiver.queue_input)
            self.processor.set_receiver_queue_output(self.receiver.queue_output)
            self.timer_connect = QtCore.QTimer(self)
            self.timer_connect.timeout.connect(partial(self.processor.on_timer, self.timeseries.update_data))
            self.timer_connect.start(30)
        else:
            button.setStyleSheet("")
            for i in range(layout_receiver.count()):
                widget = layout_receiver.itemAt(i).widget()
                if widget.objectName() not in ["connect_button", 'receiver_label']:
                    widget.setDisabled(False)
            self.timer_connect.stop()
            self.timer_connect = None
            self.receiver.disconnect()
            self.receiver = None
            self.processor.set_receiver_queue_input(None)
            self.processor.set_receiver_queue_output(None)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # Create the "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create the "Help" menu
        help_menu = menu_bar.addMenu("Help")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        help_menu.addAction("About")

    def create_control_widget(self):
        control_layout = QtWidgets.QVBoxLayout()
        control_layout.setSpacing(10)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # control_layout.addStretch()

        widget_patient_info = self.create_patient_info_widget()
        control_layout.addWidget(widget_patient_info)

        widget_general = self.create_general_widget()
        control_layout.addWidget(widget_general)

        widget_receiver = self.create_receiver_widget()
        control_layout.addWidget(widget_receiver)

        widget_experiment = self.create_experiment_widget()
        control_layout.addWidget(widget_experiment)

        control_widget = QtWidgets.QWidget()
        control_widget.setLayout(control_layout)
        control_widget.setFixedWidth(250)
        return control_widget

    def create_patient_info_widget(self):
        layout_patient_info = QtWidgets.QVBoxLayout()
        widget_patient_info = QtWidgets.QWidget()
        widget_patient_info.setLayout(layout_patient_info)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout_patient_info.addWidget(separator)

        label_patient_name = QtWidgets.QLabel("Patient Info")
        layout_patient_info.addWidget(label_patient_name)

        layout_patient_values = QtWidgets.QFormLayout()
        widget_patient_values = QtWidgets.QWidget()
        widget_patient_values.setLayout(layout_patient_values)
        layout_patient_info.addWidget(widget_patient_values)

        line_patient_name = QtWidgets.QLineEdit()
        line_patient_name.setText(str(self.config.patient_info.patient_name))
        line_patient_name.textChanged.connect(partial(self.handle_patient_name_textChanged, line_patient_name))
        layout_patient_values.addRow("patient name", line_patient_name)

        line_patient_data_path = QtWidgets.QLineEdit()
        line_patient_data_path.setText(str(self.config.paths.patient_data_path))
        line_patient_data_path.setEnabled(False)
        # line_patient_data_path.textChanged.connect(partial(self.handle_patient_name_textChanged, line_patient_data_path))
        layout_patient_values.addRow("patient data", line_patient_data_path)

        return widget_patient_info

    def handle_patient_name_textChanged(self, line_patient_name):
        self.em.trigger('update config.patient_info.patient_name', line_patient_name.text())

    def create_general_widget(self):
        layout_general = QtWidgets.QVBoxLayout()
        widget_general = QtWidgets.QWidget()
        widget_general.setLayout(layout_general)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout_general.addWidget(separator)

        label_general = QtWidgets.QLabel("General")
        layout_general.addWidget(label_general)

        button_generator_lsl = QtWidgets.QPushButton("GeneratorLSL")
        button_generator_lsl.setCheckable(True)
        button_generator_lsl.setChecked(False)
        button_generator_lsl.toggled.connect(partial(self.handle_button_generator_lsl, button_generator_lsl))
        layout_general.addWidget(button_generator_lsl)

        return widget_general

    def create_receiver_widget(self):
        layout_receiver = QtWidgets.QVBoxLayout()
        widget_receiver = QtWidgets.QWidget()
        widget_receiver.setLayout(layout_receiver)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout_receiver.addWidget(separator)

        label_receiver = QtWidgets.QLabel("Receiver")
        label_receiver.setObjectName("receiver_label")
        layout_receiver.addWidget(label_receiver)

        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        layout_receiver.addWidget(form_widget)

        self.amplifiers = [self.config.receiver.amplifier] + self.amplifiers
        selection_amplifier = QtWidgets.QComboBox()
        for amplifier in self.amplifiers:
            selection_amplifier.addItem(amplifier)
        field_ip_address = QtWidgets.QLineEdit()
        selection_amplifier.currentTextChanged.connect(
            partial(self.handle_currentTextChanged_amplifier, field_ip_address, selection_amplifier)
        )
        form_layout.addRow("Amp", selection_amplifier)

        selected_amplifier = selection_amplifier.currentText()
        field_ip_address.setText(self.config.receiver.amplifier_ip)
        if selected_amplifier != "EBNeuro_BePLusLTM":
            field_ip_address.setVisible(False)
        field_ip_address.textChanged.connect(partial(self.handle_textChanged_ip_address, field_ip_address))
        form_layout.addRow("IP", field_ip_address)

        field_fs = QtWidgets.QLineEdit()
        field_fs.setText(str(self.config.receiver.fs))
        field_fs.textChanged.connect(partial(self.handle_textChanged_fs, field_fs))
        form_layout.addRow("fs", field_fs)

        button_select_channels = QtWidgets.QPushButton("Select Channels")
        button_select_channels.clicked.connect(
            partial(self.handle_button_select_channels_clicked, button_select_channels, widget_receiver)
        )
        layout_receiver.addWidget(button_select_channels)

        button_connect = QtWidgets.QPushButton("Connect")
        button_connect.setObjectName("connect_button")
        button_connect.setCheckable(True)
        button_connect.setChecked(False)
        button_connect.toggled.connect(partial(self.handle_button_connect, button_connect, layout_receiver))
        layout_receiver.addWidget(button_connect)

        return widget_receiver

    def handle_button_select_channels_clicked(self, button, widget):
        select_channels_window = SelectChannelsWindow(self.em, self.config)
        select_channels_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        x = widget.geometry().x() + widget.geometry().width()
        # y = button.geometry().y() + int(select_channels_window.geometry().height() / 2)
        y = widget.geometry().y()
        select_channels_window.move(x, y)
        select_channels_window.setWindowFlags(
            select_channels_window.windowFlags() | QtCore.Qt.WindowType.CustomizeWindowHint)
        select_channels_window.setWindowFlags(
            select_channels_window.windowFlags() & ~QtCore.Qt.WindowType.WindowCloseButtonHint)
        select_channels_window.show()

    def create_experiment_widget(self):
        layout_experiment = QtWidgets.QVBoxLayout()
        widget_experiment = QtWidgets.QWidget()
        widget_experiment.setLayout(layout_experiment)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        layout_experiment.addWidget(separator)

        label_experiment = QtWidgets.QLabel("Experiment")
        label_experiment.setObjectName("experiment_label")
        layout_experiment.addWidget(label_experiment)

        button_experiment_parameters = QtWidgets.QPushButton("Parameters")
        button_experiment_parameters.setObjectName("button_experiment_parameters")
        button_experiment_parameters.clicked.connect(
            partial(self.handle_button_experiment_parameters_clicked, button_experiment_parameters, widget_experiment)
        )
        layout_experiment.addWidget(button_experiment_parameters)

        layout_selection_split = QtWidgets.QFormLayout()
        widget_selection_split = QtWidgets.QWidget()
        widget_selection_split.setLayout(layout_selection_split)
        # widget_experiment_parameters_iteration.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout_experiment.addWidget(widget_selection_split)

        selection_split = QtWidgets.QComboBox()
        selection_split.setObjectName("selection_split")
        for i in range(self.config.experiment.n_splits):
            selection_split.addItem(str(i+1))
        selection_split.setCurrentText('1')
        selection_split.currentTextChanged.connect(
            partial(self.handle_selection_split_currentTextChanged, selection_split)
        )
        self.em.register_handler('update selection split', partial(self._reset_selection_split, selection_split))
        self.em.trigger('update selection split')
        self.em.trigger('update local.splits_values', self.stimulus)
        layout_selection_split.addRow("split", selection_split)

        button_experiment_start = QtWidgets.QPushButton("Start")
        button_experiment_start.setObjectName("start_button")
        button_experiment_start.setCheckable(True)
        button_experiment_start.setChecked(False)
        button_experiment_start.setDisabled(False)
        button_experiment_start.toggled.connect(
            partial(self.handle_button_experiment_start, button_experiment_start, layout_experiment)
        )
        layout_experiment.addWidget(button_experiment_start)

        button_experiment_pause = QtWidgets.QPushButton("Pause")
        button_experiment_pause.setObjectName("pause_button")
        button_experiment_pause.setCheckable(True)
        button_experiment_pause.setChecked(True)
        button_experiment_pause.setDisabled(True)
        button_experiment_pause.toggled.connect(
            partial(self.handle_button_experiment_pause, button_experiment_pause, layout_experiment)
        )
        layout_experiment.addWidget(button_experiment_pause)

        return widget_experiment

    def _reset_selection_split(self, selection_split, args):
        selection_split.blockSignals(True)
        selection_split.clear()
        for i in range(self.config.experiment.n_splits):
            selection_split.addItem(str(i+1))
        selection_split.blockSignals(False)
        selection_split.setCurrentText('1')
        self.handle_selection_split_currentTextChanged(selection_split)

    def handle_button_experiment_parameters_clicked(self, button, widget):
        experiment_parameters_window = ExperimentParametersWindow(self.config, self.em, self.stimulus)
        experiment_parameters_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        x = widget.geometry().x() + widget.geometry().width()
        y = widget.geometry().y()
        # y = button.geometry().y()# + int(select_channels_window.geometry().height() / 2)
        experiment_parameters_window.move(x, y)
        experiment_parameters_window.setWindowFlags(
            experiment_parameters_window.windowFlags() | QtCore.Qt.WindowType.CustomizeWindowHint)
        experiment_parameters_window.setWindowFlags(
            experiment_parameters_window.windowFlags() & ~QtCore.Qt.WindowType.WindowCloseButtonHint)
        experiment_parameters_window.show()

    def handle_selection_split_currentTextChanged(self, selection_split):
        self.em.trigger('update local.split', int(selection_split.currentText())-1)
        print('update local.split', int(selection_split.currentText())-1)

    def handle_button_experiment_start(self, button, layout, checked):
        if checked:
            button.setStyleSheet("background-color: blue; color: white;")
            button.setText("Stop")
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget.objectName() in ["pause_button"]:
                    widget.setChecked(False)
                    widget.setDisabled(False)
                if widget.objectName() in ["button_experiment_parameters", 'selection_split']:
                    widget.setDisabled(True)
            self.em.trigger('experiment.start')
            self.timer_experiment = QtCore.QTimer(self)
            self.timer_experiment.timeout.connect(
                partial(self.canvas_pictures.update_image, self.experiment.queue_output))
            self.timer_experiment.start(10)
        else:
            button.setStyleSheet("")
            button.setText("Start")
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if widget.objectName() in ['pause_button']:
                    widget.setChecked(True)
                    widget.setDisabled(True)
                    widget.setStyleSheet("")
                if widget.objectName() in ["button_experiment_parameters", 'selection_split']:
                    widget.setDisabled(False)
            self.em.trigger('experiment.stop')
            self.timer_experiment.stop()
            self.timer_experiment = None


    def handle_button_experiment_pause(self, button, layout, checked):
        if checked:
            button.setStyleSheet("background-color: blue; color: white;")
            self.em.trigger('experiment.pause')
        else:
            button.setStyleSheet("")
            self.em.trigger('experiment.unpause')


class ExperimentParametersWindow(QtWidgets.QDialog):
    def __init__(self, config, em, stimulus):
        super().__init__()
        self.config = config
        self.em = em
        self.stimulus = stimulus
        self.config_experiment = copy.deepcopy(self.config.experiment)
        self.config_experiment_copy = copy.deepcopy(self.config.experiment)
        self.setWindowTitle("Experiment Parameters")

        layout_experiment_parameters_window = QtWidgets.QVBoxLayout()
        self.setLayout(layout_experiment_parameters_window)

        layout_experiment_parameters = QtWidgets.QHBoxLayout()
        widget_experiment_parameters = QtWidgets.QWidget()
        widget_experiment_parameters.setLayout(layout_experiment_parameters)
        layout_experiment_parameters_window.addWidget(widget_experiment_parameters)

        layout_experiment_parameters_task = QtWidgets.QFormLayout()
        widget_experiment_parameters_task = QtWidgets.QWidget()
        widget_experiment_parameters_task.setLayout(layout_experiment_parameters_task)
        # layout_experiment_parameters_task.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout_experiment_parameters.addWidget(widget_experiment_parameters_task)

        stimulus_type = ['object', 'action', 'word', 'sound']
        selection_stimulus_type = QtWidgets.QComboBox()
        for type_ in stimulus_type:
            selection_stimulus_type.addItem(type_)
        selection_stimulus_type.setCurrentText(self.config_experiment.stimulus_type)
        layout_experiment_parameters_task.addRow("type", selection_stimulus_type)

        field_n_stimulus = QtWidgets.QLineEdit()
        field_n_stimulus.setText(str(self.config.experiment.n_stimulus))
        field_n_stimulus.textChanged.connect(partial(self.handle_field_n_stimulus_textChanged, field_n_stimulus))
        layout_experiment_parameters_task.addRow("number", field_n_stimulus)

        stimulus_difficulty = ['easy', 'hard']
        selection_stimulus_difficulty = QtWidgets.QComboBox()
        for difficulty in stimulus_difficulty:
            selection_stimulus_difficulty.addItem(difficulty)
        selection_stimulus_difficulty.setCurrentText(self.config_experiment.stimulus_difficulty)
        selection_stimulus_difficulty.currentTextChanged.connect(
            partial(self.handle_selection_stimulus_difficulty_currentTextChanged, selection_stimulus_difficulty)
        )
        layout_experiment_parameters_task.addRow("difficulty", selection_stimulus_difficulty)

        stimulus_features = [
            'subjective complexity',
            'picture familiarity',
            'noun acquisition age',
            'noun imageability',
            'noun picture agreement',
            'noun frequency'
        ]
        selection_stimulus_features = QtWidgets.QComboBox()
        for feature in stimulus_features:
            selection_stimulus_features.addItem(feature)
        print(' '.join(self.config_experiment.stimulus_feature.split('_')))
        selection_stimulus_features.setCurrentText(' '.join(self.config_experiment.stimulus_feature.split('_')))
        selection_stimulus_features.currentTextChanged.connect(
            partial(self.handle_selection_stimulus_features_currentTextChanged, selection_stimulus_features)
        )
        layout_experiment_parameters_task.addRow("features", selection_stimulus_features)

        layout_experiment_parameters_iteration = QtWidgets.QFormLayout()
        widget_experiment_parameters_iteration = QtWidgets.QWidget()
        widget_experiment_parameters_iteration.setLayout(layout_experiment_parameters_iteration)
        # widget_experiment_parameters_iteration.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout_experiment_parameters.addWidget(widget_experiment_parameters_iteration)

        field_n_splits = QtWidgets.QLineEdit()
        field_n_splits.textChanged.connect(
            partial(self.handle_field_n_splits_textChanged, field_n_splits)
        )
        field_n_splits.setText(str(self.config.experiment.n_splits))
        layout_experiment_parameters_iteration.addRow("number of splits", field_n_splits)

        self.field_stimulus_time = QtWidgets.QLineEdit()
        # field_single_picture_time.setText(str(self.config.experiment.n_stimulus))
        self.field_stimulus_time.textChanged.connect(
            partial(self.handle_field_stimulus_time_textChanged, self.field_stimulus_time)
        )
        layout_experiment_parameters_iteration.addRow("time per stimulus (s)", self.field_stimulus_time)

        self.field_between_time = QtWidgets.QLineEdit()
        # field_between_time.setText(str(self.config.experiment.n_stimulus))
        self.field_between_time.textChanged.connect(
            partial(self.handle_field_between_time_textChanged, self.field_between_time)
        )
        layout_experiment_parameters_iteration.addRow("time between stimulus (s)", self.field_between_time)

        self.handle_selection_stimulus_type_currentTextChanged(selection_stimulus_type)
        selection_stimulus_type.currentTextChanged.connect(
            partial(self.handle_selection_stimulus_type_currentTextChanged, selection_stimulus_type)
        )

        layout_experiment_checkbox = QtWidgets.QHBoxLayout()
        widget_experiment_checkbox = QtWidgets.QWidget()
        widget_experiment_checkbox.setLayout(layout_experiment_checkbox)
        layout_experiment_parameters_iteration.addWidget(widget_experiment_checkbox)

        checkbox_random_intervals = QtWidgets.QCheckBox("random intervals")
        checkbox_random_intervals.setChecked(self.config_experiment.use_random_intervals)
        checkbox_random_intervals.stateChanged.connect(self.handle_checkbox_random_intervals_stateChanged)
        checkbox_random_intervals.setChecked(self.config_experiment.use_random_intervals)
        layout_experiment_checkbox.addWidget(checkbox_random_intervals)

        checkbox_shuffle_stimulus = QtWidgets.QCheckBox("shuffle stimulus")
        checkbox_shuffle_stimulus.setChecked(self.config_experiment.shuffle_stimulus)
        checkbox_shuffle_stimulus.stateChanged.connect(self.handle_checkbox_shuffle_stimulus_stateChanged)
        layout_experiment_checkbox.addWidget(checkbox_shuffle_stimulus)

        widget_out_buttons = self.create_widget_out_buttons()
        layout_experiment_parameters_window.addWidget(widget_out_buttons)


    def handle_selection_stimulus_type_currentTextChanged(self, selection_stimulus_type):
        self.config_experiment.stimulus_type = selection_stimulus_type.currentText()
        for field_name, field_value in vars(self.config_experiment).items():
            if field_name == '{}_time'.format(self.config_experiment.stimulus_type):
                # print(field_name)
                self.field_stimulus_time.setText(str(field_value))
            elif field_name == 'between_{}_time'.format(self.config_experiment.stimulus_type):
                # print(field_name)
                self.field_between_time.setText(str(field_value))


    def handle_field_n_stimulus_textChanged(self, field_n_stimulus):
        self.config_experiment.n_stimulus = field_n_stimulus.text()
        # print(self.config_experiment.stimulus_type)

    def handle_selection_stimulus_difficulty_currentTextChanged(self, selection_stimulus_difficulty):
        self.config_experiment.stimulus_difficulty = selection_stimulus_difficulty.currentText()

    def handle_selection_stimulus_features_currentTextChanged(self, selection_stimulus_features):
        self.config_experiment.stimulus_feature = '_'.join(selection_stimulus_features.currentText().split())
        # print(self.config_experiment.stimulus_feature)

    def handle_field_n_splits_textChanged(self, field_n_splits):
        self.config_experiment.n_splits = field_n_splits.text()

    def handle_field_stimulus_time_textChanged(self, field_stimulus_time):
        setattr(self.config_experiment, '{}_time'.format(self.config_experiment.stimulus_type), field_stimulus_time.text())

    def handle_field_between_time_textChanged(self, field_between_time):
        setattr(self.config_experiment, 'between_{}_time'.format(self.config_experiment.stimulus_type), field_between_time.text())

    def handle_checkbox_random_intervals_stateChanged(self, state):
        self.config_experiment.use_random_intervals = state

    def handle_checkbox_shuffle_stimulus_stateChanged(self, state):
        self.config_experiment.shuffle_stimulus = state

    def create_widget_out_buttons(self):
        layout_out_buttons = QtWidgets.QHBoxLayout()
        widget_out_buttons = QtWidgets.QWidget()
        widget_out_buttons.setLayout(layout_out_buttons)

        button_experiment_parameters_save = QtWidgets.QPushButton("Save")
        button_experiment_parameters_save.clicked.connect(self.handle_clicked_button_experiment_parameters_save)
        layout_out_buttons.addWidget(button_experiment_parameters_save)

        button_experiment_parameters_cancel = QtWidgets.QPushButton("Cancel")
        button_experiment_parameters_cancel.clicked.connect(self.handle_clicked_button_experiment_parameters_cancel)
        layout_out_buttons.addWidget(button_experiment_parameters_cancel)

        button_experiment_parameters_reset = QtWidgets.QPushButton("Reset")
        button_experiment_parameters_reset.clicked.connect(self.handle_clicked_button_experiment_parameters_reset)
        layout_out_buttons.addWidget(button_experiment_parameters_reset)

        return widget_out_buttons

    def handle_clicked_button_experiment_parameters_save(self):
        for field_name, field_value in vars(self.config_experiment).items():
            self.em.trigger('update config.experiment.{}'.format(field_name), field_value)
        self.em.trigger('update config.experiment.n_stimulus_per_split')
        self.em.trigger('update selection split')
        self.em.trigger('update local.splits_values', self.stimulus)
        self.close()

    def handle_clicked_button_experiment_parameters_cancel(self):
        self.close()

    def handle_clicked_button_experiment_parameters_reset(self):
        self.config_experiment = copy.deepcopy(self.config_experiment_copy)



class SelectChannelsWindow(QtWidgets.QDialog):
    checkboxes = []

    def __init__(self, em, config):
        super().__init__()
        self.em = em
        self.config = config
        self.setWindowTitle("Select Channels")
        self.channels_copy = np.copy(self.config.receiver.channels)
        self.channels = np.copy(self.config.receiver.channels)

        layout_select_channels_window = QtWidgets.QVBoxLayout()
        self.setLayout(layout_select_channels_window)

        widget_select_channels_button = self.create_widget_select_channels_button()
        widget_select_channels_checkbox = self.create_widget_select_channels_checkbox()

        layout_select_channels = QtWidgets.QHBoxLayout()
        layout_select_channels.addWidget(widget_select_channels_button)
        layout_select_channels.addWidget(widget_select_channels_checkbox)
        widget_select_channels = QtWidgets.QWidget()
        widget_select_channels.setLayout(layout_select_channels)

        layout_select_channels_window.addWidget(widget_select_channels)

        widget_out_buttons = self.create_widget_out_buttons()
        layout_select_channels_window.addWidget(widget_out_buttons)

    def create_widget_select_channels_button(self):
        layout_select_channels_button = QtWidgets.QVBoxLayout()
        widget_select_channels_button = QtWidgets.QWidget()
        widget_select_channels_button.setLayout(layout_select_channels_button)
        widget_select_channels_button.setFixedWidth(200)
        layout_select_channels_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        button_select_all = QtWidgets.QPushButton("All")
        button_select_all.clicked.connect(self.select_all)
        layout_select_channels_button.addWidget(button_select_all)

        layout_select_custom = QtWidgets.QHBoxLayout()
        widget_select_custom = QtWidgets.QWidget()
        widget_select_custom.setLayout(layout_select_custom)
        low_N = QtWidgets.QLineEdit()
        low_N.setText(str(1))
        high_N = QtWidgets.QLineEdit()
        high_N.setText(str(20))
        button_sellect_N = QtWidgets.QPushButton("N")
        button_sellect_N.clicked.connect(partial(self.select_N, low_N, high_N))
        layout_select_custom.addWidget(button_sellect_N)
        layout_select_custom.addWidget(low_N)
        layout_select_custom.addWidget(high_N)
        layout_select_channels_button.addWidget(widget_select_custom)

        button_select_none = QtWidgets.QPushButton("None")
        button_select_none.clicked.connect(self.select_none)
        layout_select_channels_button.addWidget(button_select_none)
        return widget_select_channels_button

    def create_widget_select_channels_checkbox(self):
        layout_select_channels_checkbox = QtWidgets.QGridLayout()
        widget_select_channels_checkbox = QtWidgets.QWidget()
        widget_select_channels_checkbox.setLayout(layout_select_channels_checkbox)

        self.checkboxes = []
        for i in range(8):
            for j in range(8):
                index = i * 8 + j
                checkbox = QtWidgets.QCheckBox("{}".format(index + 1))
                checkbox.stateChanged.connect(
                    lambda state, index=index: self.handle_checkbox_stateChanged(state, index))
                checkbox.setChecked(self.channels[index])
                self.checkboxes.append(checkbox)
                layout_select_channels_checkbox.addWidget(checkbox, i, j)
        return widget_select_channels_checkbox

    def create_widget_out_buttons(self):
        layout_out_buttons = QtWidgets.QHBoxLayout()
        widget_out_buttons = QtWidgets.QWidget()
        widget_out_buttons.setLayout(layout_out_buttons)

        button_channels_save = QtWidgets.QPushButton("Save")
        button_channels_save.clicked.connect(self.handle_clicked_button_channels_save)
        layout_out_buttons.addWidget(button_channels_save)

        button_channels_cancel = QtWidgets.QPushButton("Cancel")
        button_channels_cancel.clicked.connect(self.handle_clicked_button_channels_cancel)
        layout_out_buttons.addWidget(button_channels_cancel)

        button_channels_reset = QtWidgets.QPushButton("Reset")
        button_channels_reset.clicked.connect(self.handle_clicked_button_channels_reset)
        layout_out_buttons.addWidget(button_channels_reset)

        return widget_out_buttons

    def handle_clicked_button_channels_save(self):
        self.em.trigger('update config.receiver.channels', self.channels)
        self.close()

    def handle_clicked_button_channels_cancel(self):
        self.close()

    def handle_clicked_button_channels_reset(self):
        self.channels = np.copy(self.channels_copy)
        for i, checkbox in enumerate(self.checkboxes):
            checkbox.setChecked(self.channels[i])

    def select_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def select_none(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def select_N(self, low_N, high_N):
        low = int(low_N.text())
        high = int(high_N.text())
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
        for i, checkbox in enumerate(self.checkboxes):
            if low - 1 <= i < high:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def handle_checkbox_stateChanged(self, state, index):
        self.channels[index] = state


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
