import pygame
from pygame import gfxdraw


def draw_character(game_surface, game_characters, name):

    for poly, attributes in game_characters[name].polys.items():
        attributes.x = 0
        attributes.y = 0
        attributes.roll = 0
        attributes.scale = 0
        for move in game_characters[name].active_animations:
            if move in game_characters[name].animations:
                print("frame ", game_characters[name].animations[move].frame)
                if poly in game_characters[name].animations[move].key_frames:
                    print(poly, "-->", move)
                    for index, event in enumerate(game_characters[name].animations[move].key_frames[poly]):

                        if event[0] < game_characters[name].animations[move].frame * game_characters[name].animations[move].speed<= \
                                game_characters[name].animations[move].key_frames[poly][index + 1][0]:
                            first_mark = event
                            second_mark = game_characters[name].animations[move].key_frames[poly][index + 1]
                            tween_length = (second_mark[0] - first_mark[0])
                            tween_progress = ((game_characters[name].animations[move].frame * game_characters[name].animations[move].speed) - first_mark[0]) / tween_length
                            x_add = (first_mark[1] + (second_mark[1] - first_mark[1]) * tween_progress)
                            y_add = first_mark[2] + (second_mark[2] - first_mark[2]) * tween_progress
                            roll_add = first_mark[3] + ((second_mark[3] - first_mark[3]) * tween_progress)
                            scale_add = first_mark[4] + (second_mark[4] - first_mark[4]) * tween_progress
                            attributes.roll += roll_add
                            attributes.scale += scale_add
                            attributes.x += (x_add * game_characters[name].scale)
                            attributes.y += (y_add * game_characters[name].scale)
                            print(roll_add)
                            print("progress --> ", tween_progress)

        if attributes.parent == "origin":
            attributes.x += game_characters[name].x
            attributes.y += game_characters[name].y
            attributes.roll += game_characters[name].roll
            attributes.scale += game_characters[name].scale
        else:
            attributes.x += game_characters[name].polys[attributes.parent[0]].translated_anchors()[attributes.parent[1]][0]
            attributes.y += game_characters[name].polys[attributes.parent[0]].translated_anchors()[attributes.parent[1]][1]
            attributes.roll += game_characters[name].polys[attributes.parent[0]].roll
            attributes.scale += game_characters[name].scale

        bounding_rect = pygame.draw.polygon(game_surface, attributes.color, attributes.translated_coords())
        pygame.gfxdraw.filled_polygon(game_surface, attributes.translated_coords(), attributes.color)
        #pygame.draw.rect(game_surface, (255, 0, 0), bounding_rect, 1)
        pygame.gfxdraw.aapolygon(game_surface, attributes.translated_coords(), attributes.color)
    game_characters[name].advance_frame()


