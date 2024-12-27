

import scipy.io.wavfile
import numpy as np
from player import AudioPlayer
import psychopy.core
from psychopy import monitors

import copy
import multiprocessing
import psychopy.visual as visual
from functools import partial

from event_manager import EventManager


class Experiment:
    def __init__(self, config, em):
        # initialize basic configuration
        self.config = config
        self.em = em
        self.process = None
        self.stop_event = multiprocessing.Event()
        self.pause_event = multiprocessing.Event()

        self.em.register_handler('experiment.start', self.start)
        self.em.register_handler('experiment.stop', self.stop)
        self.em.register_handler('experiment.pause', self.pause)
        self.em.register_handler('experiment.unpause', self.unpause)

    # def queue_put(self, input_):
    #     self.queue_input.put(input_)
    #
    # def queue_get(self):
    #     return self.queue_output.get()

    # def queue_empty(self):
    #     return self.queue_output.empty()

    def start(self, args):
        try:
            self.stop_event = multiprocessing.Event()
            self.pause_event = multiprocessing.Event()
            self.process = multiprocessing.Process(
                target=run_experiment,
                args=(
                    copy.deepcopy(self.config),
                    self.stop_event,
                    self.pause_event)
            )
            # self.process.daemon = True
            self.process.start()
        except Exception as e:
            print(e)
            print('cant start experiment')

    def stop(self, args):
        self.stop_event.set()
        if self.process is not None and self.process.is_alive():
            self.process.terminate()
        # if self.process is not None:
        #     self.process.join()

    def pause(self, args):
        self.pause_event.set()

    def unpause(self, args):
        self.pause_event.clear()



def run_experiment(config, stop_event, pause_event):
    em = EventManager()

    if config.modality != 'ecog':
        setup_em(em, config)

        if config.experiment_type == 'words':
            run_experiment_words(config, em, stop_event, pause_event)
        elif config.experiment_type == 'text_full':
            run_experiment_text_listen(config, em, stop_event, pause_event)
        elif config.experiment_type == 'subset5':
            run_experiment_subset(config, em, stop_event, pause_event)
        elif config.experiment_type == 'subset20':
            run_experiment_subset20(config, em, stop_event, pause_event)

    if config.modality == 'ecog':
        from receiver import Receiver
        from recorder import Recorder

        rcvr = Receiver(em)
        rcdr = Recorder()

        rcvr.connect()
        setup_em(em, config, rcvr)

        import time
        time.sleep(3)

        if config.experiment_type == 'words':
            run_experiment_words(config, em, stop_event, pause_event)
        elif config.experiment_type == 'text_full':
            run_experiment_text_listen(config, em, stop_event, pause_event)
        elif config.experiment_type == 'subset5':
            run_experiment_subset(config, em, stop_event, pause_event)
        elif config.experiment_type == 'subset20':
            run_experiment_subset20(config, em, stop_event, pause_event)

        # print('!')
        time.sleep(3)
        # print(rcvr.queue_output.qsize())
        while rcvr.queue_output.qsize() > 0:
            # print(rcvr.queue_output.qsize())
            message = rcvr.queue_output.get()# block=False)
            if message is None:
                continue
            label, data = message
            if label == 'lost connection, data saved':
                continue
            elif label == 'chunk':
                rcdr.add(data)
        rcdr.save()
        rcvr.disconnect()




