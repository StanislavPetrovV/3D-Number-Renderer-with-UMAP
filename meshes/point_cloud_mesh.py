from settings import *
import numpy as np
import moderngl as mgl


class PointCloudMesh:
    def __init__(self, renderer):
        self.ctx = renderer.ctx
        self.program = renderer.shader_program.point_cloud
        self.data_loader = renderer.app.data_loader
        #
        self.vao = self.get_vao()

    def get_vao(self):
        point_position_buffer = self.ctx.buffer(self.data_loader.point_positions)
        point_prime_flag_buffer = self.ctx.buffer(self.data_loader.prime_flags)
        #
        vao = self.ctx.vertex_array(
            self.program,
            [
                (point_position_buffer, '3f', 'in_position'),
                (point_prime_flag_buffer, '1i1', 'is_prime'),
            ],
            skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render(mode=mgl.POINTS)
