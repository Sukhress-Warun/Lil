import pygame
from pygame.locals import *
import pickle

import graphicsUtils.color as color
from pose.transform import change_coord, fit_pose_scale
from videoUtils.live_poses import get_live_pose
from pose.images_to_poses import images_to_poses
from pose.compare import comp_poses
from graphicsUtils.draw import draw_pose, set_text
from videoUtils.video import frames_count, video_to_image


video_path = "D:\\codes\\python files\\live in lab\\final.mp4" # input("Enter video path: ")  
destination_path = "D:\\codes\\python files\\lil\\data".replace("\\", '/').strip('/')+'/' #input("Enter destination path: ").replace("\\", '/').strip('/')+'/'
practice_name = "try" # input("Enter practice name: ")
destination_path += practice_name + '/'
skip = 1
limit = 1000

try:
    with open(destination_path+"poses.bin",'rb') as f:
        poses_array, paths = pickle.load(f)
        print("\nretrieved poses")
except:
    video_to_image(video_path, destination_path, limit, skip=skip)
    print("\ngetting poses from images\n")
    poses_array, paths = images_to_poses([destination_path+str(i)+'.jpg' for i in range(0, min(int(frames_count(video_path)//skip), limit))], get_images_path=True)
    with open(destination_path+"poses.bin",'wb') as f:
        pickle.dump([poses_array, paths],f)

pygame.init()
info = pygame.display.Info()
w,h = info.current_w-50, info.current_h-50
side = min(w,h)
surface = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

cb_nodes = color.color_band([(255, 0, 0), (50, 50, 50)])
wr_cb_lines = color.color_band([(255, 0, 0), (50, 50, 50)])
crt_cb_lines = color.color_band([(0, 255, 0), (50, 50, 50)])
cb_video = color.color_band([(0, 0, 255), (50, 50, 50)])


user_pose = None
current_pose_index = 0
steady = 0
steady_limit = 5
results = [0]*12
image_res =  (w/3, (w/3) * 0.5625)

prev_frame = "lastly: None, 0%"
current_frame = "current: None, 0%"
photo = pygame.image.load(paths[current_pose_index]).convert_alpha()
flipped = pygame.transform.flip(photo, True, False)
targetSize = pygame.transform.scale(flipped, image_res)

for i in get_live_pose():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if (len(i)) :
        user_pose = change_coord(i)
        results = comp_poses(user_pose, change_coord(poses_array[current_pose_index]))
        current_frame = f"current: {current_pose_index}, {round((sum(results)/12)*100, 2)}%"
    else:
        user_pose = None
        current_frame = "current: None, 0%"
        steady = 0
        results = [0]*12

    surface.fill((0, 0, 0))
    
    draw_pose(surface, change_coord(poses_array[current_pose_index]), side, side, cb_video, cb_video, flip=True)
    if len(i):
        user_pose = fit_pose_scale(user_pose, change_coord(poses_array[current_pose_index]), limb_ind = (0, 1))
        draw_pose(surface, user_pose, side, side, cb_nodes, crt_cb_lines, results, wr_cb_lines ,flip=True)
    
    if sum(results) > 11:
        steady += 1
        if steady > steady_limit:
            prev_frame = f"lastly: {current_pose_index}, {round((sum(results)/12)*100, 2)}%"
            steady = 0
            current_pose_index += 1
            if current_pose_index >= len(poses_array):
                current_pose_index = 0
            photo = pygame.image.load(paths[current_pose_index]).convert_alpha()
            flipped = pygame.transform.flip(photo, True, False)
            targetSize = pygame.transform.scale(flipped, image_res)
            # print(current_pose_index, sum(results))
    else:
        steady = 0
    
    surface.blit(targetSize, (w - image_res[0], h - image_res[1]))
    set_text(prev_frame, 0, 10, 20, (150, 150, 255), surface)
    set_text(current_frame, 0, 40, 20, (255, 150, 150), surface)
    pygame.display.update()
    clock.tick(60)