def run_experiment_text_listen(config, em, stop_event, pause_event):
    view = View(config)
    audio_player = AudioPlayer(config)

    voice_types_sber = ['Марфа', 'Наталья', 'Борис', 'Тарас', 'Александра', 'Сергей']
    voice_types_yandex = ['Алена', 'Филипп', 'Ермил', 'Женя', 'Мадирус', 'Оммаж', 'Захар']

    audio_dir = ''
    if config.voice_type in voice_types_yandex:
        audio_dir = f'../resource/sounds/yandex/{config.voice_type}/speed{int(config.voice_speed*10)}/text_full/'
    if config.voice_type in voice_types_sber:
        audio_dir = f'../resource/sounds/sber/{config.voice_type}/speed1/text_full/'

    stimulus_index = config.block_index
    audio_path = audio_dir + f'{stimulus_index + 1}.wav'
    _, audio_array = scipy.io.wavfile.read(audio_path)
    audio_array = audio_array / np.max(np.abs(audio_array))

    em.trigger('event_start_block_text_listen', config.block_index)
    psychopy.core.wait(3)
    em.trigger('event_zero', config.block_index)
    psychopy.core.wait(1)

    sr = 48000
    play_text_full(config, em, view, audio_player, audio_array, sr, stimulus_index)
    em.trigger('event_zero', config.block_index)
    psychopy.core.wait(4)






def run_experiment_words(config, em, stop_event, pause_event):
    em.trigger('event_zero', config.block_index)
    view = View(config)
    audio_player = AudioPlayer(config)

    voice_types_sber = ['Марфа', 'Наталья', 'Борис', 'Тарас', 'Александра', 'Сергей']
    voice_types_yandex = ['Алена', 'Филипп', 'Ермил', 'Женя', 'Мадирус', 'Оммаж', 'Захар']

    audio_dir = ''
    if config.voice_type in voice_types_yandex:
        audio_dir = f'../resource/sounds/yandex/{config.voice_type}/speed{int(config.voice_speed*10)}/words/'
    if config.voice_type in voice_types_sber:
        audio_dir = f'../resource/sounds/sber/{config.voice_type}/speed1/words/'

    words_path = f'../resource/words_full.txt'
    with open(words_path, 'r', encoding="utf8") as f:
        words_string = [line.rstrip() for line in f]

    # audio_paths = [audio_dir + f'{i+1}.wav' for i in range(50*config.block_index, 50*(config.block_index+1))]
    # print(config.block_index)
    stimulus_indices = np.arange(50)
    audio_arrays = []
    for stimulus_index in stimulus_indices:
        audio_path = audio_dir + f'{50*config.block_index + stimulus_index+1}.wav'
        # print(audio_path)
        _, audio_array = scipy.io.wavfile.read(audio_path)
        audio_array = audio_array / np.max(np.abs(audio_array))
        audio_arrays.append(audio_array)

    em.trigger('event_start_block_words', config.block_index)
    psychopy.core.wait(3)
    em.trigger('event_zero', config.block_index)
    psychopy.core.wait(1)

    config.stimulus_visual_time = 1.5


    # time_cross_covert = time_cross_covert,
    # time_word_hold_covert = time_word_hold_covert,
    # time_word_covert = time_word_covert,
    # time_cross_overt = time_cross_overt,
    # time_word_hold_overt = time_word_hold_overt,
    # time_word_overt = time_word_overt,

    sr = 48000
    # for index, audio_array in enumerate(audio_arrays):
    for stimulus_index in stimulus_indices:
        audio_array = audio_arrays[stimulus_index]
        psychopy.core.wait(config.word_rest_time)

        if config.stimulus_visual and config.stimulus_audial:
            show_stimulus_audialvisual(config, em, view, words_string, audio_player, audio_array, sr, stimulus_index)
        elif not config.stimulus_audial:
            show_stimulus_visual(config, em, view, words_string, stimulus_index)
        elif not config.stimulus_visual:
            show_stimulus_audial(config, em, view, audio_player, audio_array, sr, stimulus_index)

        psychopy.core.wait(config.time_word_hold_covert)
        view.show_cross('orange')
        psychopy.core.wait(config.time_cross_covert)
        view.clear()
        view.show_rectangle('orange')
        em.trigger('event_start_show_square_covert', stimulus_index + 1)
        psychopy.core.wait(config.time_word_covert)
        view.clear()
        em.trigger('event_stop_show_square_covert', stimulus_index + 1)
        if config.word_overt_use:
            psychopy.core.wait(config.time_word_hold_overt)
            view.show_cross('green')
            psychopy.core.wait(config.time_cross_overt)
            view.clear()
            view.show_rectangle('green')
            em.trigger('event_start_show_square_overt', stimulus_index + 1)
            psychopy.core.wait(config.time_word_overt)
            view.clear()
            em.trigger('event_stop_show_square_overt', stimulus_index + 1)

        if stop_event.is_set():
            psychopy.core.wait(2)
            break
    psychopy.core.wait(4)

