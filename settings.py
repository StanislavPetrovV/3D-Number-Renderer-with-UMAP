import math
import glm
import pygame as pg

# opengl
MAJOR_VERSION = 3
MINOR_VERSION = 3
DEPTH_SIZE = 24
NUM_SAMPLES = 9

WORLD_ROT_SPEED = 0.03

# resolution
WIN_RES = glm.ivec2(1280, 720)
FPS_TARGET = 60

# control keys
KEYS = {
    'FORWARD': pg.K_w,
    'BACK': pg.K_s,
    'UP': pg.K_q,
    'DOWN': pg.K_e,
    'STRAFE_L': pg.K_a,
    'STRAFE_R': pg.K_d,
    'INTERACT': pg.K_f,
    'WEAPON_1': pg.K_1,
    'WEAPON_2': pg.K_2,
    'WEAPON_3': pg.K_3,
}

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

CAM_SPEED = 0.0045
CAM_ROT_SPEED = 0.0005
INIT_CAM_POS = glm.vec3(8, 5, 43)
INIT_CAM_YAW = -90
INIT_CAM_PITCH = 0

MOUSE_SENSITIVITY = 0.0015

# uniform block
UBO_BIND_VALUE = 0
