import yaml
from rotate import rotate


class Poly(object):
    def __init__(self, x, y, roll, coords, color, parent, anchors, scale):
        self.x = x
        self.y = y
        self.roll = roll
        self.coords = coords
        self.color = color
        self.parent = parent
        self.anchors = anchors
        self.scale = scale

    def translated_coords(self):
        translated_coords = []
        for pair in self.coords:

            rotated_coords = rotate(pair, origin=(0, 0), degrees=self.roll)
            translated_coords.append((rotated_coords[0] * self.scale + self.x,
                                      rotated_coords[1] * self.scale + self.y))
        return translated_coords

    def translated_anchors(self):
        translated_anchors = []
        for pair in self.anchors:
            rotated_anchors = rotate(pair, origin=(0, 0), degrees=self.roll)
            translated_anchors.append((rotated_anchors[0] * self.scale + self.x,
                                       rotated_anchors[1] * self.scale + self.y))
        return translated_anchors


class Actor(object):
    def __init__(self, x, y, roll, scale, polys, name, animations, active_animations):
        self.x = x
        self.y = y
        self.roll = roll
        self.scale = scale
        self.polys = polys
        self.name = name
        self.animations = animations
        self.active_animations = active_animations

    def advance_frame(self):
        for move in self.animations:
            if move in self.active_animations:
                self.animations[move].advance_frame()

    def activate_animation(self, move, speed):
        if move not in self.active_animations and move in self.animations:
            self.active_animations.append(move)
            self.animations[move].speed = speed





class Move(object):
    def __init__(self, frame, duration, key_frames, speed):
        self.frame = frame
        self.duration = duration
        self.key_frames = key_frames
        self.speed = speed

    def advance_frame(self):
        self.frame += 1
        if self.frame >= (self.duration / self.speed):
            self.frame = 0
        #print(self.frame, self.duration)


def load_characters(file):
    game_characters = {}
    with open(file) as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)

        for doc in data:
            for k, v in doc.items():
                print(k)
                polys = {}
                for k1, v1 in v['polys'].items():
                    nodes = [[0, 0]]
                    color = [255, 255, 255]
                    parent = "origin"
                    anchors = [[0, 0]]
                    if "nodes" in v1.keys():
                        nodes = v1['nodes']
                    if "color" in v1.keys():
                        color = v1['color']
                    if "parent" in v1.keys():
                        parent = v1['parent']
                    if "anchors" in v1.keys():
                        anchors = v1['anchors']
                    poly_name = k1
                    polys[poly_name] = Poly(0, 0, 0, nodes, color, parent, anchors, 1)
                animations = {}
                if "moves" in v.keys():
                    for k1, v1 in v['moves'].items():
                        move_name = k1
                        duration = 0
                        key_frames = []
                        if "length" in v1.keys():
                            duration = v1['length']
                        if "key_frames" in v1.keys():
                            key_frames = v1['key_frames']
                        animations[move_name] = Move(0, duration, key_frames, 1)
                game_characters[k] = Actor(0, 0, 0, 1, polys, k, animations, [])
        return game_characters
