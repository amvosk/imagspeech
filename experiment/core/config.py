from dataclasses import dataclass

import numpy as np


@dataclass
class Config:
    modality: str
    voice_type: str
    experiment_type: str
    block_index: int
    voice_speed: float
    full_screen: bool
    main_screen: bool
    visual_size: float
    word_rest_time: float
    word_latency_time: float
    # word_memory_time: float
    # word_imag_time: float
    time_cross_covert: float
    time_word_hold_covert: float
    time_word_covert: float
    time_cross_overt: float
    time_word_hold_overt: float
    time_word_overt: float
    time_cross_stimulus: float
    # time_cross_covert = time_cross_covert,
    # time_word_hold_covert = time_word_hold_covert,
    # time_cross_overt = time_cross_overt,
    # time_word_hold_overt = time_word_hold_overt,
    # time_cross_stimulus = time_cross_stimulus,
    stimulus_audial: bool
    stimulus_visual: bool
    word_list_path: str
    word_overt_use: bool
    # word_overt_time: float
    word_set_5: np.array
    word_set_20: np.array


    def _update_modality(self, modality):
        self.modality = modality

    def _update_voice_type(self, voice_type):
        self.voice_type = voice_type

    def _update_experiment_type(self, experiment_type):
        self.experiment_type = experiment_type

    def _update_block_index(self, block_index):
        self.block_index = block_index

    def _update_voice_speed(self, voice_speed):
        self.voice_speed = float(voice_speed)

    def _update_full_screen(self, full_screen):
        self.full_screen = full_screen

    def _update_main_screen(self, main_screen):
        self.main_screen = main_screen

    def _update_visual_size(self, visual_size):
        self.visual_size = float(visual_size)

    def _update_word_rest_time(self, word_rest_time):
        self.word_rest_time = float(word_rest_time)

    def _update_word_latency_time(self, word_latency_time):
        self.word_latency_time = float(word_latency_time)

    def _update_time_cross_covert(self, time_cross_covert):
        self.time_cross_covert = float(time_cross_covert)

    def _update_time_word_hold_covert(self, time_word_hold_covert):
        self.time_word_hold_covert = float(time_word_hold_covert)

    def _update_time_word_covert(self, time_word_covert):
        self.time_word_covert = float(time_word_covert)

    def _update_time_cross_overt(self, time_cross_overt):
        self.time_cross_overt = float(time_cross_overt)

    def _update_time_word_hold_overt(self, time_word_hold_overt):
        self.time_word_hold_overt = float(time_word_hold_overt)

    def _update_time_word_overt(self, time_word_overt):
        self.time_word_overt = float(time_word_overt)

    def _update_time_cross_stimulus(self, time_cross_stimulus):
        self.time_cross_stimulus = float(time_cross_stimulus)

    def _update_stimulus_audial(self, stimulus_audial):
        self.stimulus_audial = stimulus_audial

    def _update_stimulus_visual(self, stimulus_visual):
        self.stimulus_visual = stimulus_visual

    def _update_word_list_path(self, word_list_path):
        self.word_list_path = word_list_path

    def _update_word_overt_use(self, word_overt_use):
        self.word_overt_use = word_overt_use

    # def _update_word_overt_time(self, word_overt_time):
    #     self.word_overt_time = float(word_overt_time)


def create_config(em):
    modality = 'test'
    voice_type = 'Филипп'
    experiment_type = 'contrast' # 'words'
    block_index = 1
    voice_speed = 0.8
    full_screen = False
    main_screen = False
    visual_size = 2

    word_rest_time = 2
    word_latency_time = 1
    time_cross_stimulus = 1
    time_cross_covert = 0
    time_word_hold_covert = 1.5
    time_word_covert = 2
    time_cross_overt = 0
    time_word_hold_overt = 1.5
    time_word_overt = 2

    stimulus_audial = True
    stimulus_visual = False

    word_list_path = '../words/words_v2.txt'

    word_overt_use = True
    # word_set_5 = np.array([730, 657, 518, 801, 375])
    word_set_5 = np.array(
        [30, 37, 292, 231, 279]
    )
    word_set_10 = np.array(
        [657, 859, 292,  45,  30, 56, 208, 231, 306, 706]
    )

    word_set_20 = np.array(
        [507, 136, 691,  64, 242, 932, 262, 810, 657,  30,
         446, 794, 988, 573, 167, 180, 705,   6, 600, 496]
    )


    conf = Config(
        modality=modality,
        voice_type=voice_type,
        experiment_type=experiment_type,
        block_index=block_index,
        voice_speed=voice_speed,
        full_screen=full_screen,
        main_screen=main_screen,
        visual_size=visual_size,
        word_rest_time=word_rest_time,
        word_latency_time=word_latency_time,
        time_cross_stimulus=time_cross_stimulus,
        time_cross_covert=time_cross_covert,
        time_word_hold_covert=time_word_hold_covert,
        time_word_covert=time_word_covert,
        time_cross_overt=time_cross_overt,
        time_word_hold_overt=time_word_hold_overt,
        time_word_overt=time_word_overt,
        stimulus_audial=stimulus_audial,
        stimulus_visual=stimulus_visual,
        word_list_path=word_list_path,
        word_overt_use=word_overt_use,
        word_set_5=word_set_5,
        word_set_20 = word_set_20,
    )

    em.register_handler('update_modality', conf._update_modality)
    em.register_handler('update_voice_type', conf._update_voice_type)
    em.register_handler('update_experiment_type', conf._update_experiment_type)
    em.register_handler('update_block_index', conf._update_block_index)
    em.register_handler('update_voice_speed', conf._update_voice_speed)
    em.register_handler('update_full_screen', conf._update_full_screen)
    em.register_handler('update_main_screen', conf._update_main_screen)
    em.register_handler('update_visual_size', conf._update_visual_size)

    em.register_handler('update_word_rest_time', conf._update_word_rest_time)
    em.register_handler('update_word_latency_time', conf._update_word_latency_time)

    em.register_handler('update_time_cross_covert', conf._update_time_cross_covert)
    em.register_handler('update_time_word_hold_covert', conf._update_time_word_hold_covert)
    em.register_handler('update_time_word_covert', conf._update_time_word_covert)
    em.register_handler('update_time_cross_overt', conf._update_time_cross_overt)
    em.register_handler('update_time_word_hold_overt', conf._update_time_word_hold_overt)
    em.register_handler('update_time_word_overt', conf._update_time_word_overt)
    em.register_handler('update_time_cross_stimulus', conf._update_time_cross_stimulus)

    # em.register_handler('update_word_memory_time', conf._update_word_memory_time)
    # em.register_handler('update_word_imag_time', conf._update_word_imag_time)

    em.register_handler('update_audio_stimulus', conf._update_stimulus_audial)
    em.register_handler('update_video_stimulus', conf._update_stimulus_visual)

    em.register_handler('update_word_list_path', conf._update_word_list_path)

    em.register_handler('update_word_overt_use', conf._update_word_overt_use)
    # em.register_handler('update_word_overt_time', conf._update_word_overt_time)



    return conf