import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

vertices_cube = np.array([
    [-1, 1, 1,-1,-1, 1, 1,-1],
    [-1,-1, 1, 1,-1,-1, 1, 1],
    [-1,-1,-1,-1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1]
])

faces_cube = np.array([
    [0, 1, 5, 4],
    [1, 2, 6, 5],
    [2, 3, 7, 6],
    [3, 0, 4, 7],
    [0, 1, 2, 3],
    [4, 5, 6, 7]
])


def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def apply_transformation(vertices, transformation_matrix):
    return transformation_matrix @ vertices


def rotation_matrix(vx, vy, vz, theta):
    v = np.array([vx, vy, vz])
    v = v / np.linalg.norm(v)
    vx, vy, vz = v

    J = np.array([
        [0, -vz, vy, 0],
        [vz, 0, -vx, 0],
        [-vy, vx, 0, 0],
        [0, 0, 0, 0]
    ])

    R = np.eye(4) + np.sin(theta) * J + (1 - np.cos(theta)) * (J @ J)
    return R


def draw_shape(ax, vertices, faces, color):
    vertices = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices[faces], facecolors=color, edgecolors='k', linewidths=0.2))


# scale transformation
sx, sy, sz = 1.5, 0.5, 2.0
S = scale_matrix(sx, sy, sz)

scaled_vertices_cube = apply_transformation(vertices_cube, S)

#tranlate transformation
tx, ty, tz = 2.0, 1.0, -1.5
T = translation_matrix(tx, ty, tz)

translated_vertices_cube = apply_transformation(vertices_cube, T)
scaled_then_translated_vertices = apply_transformation(scaled_vertices_cube, T)
translated_then_scaled_vertices = apply_transformation(translated_vertices_cube, S)

#rotation transformation
vx, vy, vz = 1, 1, 0
theta = np.pi / 4

R = rotation_matrix(vx, vy, vz, theta)
rotated_vertices_cube = apply_transformation(vertices_cube, R)


fig = plt.figure()
ax = fig.add_subplot(projection='3d', proj_type='ortho')
draw_shape(ax, rotated_vertices_cube, faces_cube, 'orange')

scale_factor = 3
origin = np.array([[0, 0, 0], [scale_factor * vx, scale_factor * vy, scale_factor * vz]])
ax.quiver(*origin[0], *origin[1], color='red', arrow_length_ratio=0.2, linewidth=2)

ax.set_box_aspect([1, 1, 1])
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(-2, 2)
ax.view_init(azim=-37.5, elev=30)
plt.show()


# fig = plt.figure(figsize=(12, 6))
#
# ax1 = fig.add_subplot(121, projection='3d', proj_type='ortho')
# draw_shape(ax1, scaled_then_translated_vertices, faces_cube, 'red')
# ax1.set_title("Перемещение, затем масштабирование (ST)")
# ax1.set_xlim(-5, 5); ax1.set_ylim(-5, 5); ax1.set_zlim(-5, 5)
# ax1.view_init(azim=-37.5, elev=30)
#
# ax2 = fig.add_subplot(122, projection='3d', proj_type='ortho')
# draw_shape(ax2, translated_then_scaled_vertices, faces_cube, 'blue')
# ax2.set_title("Масштабирование, затем перемещение (TS)")
# ax2.set_xlim(-5, 5); ax2.set_ylim(-5, 5); ax2.set_zlim(-5, 5)
# ax2.view_init(azim=-37.5, elev=30)
#
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d', proj_type='ortho')
# draw_shape(translated_vertices_cube, faces_cube, 'purple')
#
# ax.set_box_aspect([1, 1, 1])
# ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-3, 3)
# ax.view_init(azim=-37.5, elev=30)
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d', proj_type = 'ortho')