def run_experiment_subset(config, em, stop_event, pause_event):
    em.trigger('event_zero', config.block_index)
    view = View(config)
    audio_player = AudioPlayer(config)

    voice_types_sber = ['Марфа', 'Наталья', 'Борис', 'Тарас', 'Александра', 'Сергей']
    voice_types_yandex = ['Алена', 'Филипп', 'Ермил', 'Женя', 'Мадирус', 'Оммаж', 'Захар']

    audio_dir = ''
    if config.voice_type in voice_types_yandex:
        audio_dir = f'../resource/sounds/yandex/{config.voice_type}/speed{int(config.voice_speed*10)}/words/'
    if config.voice_type in voice_types_sber:
        audio_dir = f'../resource/sounds/sber/{config.voice_type}/speed1/words/'

    words_path = f'../resource/words_full.txt'
    with open(words_path, 'r', encoding="utf8") as f:
        words_string_ = [line.rstrip() for line in f]

    # audio_paths = [audio_dir + f'{i+1}.wav' for i in range(50*config.block_index, 50*(config.block_index+1))]
    # print(config.block_index)
    stimulus_indices = np.arange(5)
    resource_indices = config.word_set_5
    audio_arrays = []
    for stimulus_index in stimulus_indices:
        audio_path = audio_dir + f'{resource_indices[stimulus_index]+1}.wav'
        # print(audio_path)
        _, audio_array = scipy.io.wavfile.read(audio_path)
        audio_array = audio_array / np.max(np.abs(audio_array))
        audio_arrays.append(audio_array)

    order_indices = [np.random.choice(np.arange(5), size=5, replace=False)]
    while len(order_indices) < 8:
        trial_order = np.random.choice(np.arange(5), size=5, replace=False)
        # if trial_order[0] != order_indices[-1][-1]:
        order_indices.append(trial_order)
    order_indices = np.concatenate(order_indices)
    print(order_indices)

    words_string = []
    for order_index in order_indices:
        words_string.append(words_string_[resource_indices[order_index]])
    # print(order_indices)

    em.trigger('event_start_block_words', config.block_index + 100)
    psychopy.core.wait(3)
    em.trigger('event_zero', config.block_index + 100)
    psychopy.core.wait(1)

    config.stimulus_visual_time = 1.5

    sr = 48000
    # for index, audio_array in enumerate(audio_arrays):
    for order_index in order_indices:
        audio_array = audio_arrays[order_index]
        psychopy.core.wait(config.word_rest_time)

        if config.stimulus_visual and config.stimulus_audial:
            show_stimulus_audialvisual(config, em, view, words_string, audio_player, audio_array, sr, order_index)
        elif not config.stimulus_audial:
            show_stimulus_visual(config, em, view, words_string, order_index)
        elif not config.stimulus_visual:
            show_stimulus_audial(config, em, view, audio_player, audio_array, sr, order_index)

        psychopy.core.wait(config.time_word_hold_covert)
        view.show_cross('orange')
        psychopy.core.wait(config.time_cross_covert)
        view.clear()
        view.show_rectangle('orange')
        em.trigger('event_start_show_square_covert', order_index + 1)
        psychopy.core.wait(config.time_word_covert)
        view.clear()
        em.trigger('event_stop_show_square_covert', order_index + 1)
        if config.word_overt_use:
            psychopy.core.wait(config.time_word_hold_overt)
            view.show_cross('green')
            psychopy.core.wait(config.time_cross_overt)
            view.clear()
            view.show_rectangle('green')
            em.trigger('event_start_show_square_overt', order_index + 1)
            psychopy.core.wait(config.time_word_overt)
            view.clear()
            em.trigger('event_stop_show_square_overt', order_index + 1)

        if stop_event.is_set():
            psychopy.core.wait(2)
            break
    psychopy.core.wait(4)


