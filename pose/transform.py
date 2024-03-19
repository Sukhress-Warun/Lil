import numpy as np

def change_coord(points):
    ## method 1 - unit cube

    # min_x, min_y, min_z = map(min, (points[:, 0], points[:, 1], points[:, 2]))
    # max_x, max_y, max_z = map(max, (points[:, 0], points[:, 1], points[:, 2]))

    # min_arr = np.array([min_x, min_y, min_z])
    # max_arr = np.array([max_x, max_y, max_z])

    # points = points - min_arr
    # max_arr = max_arr - min_arr

    # points = points / max_arr
    # return points
    

    ## method 2 - origin misunderstood unit sphere

    # max_point=max(points,key=lambda x:sum(x*x)**0.5)
    # points = points / (sum(max_point*max_point)**0.5)
    # points = points * 0.5
    # points = points + np.array([0.5,0.5,0.5])
    # return points


    ## method 3 - inside unit sphere midpoint

    # midpoint = sum(points)/points.shape[0]
    # points = points - midpoint
    # max_point=max(points,key=lambda x:sum(x*x)**0.5)
    # points = points / (sum(max_point*max_point)**0.5)
    # points = points * 0.5
    # points = points + np.array([0.5,0.5,0.5])
    # return points


    ## method 4 - inside unit sphere hip center as origin (6-7 hip mid point)

    hipmidpoint=(points[6]+points[7])/2
    points = points - hipmidpoint
    max_point=max(points,key=lambda x:sum(x*x)**0.5)
    points = points / (sum(max_point*max_point)**0.5)
    points = points * 0.5
    points = points + np.array([0.5,0.5,0.5])
    return points

def limb_length(pose, limb_ind):
    limb = pose[limb_ind[0]] - pose[limb_ind[1]]
    return sum(limb*limb)**0.5

def fit_pose_scale(user_pose, pose, limb_ind = (0, 1), node = None):
    user_pose = user_pose - np.array([0.5,0.5,0.5])
    pose = pose - np.array([0.5,0.5,0.5])
    if node:
        user_pose_node_len = sum(user_pose[node]*user_pose[node])**0.5
        pose_node_len = sum(pose[node]*pose[node])**0.5
        if user_pose_node_len < pose_node_len:
            user_pose = user_pose * (pose_node_len / user_pose_node_len)
        user_pose = user_pose + np.array([0.5,0.5,0.5])
        return user_pose

    user_limb_len = limb_length(user_pose, limb_ind)
    pose_limb_len = limb_length(pose, limb_ind)
    if user_limb_len < pose_limb_len:
        user_pose = user_pose * (pose_limb_len / user_limb_len)
    user_pose = user_pose + np.array([0.5,0.5,0.5])
    return user_pose