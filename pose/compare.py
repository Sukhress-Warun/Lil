import numpy as np


def comp_directions(dirs1, dirs2):
    similarities=[]
    for i in range(12):
        similarities.append(np.dot(dirs1[i],dirs2[i]))
    return similarities

def get_directions_from_pose(pose):
    directions=[]
    for (i, j) in [(0, 1), (0, 2), (0, 6), (1, 7), (1, 3), (2, 4), (3, 5), (6, 7), (6, 8), (7, 9), (8, 10), (9, 11)]:
        diff = pose[i] - pose[j]
        mag = sum(diff * diff) ** 0.5
        diff = diff / mag
        directions.append(diff)
    return np.array(directions)

def comp_poses(pose1, pose2):
    return comp_directions(get_directions_from_pose(pose1), get_directions_from_pose(pose2))