def run_experiment_subset20(config, em, stop_event, pause_event):
    em.trigger('event_zero', config.block_index)
    view = View(config)
    audio_player = AudioPlayer(config)

    voice_types_sber = ['Марфа', 'Наталья', 'Борис', 'Тарас', 'Александра', 'Сергей']
    voice_types_yandex = ['Алена', 'Филипп', 'Ермил', 'Женя', 'Мадирус', 'Оммаж', 'Захар']

    audio_dir = ''
    if config.voice_type in voice_types_yandex:
        audio_dir = f'../resource/sounds/yandex/{config.voice_type}/speed{int(config.voice_speed*10)}/words/'
    if config.voice_type in voice_types_sber:
        audio_dir = f'../resource/sounds/sber/{config.voice_type}/speed1/words/'

    words_path = f'../resource/words_full.txt'
    with open(words_path, 'r', encoding="utf8") as f:
        words_string_ = [line.rstrip() for line in f]

    # audio_paths = [audio_dir + f'{i+1}.wav' for i in range(50*config.block_index, 50*(config.block_index+1))]
    # print(config.block_index)
    stimulus_indices = np.arange(20)
    resource_indices = config.word_set_20
    audio_arrays = []
    for stimulus_index in stimulus_indices:
        audio_path = audio_dir + f'{resource_indices[stimulus_index]+1}.wav'
        # print(audio_path)
        _, audio_array = scipy.io.wavfile.read(audio_path)
        audio_array = audio_array / np.max(np.abs(audio_array))
        audio_arrays.append(audio_array)

    order_indices = [np.random.choice(np.arange(20), size=20, replace=False)]
    while len(order_indices) < 2:
        trial_order = np.random.choice(np.arange(20), size=20, replace=False)
        if trial_order[0] != order_indices[-1][-1]:
            order_indices.append(trial_order)
    order_indices = np.concatenate(order_indices)
    print(order_indices)

    words_string = []
    for order_index in order_indices:
        words_string.append(words_string_[resource_indices[order_index]])
    # print(order_indices)

    em.trigger('event_start_block_words', config.block_index + 21000)
    psychopy.core.wait(3)
    em.trigger('event_zero', config.block_index + 21000)
    psychopy.core.wait(1)

    config.stimulus_visual_time = 1.5

    sr = 48000
    # for index, audio_array in enumerate(audio_arrays):
    for order_index in order_indices:
        index = resource_indices[order_index]
        audio_array = audio_arrays[order_index]
        psychopy.core.wait(config.word_rest_time)

        if config.stimulus_visual and config.stimulus_audial:
            show_stimulus_audialvisual(config, em, view, words_string, audio_player, audio_array, sr, index)
        elif not config.stimulus_audial:
            show_stimulus_visual(config, em, view, words_string, index)
        elif not config.stimulus_visual:
            show_stimulus_audial(config, em, view, audio_player, audio_array, sr, index)

        psychopy.core.wait(config.time_word_hold_covert)
        if config.time_cross_covert > 0:
            view.show_cross('orange')
            psychopy.core.wait(config.time_cross_covert)
        view.clear()
        view.show_rectangle('orange')
        em.trigger('event_start_show_square_covert', index + 1)
        psychopy.core.wait(config.time_word_covert)
        view.clear()
        em.trigger('event_stop_show_square_covert', index + 1)
        if config.word_overt_use:
            psychopy.core.wait(config.time_word_hold_overt)
            if config.time_cross_overt > 0:
                view.show_cross('green')
                psychopy.core.wait(config.time_cross_overt)
            view.clear()
            view.show_rectangle('green')
            em.trigger('event_start_show_square_overt', index + 1)
            psychopy.core.wait(config.time_word_overt)
            view.clear()
            em.trigger('event_stop_show_square_overt', index + 1)

        if stop_event.is_set():
            psychopy.core.wait(2)
            break
    psychopy.core.wait(4)

