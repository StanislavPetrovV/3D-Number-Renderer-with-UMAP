import numpy as np


class DataLoader:
    def __init__(self, data_path='data/map_data_3d_1000000_15_02.npy'):
        #
        self.point_positions = np.load(data_path)
        #
        self.scale = np.max(self.point_positions)
        self.center = np.mean(self.point_positions, axis=0)
