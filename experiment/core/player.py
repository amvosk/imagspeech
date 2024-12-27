# import psychopy.audio
# psychopy.audio.init(mode=3, rate=44100, buffer=1024)
import psychtoolbox as ptb
from psychopy import sound
from psychopy.sound.backend_ptb import SoundPTB
# from psychopy.sound.backend_sounddevice import SoundDeviceSound
import psychopy.core

class AudioPlayer:
    def __init__(self, config):
        self.config = config
        # self.sound = sound.Sound('A', sampleRate=48000)#, stereo=True)
        # self.sound = SoundDeviceSound('A', sampleRate=48000)  # , stereo=True)
        self.sound = SoundPTB('A', sampleRate=48000)
        print(self.sound)

    def play(self, audio_array, latency):
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        #     _, data = scipy.io.wavfile.read(path)
        # data = data / np.max(np.max(data))
        # print(data.shape)
        # s = sound.Sound(data)  # , stereo=True)
        self.sound.setSound(audio_array)
        play_time = ptb.GetSecs() + latency
        self.sound.play(when=play_time)


if __name__ == '__main__':
    pass