#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 v_color;


void main() {
    vec2 point_uv = 2.0 * gl_PointCoord - 1.0;

    float circle = smoothstep(1.0, 0.7, dot(point_uv, point_uv));
    if (circle < 0.1) discard;

    fragColor = vec4(vec3(circle * v_color), 1);
}
