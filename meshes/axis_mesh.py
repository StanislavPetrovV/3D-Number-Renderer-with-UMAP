from settings import *
import numpy as np
import moderngl as mgl


class AxisMesh:
    def __init__(self, renderer, scale=1.0, center=glm.vec3(0.0)):
        self.ctx = renderer.ctx
        self.program = renderer.shader_program.axis

        self.scale = scale * 0.85
        self.center = center

        self.vbo_format = '3f'
        self.vbo_attrs = ('in_position',)
        self.vao = self.get_vao()

    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [
                (vbo, self.vbo_format, *self.vbo_attrs)
            ],
            skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render(mgl.LINES)

    def get_vertex_data(self):
        vert_data = np.array(
            [[-1, 0, 0], [1, 0, 0],
             [0, 0, 1], [0, 0, -1],
             [0, -1, 0], [0, 1, 0],], dtype='float32')

        vert_data = vert_data * self.scale + self.center
        return vert_data
