import numpy as np
import h5py


class Recorder:
    def __init__(self):
        self.memory = []

    def add(self, chunk):
        # if len(self.memory) > 0:
        #     assert self.memory[-1].shape[0] == chunk.shape[0]
        self.memory.append(chunk)

    def clear(self):
        self.memory = []

    def save(self):
        import datetime

        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

        dirpath = 'C:/PatientData/patient/'
        os.makedirs(dirpath, exist_ok=True)
        with h5py.File(dirpath + date_string + '.h5', 'w') as file:
            if len(self.memory) > 0:
                stacked_data = np.concatenate(self.memory, axis=0)
                file['raw_data'] = stacked_data
            else:
                empty_shape = (0, 68)
                file.create_dataset('raw_data', empty_shape)

            file.attrs['fs'] = 4096
        print('SAVED!!! ' + date_string)

            #
            # file.create_dataset('channel_bads', data=np.asarray(config_recorder.channel_bads))
            # file.create_dataset('channel_names', data=np.asarray(config_recorder.channel_names))
            # file.create_dataset('fs', data=np.array(config_recorder.fs))
