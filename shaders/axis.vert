#version 330 core

layout (location = 0) in vec3 in_position;

layout (std140) uniform UBO {
    mat4  m_proj;
    vec3  u_center;
    float rot_speed;
    mat4  m_view;
    vec3  cam_pos;
    float u_time;
};


mat2 rot(float a) {
    float sa = sin(a);
    float ca = cos(a);
    return mat2(ca, -sa, sa, ca);
}


vec3 rotate_world(vec3 in_position) {
    vec3 v_position = in_position;

    v_position -= u_center;
    v_position.xz *= rot(u_time * rot_speed);
    v_position += u_center;

    return v_position;
}


void main() {
    vec3 v_position = rotate_world(in_position);

    gl_Position = m_proj * m_view * vec4(v_position, 1.0);
}