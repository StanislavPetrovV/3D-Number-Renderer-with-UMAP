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

out vec3 v_color;


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


vec3 hsl2rgb(vec3 c) {
    vec3 rgb = clamp(abs(mod(c.x * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
    return c.z + c.y * (rgb - 0.5) * (1.0 - abs(2.0 * c.z - 1.0));
}


void main() {
    float max_point_size = 12.0;
    float min_point_size = 2.0;

    v_color = abs(normalize(in_position));
    v_color = hsl2rgb(vec3(mix(v_color.r, v_color.b, length(v_color)), 1.0, 0.5));

    vec3 v_position = rotate_world(in_position);

    float dist = length(v_position - cam_pos);
    gl_PointSize = max(max_point_size / dist, min_point_size);

    gl_Position = m_proj * m_view * vec4(v_position, 1);
}
