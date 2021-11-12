from abc import ABC
from abc import abstractmethod
import numpy as np

from OpenGL.GL import *

class BaseModel(ABC):

    def __init__(self):
        self.vao = None
        pass
    @abstractmethod
    def get_verts(self):
        return np.array([], dtype=np.float32)
    @abstractmethod
    def get_indices(self):
        return np.array([], dtype=np.uint32)
    @abstractmethod
    def get_normals(self):
        return np.array([], dtype=np.float32)
    @abstractmethod
    def is_empty(self):
        pass
    @abstractmethod
    def farthest_distance(self):
        return 10

    def get_magnitude_squared(self, vert):
        s = 0
        for i in vert:
            s += i*i
        return s**0.5
    def sub(self, u, v):
        return [u[0] - v[0], u[1] - v[1], u[2] - v[2]]
    def get_normal(self, u, v):
        return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
    def create_vao(self):
        # create and bind vao
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # create index buffer and bind it to vao
        indices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.get_indices().nbytes, self.get_indices(), GL_STATIC_DRAW)

        # create vertex buffer and bind to vao
        # vertex attrib is at slot 0 for the fixed-function pipeline
        glEnableVertexAttribArray(0)
        vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertices)
        glBufferData(GL_ARRAY_BUFFER, self.get_verts().nbytes, self.get_verts(), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        self.clear_buffers()

        # create normal buffer and bind to vao
        # normal attrib is at slot 2 for the fixed-function pipeline
        glEnableVertexAttribArray(2)
        normals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, normals)
        glBufferData(GL_ARRAY_BUFFER, self.get_normals().nbytes, self.get_normals(), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(2)

    def clear_buffers(self):
        glBindVertexArray(0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bind_vao(self):
        glBindVertexArray(self.vao)

    def draw(self):
        self.bind_vao()
        glDrawElements(GL_TRIANGLES, self.get_indices().shape[0], GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def draw_wireframe(self):
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
        self.draw()
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