def show_stimulus_audialvisual(config, em, view, words_string, audio_player, audio_array, sr, stimulus_index):
    audio_player.play(audio_array, latency=config.word_latency_time)
    time_offset = config.word_latency_time - config.time_cross_stimulus
    if time_offset > 0:
        psychopy.core.wait(time_offset)
        view.show_cross('grey')
        psychopy.core.wait(config.time_cross_stimulus)
    else:
        view.show_cross('grey')
        psychopy.core.wait(config.word_latency_time)
    view.clear()
    # view.show_icon_headphones()
    view.show_word(words_string[stimulus_index + 50*config.block_index])
    em.trigger('event_start_showplay_word', stimulus_index + 1)
    psychopy.core.wait(np.max([audio_array.shape[0] / sr, config.stimulus_visual_time]))
    view.clear()
    em.trigger('event_stop_showplay_word', stimulus_index + 1)

def show_stimulus_visual(config, em, view, words_string, stimulus_index):
    time_offset = config.word_latency_time - config.time_cross_stimulus
    if time_offset > 0:
        psychopy.core.wait(time_offset)
        view.show_cross('grey')
        psychopy.core.wait(config.time_cross_stimulus)
    else:
        view.show_cross('grey')
        psychopy.core.wait(config.word_latency_time)

    view.clear()
    view.show_word(words_string[stimulus_index + 50*config.block_index])
    em.trigger('event_start_show_word', stimulus_index + 1)
    psychopy.core.wait(config.stimulus_visual_time)
    view.clear()
    em.trigger('event_stop_show_word', stimulus_index + 1)

def show_stimulus_audial(config, em, view, audio_player, audio_array, sr, stimulus_index):
    audio_player.play(audio_array, latency=config.word_latency_time)
    # view.show_cross('white')
    view.show_cross('grey')
    time_offset = config.word_latency_time - config.time_cross_stimulus
    if time_offset > 0:
        psychopy.core.wait(time_offset)
        view.show_cross('grey')
        psychopy.core.wait(config.time_cross_stimulus)
    else:
        view.show_cross('grey')
        psychopy.core.wait(config.word_latency_time)

    view.clear()
    view.show_icon_headphones('grey')
    # view.show_rectangle('grey')
    # view.show_cross('red')
    em.trigger('event_start_play_word', stimulus_index + 1)
    psychopy.core.wait(audio_array.shape[0] / sr)
    view.clear()
    em.trigger('event_stop_play_word', stimulus_index + 1)

def play_text_full(config, em, view, audio_player, audio_array, sr, stimulus_index):
    audio_player.play(audio_array, latency=config.word_latency_time)
    view.show_cross('grey')
    # view.show_cross('red')
    psychopy.core.wait(config.word_latency_time)
    # view.clear()
    view.show_icon_headphones()
    em.trigger('event_start_play_text_full', stimulus_index + 1)
    n_sec = int(audio_array.shape[0] / sr)
    leftover = audio_array.shape[0] / sr - n_sec
    for i in range(n_sec):
        psychopy.core.wait(1)
        view.show_icon_headphones()
    psychopy.core.wait(leftover)
    view.clear()
    em.trigger('event_stop_play_text_full', stimulus_index + 1)
    psychopy.core.wait(4)




