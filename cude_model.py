from base_model import BaseModel
import numpy as np

class CubeModel(BaseModel):
    def __init__(self, edge_size):
        
        self.verts = []
        self.indices = []
        self.farthest_distance_var = 0

        A = []

        self.verts = np.array(self.verts, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint16)
        self.create_vao()

    def get_verts(self):
        return self.verts
    def get_indices(self):
        return self.indices
    def is_empty(self):
        return self.get_verts().shape[0] == 0 # type: ignore
    def farthest_distance(self):
        return self.farthest_distance_var
