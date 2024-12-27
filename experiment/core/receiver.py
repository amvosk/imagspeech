# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 13:31:28 2020

@author: AlexVosk
"""

import time, copy
import multiprocessing
from dataclasses import dataclass

from pylsl import StreamInlet, resolve_byprop
import numpy as np


@dataclass
class RecorderFlags:
    # connection_state: int
    # experiment_state: int
    control_index: int
    stimulus_index: int
    cache_index: int


class NoStreamError(ConnectionError):
    pass


class EmptyStreamError(ConnectionError):
    pass


def _connect_lsl():
    try:
        streams = resolve_byprop('name', 'EBNeuro_BePLusLTM_192.168.171.81', timeout=1)
        if len(streams) == 0 or len(streams) >= 2:
            print('Found {} streams with name {}'.format(len(streams), 'EBNeuro_BePLusLTM_192.168.171.81'))
    except TimeoutError:
        raise NoStreamError(
            'No lsl streams with name {} detected'.format('EBNeuro_BePLusLTM_192.168.171.81')) from None
    for i, stream in enumerate(streams):
        try:
            inlet = StreamInlet(stream, 4096)
            _, timestamp = inlet.pull_sample(timeout=1)
            if timestamp:
                return inlet
        except TimeoutError:
            print('{} out of {} lsl streams is empty'.format(i + 1, len(streams)))
    raise EmptyStreamError(
        'Found {} streams, all streams with name {} are empty'.format(len(streams),
                                                                      'EBNeuro_BePLusLTM_192.168.171.81')) from None


def resolve_queue_input(flags, receiver_queue_input_):
    while not receiver_queue_input_.empty():
        queue_flags = receiver_queue_input_.get()
        for field, value in queue_flags.items():
            vars(flags)[field] = copy.deepcopy(value)
    return flags


def _connect(queue_input, queue_output, stop_event):
    try:
        inlet = _connect_lsl()
    except ConnectionError as exc:
        print(exc)
        stop_event.set()
        inlet = None

    flags = RecorderFlags(
        # connection_state=1,
        # experiment_state=0,
        control_index=0,
        stimulus_index=0,
        cache_index=0,
    )

    # flags = resolve_queue_input(flags, queue_input)
    cache = np.zeros((256, 68))
    while not stop_event.is_set():

        flags = resolve_queue_input(flags, queue_input)
        # pull sample and check, is it successful
        sample, timestamp = inlet.pull_sample(timeout=1)
        if timestamp is None:
            message = ('lost connection, data saved', True)
            queue_output.put(message)
            inlet.close_stream()
            return
        # if timestamp exists, add sample to the cache
        else:
            sample = np.asarray(sample)
            big_sample = np.zeros(68)
            # add sEEG data
            big_sample[0:64] = sample[:64]
            # add sound data
            big_sample[64] = sample[64]
            # add timestamp
            big_sample[65] = time.perf_counter()
            # add control_index
            big_sample[66] = flags.control_index
            # add stimulus_index
            big_sample[67] = flags.stimulus_index

            cache[flags.cache_index] = big_sample
            flags.cache_index += 1

            flags.control_index = 0
            flags.stimulus_index = 0

        if flags.cache_index == 256:
            queue_output.put(('chunk', np.copy(cache)))
            # print(queue_output.qsize())
            cache = np.zeros((256, 68))
            flags.cache_index = 0

        if stop_event.is_set() and flags.cache_index > 0:
            queue_output.put(('chunk', np.copy(cache[:flags.cache_index])))
    if inlet is not None:
        inlet.close_stream()


class Receiver:
    def __init__(self, em):
        # initialize basic configuration
        self.em = em
        self.receiver_process = None
        self.stop_event = multiprocessing.Event()
        self.queue_input = multiprocessing.Queue()
        self.queue_output = multiprocessing.Queue()


    def queue_put(self, input_):
        self.queue_input.put(input_)

    def queue_get(self):
        return self.queue_output.get()

    def queue_empty(self):
        return self.queue_output.empty()

    def queue_size(self):
        return self.queue_output.qsize()

    def connect(self):
        try:
            self.receiver_process = multiprocessing.Process(
                target=_connect,
                args=(self.queue_input, self.queue_output, self.stop_event)
            )
            self.receiver_process.daemon = True
            self.receiver_process.start()
        except ConnectionError:
            print('connection error')
            if self.receiver_process.is_alive():
                self.receiver_process.join()
            if self.receiver_process.is_alive():
                self.receiver_process.terminate()

    def disconnect(self):
        self.stop_event.set()
        # try:
        #     self.queue_put({'connection_state': 0})
        # except AttributeError as exc:
        #     print('No process available to disconnect')
    #
    # def stop(self):
    #     self.stop_event.set()

    def clear(self):
        if self.receiver_process.is_alive():
            self.receiver_process.join()
        if self.receiver_process.is_alive():
            self.receiver_process.terminate()
        self.receiver_process = None
        self.stop_event = multiprocessing.Event()
        self.queue_input = multiprocessing.Queue()
        self.queue_output = multiprocessing.Queue()


if __name__ == '__main__':
    pass
#how to block buttons and feilds from change while one buttom is pressed?