class View:
    def __init__(self, config):

        # Create an instance of the Monitor class
        my_monitor = monitors.Monitor('testMonitor')
        my_monitor.setSizePix((1920, 1080))
        # my_monitor.setRefreshRate(240)
        my_monitor.setGamma(1.0)
        size = config.visual_size

        screen = 0 if config.main_screen else 1
        if config.full_screen:
            self.win = visual.Window(
                monitor=my_monitor, color=self._get_color('black'),
                units='pix', fullscr=True, screen=screen
            )
        else:
            self.win = visual.Window(
                monitor=my_monitor, size=[600, 600], color=self._get_color('black'),
                units='pix', fullscr=False, screen=screen
            )

        # square_miltiplier = config.square_size
        # square_size = [square_miltiplier*self.win.size[1]/10000, square_miltiplier*self.win.size[0]/10000]
        self.cross = visual.ShapeStim(
            self.win,
            units='pix',
            lineColor=self._get_color('white'),
            lineWidth=2,
            vertices=((-15*size,0),(15*size,0), (0,0), (0,-15*size),(0,15*size)),
            closeShape=False,
            pos=(0,0)
        )
        self.rectangle = visual.Rect(
            self.win,
            units='pix',
            width=100*size,
            height=40*size,
            fillColor=self._get_color('black'),
            lineColor=self._get_color('green'),
            lineWidth=4,
            pos=(0,0)
        )
        self.icon_headphones = visual.ImageStim(
            self.win,
            image='../resource/images/icon_headphones.png',
            pos=(0, 0),
            color=self._get_color('grey'),
            size=(50*size, 50*size)
        )

        self.text = visual.TextStim(
            win=self.win,
            text='word',
            color=self._get_color('white'),
            height=40*size
        )

        self.win.flip()

    def show_cross(self, color=None):
        if color is not None:
            self.cross.lineColor = self._get_color(color)
        self.cross.draw()
        self.win.flip()
        
    def show_rectangle(self, color=None):
        if color is not None:
            self.rectangle.lineColor = self._get_color(color)
        self.rectangle.draw()
        self.win.flip()

    def show_icon_headphones(self, color=None):
        if color is not None:
            self.rectangle.lineColor = self._get_color(color)
        self.icon_headphones.draw()
        # self.show_cross('red')
        self.win.flip()

    def show_word(self, word, color=None):
        if color is None:
            color = 'white'
            self.text.color = self._get_color(color)
        self.text.text = word
        self.text.draw()
        self.win.flip()

    def clear(self):
        self.win.clearBuffer()
        self.win.flip()

    def _get_color(self, color_name):
        if color_name == 'black': return [-1,-1,-1]
        elif color_name == 'grey': return [0, 0, 0]
        elif color_name == 'green': return [-1, 1, -1]
        elif color_name == 'red': return [1, -1, -1]
        elif color_name == 'orange': return [1, 0, -1]
        elif color_name == 'yellow': return [1, 1, -1]
        elif color_name == 'white': return [1, 1, 1]
        else: return [0, 0, 0]



