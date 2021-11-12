from PyQt5 import QtOpenGL
from PyQt5.QtCore import QPoint
from base_model import BaseModel
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
import math

class ModelCanvas (QtOpenGL.QGLWidget):

    def __init__(self):
        super(ModelCanvas, self).__init__()

        self.model = None

        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size

        self.fov = 60

        self.horizontal_rot = 0
        self.vertical_rot = 0
        self.radius = 20

        self.drag_speed = 1/90
        self.drag_reference : QPoint = QPoint(0, 0)
        self.clear()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

    def setup_lighting(self):
        # Enable Lighting
        glEnable(GL_LIGHTING);

        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, 0);
        glLightfv(GL_LIGHT0, GL_POSITION, [10, 10, -2, 1]);
        glLightfv(GL_LIGHT1, GL_POSITION, [1, 1, 1, 1]);

        # Set light intensity and color for each component
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5,0.5,0.5,1]);
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5,0.5,0.5,1]);
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1,1,1,1]);

        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.7,0.7,0.7,1]);
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.3,0.3,0.3,1]);
        glLightfv(GL_LIGHT1, GL_SPECULAR, [1,1,1,1]);

        # Set attenuation
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5);
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 1.0);

        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.2);

        # Enable Lights
        glEnable(GL_LIGHT0);
        glEnable(GL_LIGHT1);
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_SPECULAR)

        # Make so objects shine
        glMaterialfv(GL_FRONT, GL_SHININESS, 60);

    def initializeGL(self): #glClearColor(1.0, 1.0, 1.0, 1.0)

        glClearColor(0.1, 0.1, 0.1, 0.1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_NORMALIZE)

        self.setup_lighting()

        self.clear()

    def resizeGL(self, _width, _height):

        # store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        # setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        # reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(self.fov, self.m_w/float(self.m_h), 0.1, 2000);

        # setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.radius*math.cos(self.horizontal_rot), self.radius*math.cos(self.vertical_rot), self.radius*math.sin(self.horizontal_rot), 0, 0, 0, 0, 1, 0)

    def set_material_color(self, colors):
        glMaterialfv(GL_FRONT, GL_SPECULAR, colors);
        glMaterialfv(GL_FRONT, GL_AMBIENT, colors);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, colors);
        glColor(colors)

    def set_lighting(self):

        # lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [10, 10, -2, 1]);
        glLightfv(GL_LIGHT1, GL_POSITION, [1, 1, 1, 1]);

    def draw_axis_lines(self):

        # ignore lighting
        glDisable(GL_LIGHTING)
        # axis lines
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(-100.0, 0.0, 0.0)
        glVertex3f(100.0, 0.0, 0.0)
        glColor3f(0, 1, 0)
        glVertex3f(0.0, -100.0, 0.0)
        glVertex3f(0.0, 100.0, 0.0)
        glColor3f(0, 0, 1)
        glVertex3f(0.0, 0.0, -100.0)
        glVertex3f(0.0, 0.0, 100.0)
        glEnd()
        glEnable(GL_LIGHTING)

    def paintGL(self):

        if(self.model == None or self.model.is_empty()): return
        # clear the buffer with the current clear color
        self.clear()

        # draw a triangle with RGB color at the 3 vertices
        # interpolating smoothly the color in the interior
        glShadeModel(GL_SMOOTH)

        self.draw_axis_lines()

        self.set_lighting()

        # model
        self.set_material_color([0.8, .15, 0])
        self.model.draw()
        self.set_material_color([0, 0, 0])
        self.model.draw_wireframe()

    def set_model(self, model : BaseModel):
        if(model == None): return
        self.model = model
        self.radius = self.model.farthest_distance()
        self.updateGL()

    def zoom(self, delta):

        # zoom in/out by changing Field of Vision
        #self.fov -= delta/60

        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #gluPerspective(self.fov, self.m_w/float(self.m_h), 0.1, 2000);

        # zoom in/out by changing camera position

        self.radius -= delta/1000
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.radius*math.cos(self.horizontal_rot), self.radius*math.cos(self.vertical_rot), self.radius*math.sin(self.horizontal_rot), 0, 0, 0, 0, 1, 0)

        self.updateGL()
    

        self.updateGL()

    def drag(self, x, y):
        self.horizontal_rot += x * self.drag_speed
        self.vertical_rot += y * self.drag_speed

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.radius*math.cos(self.horizontal_rot), self.radius*math.cos(self.vertical_rot), self.radius*math.sin(self.horizontal_rot), 0, 0, 0, 0, 1, 0)

        self.updateGL()
    
    def mousePressEvent(self, _):
        pass
        #print("pressed at: ", e.x(), e.y())
    def mouseReleaseEvent(self, _):
        self.drag_reference = QPoint(0, 0)
        #print("released at: ", e.x(), e.y())
    def mouseMoveEvent(self, e):
        point = QPoint(e.x(), e.y())
        if(not self.drag_reference.isNull()):
            move = point - self.drag_reference
            self.drag(move.x(), move.y())
        self.drag_reference = point

    def wheelEvent(self, e):
        #print("wheel:", e.angleDelta().y())
        self.zoom(e.angleDelta().y())
