import pygame
from pygame.locals import *

import graphicsUtils.color as color

def set_text(string, coordx, coordy, fontSize, text_color, surface): 

    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    text = font.render(string, True, text_color) 
    textRect = text.get_rect()
    textRect.topleft = (coordx, coordy) 
    surface.blit(text, textRect)

def line_render_3d(p1, p2, segments, thickness, surface, w, h, crt_cb_lines, crt=True, wr_cb_lines=None):
    if p1[2] > p2[2]:
        p1, p2 = p2, p1
    diff = p2 - p1
    mag = sum(diff * diff) ** 0.5
    diff = diff / mag
    mag = mag / segments
    if crt:
        tmp_cb_lines = color.color_band([crt_cb_lines.getcolor(p1[2]), crt_cb_lines.getcolor(p2[2])])
    else:
        tmp_cb_lines = color.color_band([wr_cb_lines.getcolor(p1[2]), wr_cb_lines.getcolor(p2[2])])
    for i in range(1, segments + 1):
        tmp_p1 = (p1 + diff * ((i - 1) * mag))[:2]
        tmp_p2 = (p1 + diff * (i * mag))[:2]
        tmp_p1[0] *= w
        tmp_p1[1] *= h
        tmp_p2[0] *= w
        tmp_p2[1] *= h
        tmp_p1[0] = int(tmp_p1[0])
        tmp_p1[1] = int(tmp_p1[1])
        tmp_p2[0] = int(tmp_p2[0])
        tmp_p2[1] = int(tmp_p2[1])
        pygame.draw.line(surface, tmp_cb_lines.getcolor(i / segments), tuple(tmp_p1), tuple(tmp_p2), thickness)

def draw_pose(surface, pose, w, h, cb_nodes, crt_cb_lines, results = None, wr_cb_lines = None, flip = False):
    if flip:
        for i in range(len(pose)):
            pose[i][0] = 1 - pose[i][0]
    for (ind, (i, j)) in enumerate([(0, 1), (0, 2), (0, 6), (1, 7), (1, 3), (2, 4), (3, 5), (6, 7), (6, 8), (7, 9), (8, 10), (9, 11)]):
        if(results is None):
            line_render_3d(pose[i], pose[j], 50, 3, surface, w, h, crt_cb_lines)
        else:
            line_render_3d(pose[i], pose[j], 50, 3, surface, w, h, crt_cb_lines, results[ind]>0.7, wr_cb_lines)
    for i in sorted(pose, key=lambda x: x[2], reverse=True):
        pygame.draw.circle(surface, cb_nodes.getcolor(i[2]), (int(i[0] * w), int(i[1] * h)), 5 + int(10 * (1 - i[2])))