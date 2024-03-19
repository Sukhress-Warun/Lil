import pygame
from pygame.locals import *

import graphicsUtils.color as color
from pose.transform import change_coord
from videoUtils.live_poses import get_live_pose
from pose.images_to_poses import images_to_poses
from pose.compare import comp_poses
from graphicsUtils.draw import draw_pose

pygame.init()
info = pygame.display.Info()
side = min(info.current_w, info.current_h)-50
w,h = side,side
surface = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

cb_nodes = color.color_band([(255, 0, 0), (50, 50, 50)])
wr_cb_lines = color.color_band([(255, 0, 0), (50, 50, 50)])
crt_cb_lines = color.color_band([(0, 255, 0), (50, 50, 50)])

img_pose = change_coord(images_to_poses(['data/try/79.jpg'])[0])
user_pose = None

for i in get_live_pose():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if (len(i)) :
        user_pose = change_coord(i)
        results = comp_poses(user_pose, img_pose)

    surface.fill((0, 0, 0))
    
    draw_pose(surface, img_pose, w, h, cb_nodes, crt_cb_lines)
    if len(i):
        draw_pose(surface, user_pose, w, h, cb_nodes, crt_cb_lines, results, wr_cb_lines)

    pygame.display.update()
    clock.tick(60)