from shader_program import ShaderProgram
from camera import Camera
from meshes.point_cloud_mesh import PointCloudMesh
from meshes.axis_mesh import AxisMesh


class Renderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        #
        self.camera = Camera(app)
        self.shader_program = ShaderProgram(renderer=self)
        #
        self.point_mesh = PointCloudMesh(renderer=self)
        #
        self.axis_mesh = AxisMesh(
            renderer=self,
            scale=self.app.data_loader.scale,
            center=self.app.data_loader.center
        )

    def update(self):
        self.camera.update()
        self.shader_program.update()

    def render(self):
        self.axis_mesh.render()
        self.point_mesh.render()
