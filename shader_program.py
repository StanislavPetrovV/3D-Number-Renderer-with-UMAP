from settings import *
from itertools import accumulate
import struct


class ShaderProgram:
    def __init__(self, renderer):
        self.app = renderer.app
        self.ctx = renderer.ctx
        self.camera = renderer.camera

        # -------- shaders -------- #
        self.axis = self.get_program(shader_name='axis')
        self.point_cloud = self.get_program(shader_name='point_cloud')

        # UBO structure:
        #
        #   mat4  m_proj     == 64 bytes
        #   vec3  center     == 12
        #   float rot_speed  == 4
        #   mat4  m_view     == 64
        #   vec3  cam_pos    == 12
        #   float u_time     == 4

        self.ubo_bytes = {
            'm_proj': 64,
            'center': 12,
            'rot_speed': 4,
            'm_view': 64,
            'cam_pos': 12,
            'u_time': 4
        }

        # offsets
        self.offsets = dict(zip(
            self.ubo_bytes, accumulate(self.ubo_bytes.values(), initial=0)))

        # get buffer size
        min_size = sum(self.ubo_bytes.values())
        buffer_size = min_size if not min_size % 16 else ((min_size // 16) + 1) * 16
        # padding = buffer_size - min_size

        # ubo
        self.uniform_buffer = self.ctx.buffer(reserve=buffer_size)
        self.uniform_buffer.bind_to_uniform_block(binding=UBO_BIND_VALUE)

        # binding
        self.axis['UBO'].binding = UBO_BIND_VALUE

        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        #
        self.uniform_buffer.write(
            data=self.camera.m_proj, offset=self.offsets['m_proj'])
        #
        self.uniform_buffer.write(
            data=self.app.data_loader.center, offset=self.offsets['center'])
        #
        self.uniform_buffer.write(
            data=struct.pack('=1f', WORLD_ROT_SPEED), offset=self.offsets['rot_speed'])

    def update(self):
        #
        self.uniform_buffer.write(
            data=self.camera.m_view, offset=self.offsets['m_view'])
        #
        self.uniform_buffer.write(
            data=self.camera.position, offset=self.offsets['cam_pos'])
        #
        self.uniform_buffer.write(
            data=struct.pack('=1f', self.app.time), offset=self.offsets['u_time'])

    def get_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
