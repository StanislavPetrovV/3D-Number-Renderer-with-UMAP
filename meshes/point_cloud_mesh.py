from settings import *
import numpy as np
import moderngl as mgl


class PointCloudMesh:
    def __init__(self, renderer):
        self.ctx = renderer.ctx
        self.program = renderer.shader_program.point_cloud
        #
        self.vao = self.get_vao(point_positions=renderer.app.data_loader.point_positions)

    def get_vao(self, point_positions):
        point_position_buffer = self.ctx.buffer(point_positions)
        #
        vao = self.ctx.vertex_array(
            self.program,
            [
                (point_position_buffer, '3f', 'in_position'),
            ],
            skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render(mode=mgl.POINTS)
