import pygame as pg

pg.init()

# images paths
LONG_IMG = 'images/long.png'
HEAD_IMG = 'images/head.png'
TAIL_IMG = 'images/tail.png'
CURVE_IMG = 'images/curve.png'
APPLE_IMG = 'images/apple.png'

# rotated images
long_up = pg.image.load(LONG_IMG)
long_down = pg.transform.rotate(long_up, 180)
long_left = pg.transform.rotate(long_up, 90)
long_right = pg.transform.rotate(long_up, -90)
head_up = pg.image.load(HEAD_IMG)
head_down = pg.transform.rotate(head_up, 180)
head_left = pg.transform.rotate(head_up, 90)
head_right = pg.transform.rotate(head_up, -90)
tail_up = pg.image.load(TAIL_IMG)
tail_down = pg.transform.rotate(tail_up, 180)
tail_left = pg.transform.rotate(tail_up, 90)
tail_right = pg.transform.rotate(tail_up, -90)
curve_down_left = pg.image.load(CURVE_IMG)
curve_down_right = pg.transform.rotate(curve_down_left, 90)
curve_up_left = pg.transform.rotate(curve_down_left, -90)
curve_up_right = pg.transform.rotate(curve_up_left, 180)
curve_up_right = pg.transform.flip(curve_up_right, False, True)



class Background:
    def __init__(self, size, background_color, second_color):
        self.size = size
        self.background_color = background_color
        self.second_color = second_color
        self.background_brick = self.create_brick()

    def create_brick(self):
        brick_surf = pg.Surface((self.size, self.size))
        brick_surf_rect = brick_surf.get_rect(topleft=(0, 0))
        brick_surf.fill(self.background_color)
        brick_scnd = pg.Surface((self.size // 8, self.size // 8))
        brick_scnd_rect = brick_scnd.get_rect(center=brick_surf_rect.center)
        brick_scnd.fill(self.second_color)
        brick_surf.blit(brick_scnd, brick_scnd_rect)
        return brick_surf


class Snake:
    def __init__(self, size, background_color):
        self.size = size
        self.background_color = background_color
        # scalling snake sprites
        self.long_up = pg.transform.scale(long_up, (self.size, self.size))
        self.long_down = pg.transform.scale(long_down, (self.size, self.size))
        self.long_left = pg.transform.scale(long_left, (self.size, self.size))
        self.long_right = pg.transform.scale(long_right, (self.size, self.size))
        self.head_up = pg.transform.scale(head_up, (self.size, self.size))
        self.head_down = pg.transform.scale(head_down, (self.size, self.size))
        self.head_left = pg.transform.scale(head_left, (self.size, self.size))
        self.head_right = pg.transform.scale(head_right, (self.size, self.size))
        self.tail_up = pg.transform.scale(tail_up, (self.size, self.size))
        self.tail_down = pg.transform.scale(tail_down, (self.size, self.size))
        self.tail_left = pg.transform.scale(tail_left, (self.size, self.size))
        self.tail_right = pg.transform.scale(tail_right, (self.size, self.size))
        self.curve_down_left = pg.transform.scale(curve_down_left, (self.size, self.size))
        self.curve_down_right = pg.transform.scale(curve_down_right, (self.size, self.size))
        self.curve_up_left = pg.transform.scale(curve_up_left, (self.size, self.size))
        self.curve_up_right = pg.transform.scale(curve_up_right, (self.size, self.size))

    def snake(self, corner, direction):
        if direction == 'long_up':
            surf = self.long_up
        elif direction == 'long_down':
            surf = self.long_down
        elif direction == 'long_left':
            surf = self.long_left
        elif direction == 'long_right':
            surf = self.long_right
        elif direction == 'head_up':
            surf = self.head_up
        elif direction == 'head_down':
            surf = self.head_down
        elif direction == 'head_left':
            surf = self.head_left
        elif direction == 'head_right':
            surf = self.head_right
        elif direction == 'tail_up':
            surf = self.tail_up
        elif direction == 'tail_down':
            surf = self.tail_down
        elif direction == 'tail_left':
            surf = self.tail_left
        elif direction == 'tail_right':
            surf = self.tail_right
        elif direction == 'curve_down_left':
            surf = self.curve_down_left
        elif direction == 'curve_down_right':
            surf = self.curve_down_right
        elif direction == 'curve_up_left':
            surf = self.curve_up_left
        elif direction == 'curve_up_right':
            surf = self.curve_up_right
        else:
            surf = pg.Surface((self.size, self.size))
            surf.fill('Green')
        surf_res = pg.Surface((self.size, self.size))
        surf_res.fill(self.background_color)
        rect = surf.get_rect(topleft=(0, 0))
        surf_res.blit(surf, rect)
        return surf_res


class Apple:
    def __init__(self, size, background):
        self.size = size
        self.background = background
        self.apple = pg.image.load(APPLE_IMG)
        self.apple = pg.transform.scale(self.apple, (self.size, self.size))
        self.surf = self.create_apple()

    def create_apple(self):
        surf = pg.Surface((self.size, self.size))
        surf.fill(self.background)
        surf.blit(self.apple, (0, 0))
        return surf