def setup_em(em, config, rcvr=None):
    if config.modality == 'test':
        em.register_handler('event_start_kk_words', _start_block_words_test)
        em.register_handler('event_start_play_word', _start_play_word_test)
        em.register_handler('event_stop_play_word', _stop_play_word_test)
        em.register_handler('event_start_show_word', _start_show_word_test)
        em.register_handler('event_stop_show_word', _stop_show_word_test)
        em.register_handler('event_start_showplay_word', _start_showplay_word_test)
        em.register_handler('event_stop_showplay_word', _stop_showplay_word_test)
        em.register_handler('event_start_show_square_covert', _start_show_square_covert)
        em.register_handler('event_stop_show_square_covert', _stop_show_square_covert)
        em.register_handler('event_start_show_square_overt', _start_show_square_overt)
        em.register_handler('event_stop_show_square_overt', _stop_show_square_overt)
        em.register_handler('event_zero', _zero)

        em.register_handler('event_start_block_text_listen', _start_block_text_listen)
        em.register_handler('event_start_play_text_full', _start_play_text_full)
        em.register_handler('event_stop_play_text_full', _stop_play_text_full)
    elif config.modality == 'ecog':
        em.register_handler('event_start_block_words', partial(_start_block_words_test_ecog, rcvr))
        em.register_handler('event_start_play_word', partial(_start_play_word_test_ecog, rcvr))
        em.register_handler('event_stop_play_word', partial(_stop_play_word_test_ecog, rcvr))
        em.register_handler('event_start_show_word', partial(_start_show_word_test_ecog, rcvr))
        em.register_handler('event_stop_show_word', partial(_stop_show_word_test_ecog, rcvr))
        em.register_handler('event_start_showplay_word', partial(_start_showplay_word_test_ecog, rcvr))
        em.register_handler('event_stop_showplay_word', partial(_stop_showplay_word_test_ecog, rcvr))
        em.register_handler('event_start_show_square_covert', partial(_start_show_square_covert_ecog, rcvr))
        em.register_handler('event_stop_show_square_covert', partial(_stop_show_square_covert_ecog, rcvr))
        em.register_handler('event_start_show_square_overt', partial(_start_show_square_overt_ecog, rcvr))
        em.register_handler('event_stop_show_square_overt', partial(_stop_show_square_overt_ecog, rcvr))
        em.register_handler('event_zero', partial(_zero_ecog, rcvr))

        em.register_handler('event_start_block_text_listen', partial(_start_block_text_listen_ecog, rcvr))
        em.register_handler('event_start_play_text_full', partial(_start_play_text_full_ecog, rcvr))
        em.register_handler('event_stop_play_text_full', partial(_stop_play_text_full_ecog, rcvr))

    elif config.modality == 'meg':
        parallel_port = ParallelPort(verbose=True)
        em.register_handler('event_start_block_words', partial(_start_block_words_test_meg, parallel_port))
        em.register_handler('event_start_play_word', partial(_start_play_word_test_meg, parallel_port))
        em.register_handler('event_stop_play_word', partial(_stop_play_word_test_meg, parallel_port))
        em.register_handler('event_start_show_word', partial(_start_show_word_test_meg, parallel_port))
        em.register_handler('event_stop_show_word', partial(_stop_show_word_test_meg, parallel_port))
        em.register_handler('event_start_showplay_word', partial(_start_showplay_word_test_meg, parallel_port))
        em.register_handler('event_stop_showplay_word', partial(_stop_showplay_word_test_meg, parallel_port))
        em.register_handler('event_start_show_square_covert', partial(_start_show_square_covert_meg, parallel_port))
        em.register_handler('event_stop_show_square_covert', partial(_stop_show_square_covert_meg, parallel_port))
        em.register_handler('event_start_show_square_overt', partial(_start_show_square_overt_meg, parallel_port))
        em.register_handler('event_stop_show_square_overt', partial(_stop_show_square_overt_meg, parallel_port))
        em.register_handler('event_zero', partial(_zero_meg, parallel_port))

        em.register_handler('event_start_block_text_listen', partial(_start_block_text_listen_meg, parallel_port))
        em.register_handler('event_start_play_text_full', partial(_start_play_word_test_meg, parallel_port))
        em.register_handler('event_stop_play_text_full', partial(_stop_play_word_test_meg, parallel_port))


def _start_block_words_test(block_index):
    print(f'start block words test {block_index + 1}')

def _start_play_word_test(word_index):
    print(f'start play word test {word_index}')

def _stop_play_word_test(word_index):
    print(f'stop play word test {word_index}')

def _start_show_word_test(word_index):
    print(f'start show word test {word_index}')

def _stop_show_word_test(word_index):
    print(f'stop show word test {word_index}')

def _start_showplay_word_test(word_index):
    print(f'start showplay word test {word_index}')

def _stop_showplay_word_test(word_index):
    print(f'stop showplay word test {word_index}')

