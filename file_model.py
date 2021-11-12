from base_model import BaseModel
import numpy as np
class FileModel(BaseModel):
    def __init__(self, filename: str):
        
        self.verts = []
        self.indices = []
        self.normals = []
        self.farthest_distance_var = 0

        with open(filename, "r") as f:
            for line in f:
                if(line[0] == 'v'):
                    # read three coords and add to vert
                    vert = list(map(float, line[2:].split(' ')))
                    self.verts += vert
                    dist = self.get_magnitude_squared(vert)
                    if(self.farthest_distance == None or self.farthest_distance_var < dist):
                        self.farthest_distance_var = dist
                elif(line[0] == 'f'):
                    # read the index of the vertices that make up this triangle
                    index = list(map(lambda x: int(x) - 1, line[2:].split(' ')))
                    self.indices += index

                    p1 = [self.verts[index[0]*3], self.verts[index[0]*3 + 1], self.verts[index[0]*3 + 2]]
                    p2 = [self.verts[index[1]*3], self.verts[index[1]*3 + 1], self.verts[index[1]*3 + 2]]
                    p3 = [self.verts[index[2]*3], self.verts[index[2]*3 + 1], self.verts[index[2]*3 + 2]]
                    u = self.sub(p2, p1)
                    v = self.sub(p3, p1)
                    self.normals += self.get_normal(u, v)

        self.verts = np.array(self.verts, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)
        self.normals = np.array(self.normals, dtype=np.float32)
        self.create_vao()

    def get_verts(self):
        return self.verts
    def get_indices(self):
        return self.indices
    def get_normals(self):
        return self.normals
    def is_empty(self):
        return self.get_verts().shape[0] == 0 # type: ignore
    def farthest_distance(self):
        return self.farthest_distance_var
