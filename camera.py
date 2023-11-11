from settings import *


class Camera:
    def __init__(self, app, position=INIT_CAM_POS, yaw=INIT_CAM_YAW, pitch=INIT_CAM_PITCH):
        self.app = app

        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = CAM_SPEED * self.app.delta_time
        next_step = glm.vec3()
        #
        if key_state[KEYS['FORWARD']]:
            next_step += self.move_forward(vel)
        if key_state[KEYS['BACK']]:
            next_step += self.move_back(vel)
        if key_state[KEYS['STRAFE_R']]:
            next_step += self.move_right(vel)
        if key_state[KEYS['STRAFE_L']]:
            next_step += self.move_left(vel)
        #
        if key_state[KEYS['UP']]:
            self.move_up(vel)
        if key_state[KEYS['DOWN']]:
            self.move_down(vel)
        #
        self.position += next_step

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        #
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        return -self.right * velocity

    def move_right(self, velocity):
        return self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        return self.forward * velocity

    def move_back(self, velocity):
        return -self.forward * velocity
