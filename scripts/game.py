import random
import copy

import pygame as pg

import scripts.menu as menu
import scripts.brick as bricks


class Game:
    def __init__(self):
        self.DOWN_MENU_HEIGHT = 100
        self.settings = menu.load_init()
        self.SIZE = self.settings['Size']
        self.NAME = self.settings['Name']
        self.POINT_SIZE = self.settings['Brick size']
        self.FPS = self.settings['Speed']
        self.HIGH_SCORE = self.settings['High score']
        self.player_score = 0
        self.BACKGROUND = self.settings['Background']
        self.BACKGROUND_2 = menu.GAME_COLORS[self.BACKGROUND]
        self.option_fonts = pg.font.Font('fonts/Comfortaa-VariableFont_wght.ttf', self.SIZE//30)
        self.end = False
        self.corners_matrix = self.create_corners_matrix()
        self.tail = []
        self.curves = []
        self.direction = 'right'
        self.apple = bricks.Apple(self.POINT_SIZE, self.BACKGROUND)
        self.apple_pos = None
        self.background = bricks.Background(self.POINT_SIZE, self.BACKGROUND, self.BACKGROUND_2)
        self.background_brick_surf = self.background.background_brick
        self.snake = bricks.Snake(self.POINT_SIZE, self.BACKGROUND)
        self.start()

        pg.init()
        self.screen = pg.display.set_mode((self.SIZE, self.SIZE + self.DOWN_MENU_HEIGHT))
        pg.display.set_caption('Game', menu.ICON_PATH)
        pg.display.set_icon(pg.image.load(menu.ICON_PATH))
        self.surface = pg.Surface((self.SIZE, self.SIZE))
        self.rect = self.surface.get_rect(topleft=(0, 0))

        self.create_background()
        self.surface_clear = pg.Surface((self.SIZE, self.SIZE))
        self.surface_clear.blit(self.surface, (0, 0))
        self.clock = pg.time.Clock()

    def down_menu(self):
        d_menu = pg.Surface((self.SIZE, self.DOWN_MENU_HEIGHT))
        d_menu.fill(self.settings['Background'])
        d_menu_rect = d_menu.get_rect(topleft=self.rect.bottomleft)
        info_text = self.option_fonts.render('Press m to back to menu, n to quit.', False, self.BACKGROUND_2)
        info_text_rect = info_text.get_rect(midleft=d_menu_rect.midleft)
        player_score_text = self.option_fonts.render(f'Your score: {self.player_score}', False, self.BACKGROUND_2)
        player_score_text_rect = player_score_text.get_rect(midright=d_menu_rect.midright)
        high_score_text = self.option_fonts.render(f'High score - {self.settings["High score"][1]} : {self.settings["High score"][0]}', False, self.BACKGROUND_2)
        high_score_text_rect = high_score_text.get_rect(topright=player_score_text_rect.bottomright)
        self.screen.blit(d_menu, d_menu_rect)
        self.screen.blit(info_text, info_text_rect)
        self.screen.blit(player_score_text, player_score_text_rect)
        self.screen.blit(high_score_text, high_score_text_rect)
    
    def create_corners_matrix(self):
        result = []
        for height in range(0, self.SIZE, self.POINT_SIZE):
            temp = []
            for width in range(0, self.SIZE, self.POINT_SIZE):
                temp.append((width, height))
            result.append(temp.copy())
            temp.clear()
        return result

    def start(self):
        self.direction = 'right'
        pos1 = (((len(self.corners_matrix) // 2)*self.POINT_SIZE, (len(self.corners_matrix) // 2)*self.POINT_SIZE),
                'tail_right')
        pos2 = (((len(self.corners_matrix) // 2 + 1)*self.POINT_SIZE, (len(self.corners_matrix) // 2)*self.POINT_SIZE),
                'head_right')
        self.tail.clear()
        self.tail.append(pos1)
        self.tail.append(pos2)
        if self.player_score > self.HIGH_SCORE[0]:
            self.settings['High score'] = (self.player_score, self.settings['Name'])
            menu.save_init(self.settings)
        self.player_score = 0
        self.apple_pos = self.insert_apple()

    def insert_apple(self):
        pos = (random.randint(1, len(self.corners_matrix) - 2), random.randint(0, len(self.corners_matrix) - 2))
        pos = (pos[0]*self.POINT_SIZE, pos[1]*self.POINT_SIZE)
        while True:
            collisions_with_snake = 0
            for position in self.tail:
                if position[0] == pos:
                    pos = (random.randint(1, len(self.corners_matrix) - 2), random.randint(0, len(self.corners_matrix) - 2))
                    pos = (pos[0] * self.POINT_SIZE, pos[1] * self.POINT_SIZE)
                    collisions_with_snake = 1
                    break
            if  collisions_with_snake == 0: break
        return pos

    def show_bricks(self):
        self.surface.blit(self.surface_clear, (0, 0))
        self.screen.blit(self.surface_clear, (0, 0))
        apple = self.apple.surf
        apple_rect = apple.get_rect(topleft=self.apple_pos)
        self.surface.blit(apple, apple_rect)
        for i in range(len(self.tail)):
            temp_snake = self.tail[i]
            if i == len(self.tail)-1:
                if temp_snake[1] == 'right': snake = self.snake.snake(temp_snake[0], 'head_right')
                elif temp_snake[1] == 'left': snake = self.snake.snake(temp_snake[0], 'head_left')
                elif temp_snake[1] == 'down': snake = self.snake.snake(temp_snake[0], 'head_down')
                elif temp_snake[1] == 'up': snake = self.snake.snake(temp_snake[0], 'head_up')
            elif i == 0:
                if temp_snake[1] == 'right': snake = self.snake.snake(temp_snake[0], 'tail_right')
                elif temp_snake[1] == 'left': snake = self.snake.snake(temp_snake[0], 'tail_left')
                elif temp_snake[1] == 'down': snake = self.snake.snake(temp_snake[0], 'tail_down')
                elif temp_snake[1] == 'up': snake = self.snake.snake(temp_snake[0], 'tail_up')
                else:
                    snake = self.snake.snake(*temp_snake)
            elif not temp_snake[0] in self.curves:
                if temp_snake[1] == 'right': snake = self.snake.snake(temp_snake[0], 'long_right')
                elif temp_snake[1] == 'left':snake = self.snake.snake(temp_snake[0], 'long_left')
                elif temp_snake[1] == 'down': snake = self.snake.snake(temp_snake[0], 'long_down')
                elif temp_snake[1] == 'up': snake = self.snake.snake(temp_snake[0], 'long_up')
            
            if temp_snake[0] in self.curves and i != len(self.tail)-1:
                if self.tail[i][1] == 'left' and self.tail[i+1][1] == 'up':
                    snake = self.snake.snake(temp_snake[0], 'curve_up_right')
                elif self.tail[i][1] == 'left' and self.tail[i+1][1] == 'down':
                    snake = self.snake.snake(temp_snake[0], 'curve_down_right')
                elif self.tail[i][1] == 'right' and self.tail[i+1][1] == 'down':
                    snake = self.snake.snake(temp_snake[0], 'curve_down_left')
                elif self.tail[i][1] == 'right' and self.tail[i+1][1] == 'up':
                    snake = self.snake.snake(temp_snake[0], 'curve_up_left')
                elif self.tail[i][1] == 'up' and self.tail[i+1][1] == 'left':
                    snake = self.snake.snake(temp_snake[0], 'curve_down_left')
                elif self.tail[i][1] == 'up' and self.tail[i+1][1] == 'right':
                    snake = self.snake.snake(temp_snake[0], 'curve_down_right')
                elif self.tail[i][1] == 'down' and self.tail[i+1][1] == 'left':
                    snake = self.snake.snake(temp_snake[0], 'curve_up_left')
                elif self.tail[i][1] == 'down' and self.tail[i+1][1] == 'right':
                    snake = self.snake.snake(temp_snake[0], 'curve_up_right')


            snake_rect = snake.get_rect(topleft=temp_snake[0])
            self.surface.blit(snake, snake_rect)
        temp_pos = [position for (position, direction) in self.tail]
        self.curves = [pos for pos in self.curves if pos in temp_pos]
        self.down_menu()
        self.screen.blit(self.surface, (0, 0))

    def move_snake(self):
        pos, part = self.tail[-1]
        point = self.POINT_SIZE
        direction = self.direction
        size = self.SIZE
        if self.direction == 'right':
            if pos[0] >= size-point:
                self.tail.append(((0, pos[1]), direction))
            else:
                self.tail.append(((pos[0]+point, pos[1]), direction))
        elif self.direction == 'left':
            if pos[0] < point:
                self.tail.append(((size-point, pos[1]), direction))
            else:
                self.tail.append(((pos[0] - point, pos[1]), direction))
        elif self.direction == 'up':
            if pos[1] < point:
                self.tail.append(((pos[0], size-point), direction))
            else:
                self.tail.append(((pos[0], pos[1]-point), direction))
        elif self.direction == 'down':
            if pos[1] >= size-point:
                self.tail.append(((pos[0], 0), direction))
            else:
                self.tail.append(((pos[0], pos[1]+point), direction))
        if self.apple_pos != pos:
            self.tail.remove(self.tail[0])
        else:
            self.apple_pos = self.insert_apple()
            self.player_score += 1
        if pos in [position for (position, part) in self.tail][:-2]:
        # if pos in [position for (position, part) in self.tail][:-1]:
            self.start()

    def create_background(self):
        for line in self.corners_matrix:
            for point in line:
                rect = self.background_brick_surf.get_rect(topleft=point)
                self.surface.blit(self.background_brick_surf, rect)
    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                menu.save_init(self.settings)
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                last_position = self.tail[-1][0]
                if event.key == pg.K_d and self.direction != 'left' and self.direction != 'right':
                    self.direction = 'right'
                    self.curves.append(last_position)
                elif event.key == pg.K_a and self.direction != 'right' and self.direction != 'left':
                    self.direction = 'left'
                    self.curves.append(last_position)
                elif event.key == pg.K_w and self.direction != 'down' and self.direction != 'up':
                    self.direction = 'up'
                    self.curves.append(last_position)
                elif event.key == pg.K_s and self.direction != 'up' and self.direction != 'down':
                    self.direction = 'down'
                    self.curves.append(last_position)
                elif event.key == pg.K_m:
                    if self.player_score > self.HIGH_SCORE[0]:
                        self.settings['High score'] = (self.player_score, self.settings['Name'])
                    self.player_score = 0
                    menu.save_init(self.settings)
                    self.end = True
                elif event.key == pg.K_n:
                    menu.save_init(self.settings)
                    pg.quit()
                    exit()

    def on_end_of_loop(self):
        self.move_snake()
        self.show_bricks()
        self.screen.blit(self.surface, (0, 0))
        pg.display.update()
        self.clock.tick(self.FPS)