def _start_show_square_covert(word_index):
    print(f'start show square covert {word_index}')

def _stop_show_square_covert(word_index):
    print(f'stop show square covert {word_index}')

def _start_show_square_overt(word_index):
    print(f'start show square overt {word_index}')

def _stop_show_square_overt(word_index):
    print(f'stop show square overt {word_index}')

def _start_block_text_listen(block_index):
    print(f'start block text listen {50 + block_index + 1}')

def _start_play_text_full(text_index):
    print(f'start play text full {text_index}')

def _stop_play_text_full(text_index):
    print(f'stop play text full {text_index}')

def _zero(args):
    print('zero output')
    
    
class ParallelPort():
    def __init__(self, idle=False, verbose=True):
        self.idle = idle
        self.verbose = verbose
        if self.idle:
            print('Idle parallel port created')
        else:
            try:
                from psychopy import parallel
                self.p_port = parallel.ParallelPort(address='0xE030')
            except:
                print('Something went wrong, parallel port wasn\'t created, started idle mode')
                self.idle = True                      

    def set_parallel_port(self, index):
        if self.idle and self.verbose:
            print('parralel port: idle {}'.format(int(index)))
        elif not self.idle:
            try:
                self.p_port.setData(int(index))
            except:
                print('Something went wrong, can\'t sent into the parallel port, started idle mode')
                self.idle = True                      
            if self.verbose:
                print('parralel port: real {}'.format(int(index)))
            
    
    
def _start_block_words_test_meg(parallel_port, block_index):
    parallel_port.set_parallel_port(block_index + 1)

def _start_play_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(word_index)

def _stop_play_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(0)

def _start_show_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(50 + word_index)

def _stop_show_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(0)

def _start_showplay_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(100 + word_index)

def _stop_showplay_word_test_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(0)

def _start_show_square_covert_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(150 + word_index)

def _stop_show_square_covert_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(0)

def _start_show_square_overt_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(200 + word_index)

def _stop_show_square_overt_meg(parallel_port, word_index):
    parallel_port.set_parallel_port(0)

def _start_block_text_listen_meg(parallel_port, block_index):
    parallel_port.set_parallel_port(50 + block_index + 1)

def _zero_meg(parallel_port, args):
    parallel_port.set_parallel_port(0)


control_index = 0,
stimulus_index = 0,

def _start_block_words_test_ecog(rcvr, block_index):
    rcvr.queue_input.put({'control_index':block_index+1+20000})

def _start_play_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index':word_index})
    print(word_index)

def _stop_play_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index':word_index+1000})
    print(word_index + 1000)

def _start_show_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index':word_index+2000})
    print(word_index+2000)

def _stop_show_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index':word_index+3000})
    print(word_index+3000)

def _start_showplay_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 4000})
    print(word_index + 4000)

def _stop_showplay_word_test_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 5000})
    print(word_index + 5000)

def _start_show_square_covert_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 6000})
    print(word_index + 6000)

def _stop_show_square_covert_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 7000})
    print(word_index + 7000)

def _start_show_square_overt_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 8000})
    print(word_index + 8000)

def _stop_show_square_overt_ecog(rcvr, word_index):
    rcvr.queue_input.put({'stimulus_index': word_index + 9000})
    print(word_index + 9000)

def _start_block_text_listen_ecog(rcvr, block_index):
    rcvr.queue_input.put({'stimulus_index': block_index + 1 + 10000})
    print(block_index + 10000)


def _start_play_text_full_ecog(rcvr, text_index):
    rcvr.queue_input.put({'stimulus_index': text_index + 11000})
    print(text_index + 11000)

def _stop_play_text_full_ecog(rcvr, text_index):
    rcvr.queue_input.put({'stimulus_index': text_index + 12000})
    print(text_index + 12000)


def _zero_ecog(rcvr, args):
    rcvr.queue_input.put({'stimulus_index': 0})
    print(0)



