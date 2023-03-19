import json
from string import ascii_lowercase, digits

import pygame as pg



# constants
INIT_FILE = 'snake.json'
INIT_DEFAULT = {'Name': 'player',
                'Size': 600,
                'Brick size': 50,
                'Speed': 10,
                'High score': (0, 'player'),
                'Background': 'Black'
                }
GAME_COLORS = {'Black': 'White',
               'Blue': 'Yellow'}
LOGO_PATH = 'images/logo.png'
ICON_PATH = 'images/icon.ico'
MENU_SIZE = 600
DOWN_MENU_HEIGHT = 200
OPTIONS_HEIGHT = 50


def make_cycle_gen(items):
    while True:
        for item in items:
            yield item
color_cycle = make_cycle_gen(GAME_COLORS)
size_cycle = make_cycle_gen((500, 600, 900))
point_size_cycle = make_cycle_gen((30, 50))
speed_cycle = make_cycle_gen((10, 20, 30))

#load settings
def load_init():
    try:
        return json.load(open(INIT_FILE, 'r'))
    except FileNotFoundError:
        with open(INIT_FILE, 'w') as f:
            json.dump(INIT_DEFAULT, f, indent=4)
        return INIT_DEFAULT

#save settings
def save_init(settings):
    json.dump(settings, open(INIT_FILE, 'w'), indent=4)


class Menu:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = load_init()
        self.screen = pg.display.set_mode((MENU_SIZE, MENU_SIZE))
        self.surface = pg.Surface((MENU_SIZE, MENU_SIZE))
        self.surface.fill('Black')
        pg.display.set_caption('Snake', ICON_PATH)
        pg.display.set_icon(pg.image.load(ICON_PATH))
        self.title_font = pg.font.Font('fonts/karma future.otf', 60)
        self.option_fonts = pg.font.Font('fonts/karma future.otf', 30)
        self.options_pos_dict = {}
        self._make_down_screen()
        self._make_options()
        self._checking = 0

        # Change to False
        self.start = False

        self.screen.blit(self.surface, (0, 0))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_init(self.settings)
                pg.quit()
                exit()
            for item in self.options_pos_dict:
                if self.options_pos_dict[item].collidepoint(pg.mouse.get_pos()):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if item == 'Size':
                            self.settings['Size'] = next(size_cycle)
                        elif item == 'Name':
                            self._change_name()
                        elif item == 'Brick size':
                            self.settings['Brick size'] = next(point_size_cycle)
                        elif item == 'Speed':
                            self.settings['Speed'] = next(speed_cycle)
                        elif item == 'Background':
                            self.settings['Background'] = next(color_cycle)
                        self._make_options()
                        self.screen.blit(self.surface, (0, 0))
            if self.circle_play.collidepoint(pg.mouse.get_pos()):
                if event.type == pg.MOUSEBUTTONDOWN:
                    save_init(self.settings)
                    self.start = True

    def _change_name(self):
        name = self.settings['Name']
        temp_old_name = name
        while True:
            if pg.mouse.get_pressed()[0] and not self.options_pos_dict['Name'].collidepoint(pg.mouse.get_pos()):
                self.settings['Name'] = temp_old_name
                break
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        save_init(self.settings)
                        exit()
                    if event.type == pg.KEYDOWN:
                        try:
                            if event.key == pg.K_BACKSPACE:
                                if len(name) < 1: continue
                                name = name[:-1]
                            elif event.key == pg.K_RETURN:
                                save_init(self.settings)
                                self._checking = 1
                                break
                            else:
                                if chr(event.key) in ascii_lowercase+digits+' ' and len(name) < 18:
                                    name += chr(event.key)
                                else:
                                    continue
                            self.settings['Name'] = name
                            self.refresh_options_view()
                        except Exception as e:
                            print(e)
            if self._checking != 0:
                save_init(self.settings)
                self._checking = 0
                break


    def _make_option_field(self, option):
        text = self.option_fonts.render(f'{option:20}', False, 'White')
        text_rect = text.get_rect(midleft=(OPTIONS_HEIGHT // 10, OPTIONS_HEIGHT // 2))
        if option != 'High score':
            option_field = self.option_fonts.render(str(self.settings[option]), False, 'Red')
        else:
            option_field = self.option_fonts.render(' : '.join([str(el) for el in self.settings[option]]), False, 'Red')
        option_field_rect = option_field.get_rect(
            midleft=(text_rect.midright[0] + OPTIONS_HEIGHT // 5, text_rect.midright[1]))
        surf = pg.Surface((text_rect.size[0] + option_field_rect.size[0] + OPTIONS_HEIGHT, OPTIONS_HEIGHT))
        surf.fill('grey33')
        surf.blit(text, text_rect)
        surf.blit(option_field, option_field_rect)
        return surf

    def _make_options(self):
        options_field = pg.Surface((MENU_SIZE, MENU_SIZE - DOWN_MENU_HEIGHT))
        options_field.fill('gray50')
        options_field_rect = options_field.get_rect(topleft=(0, 0))
        height = OPTIONS_HEIGHT // 2
        for option in self.settings:
            surf = self._make_option_field(option)
            surf_rect = surf.get_rect(topleft=(OPTIONS_HEIGHT, height + 10))
            options_field.blit(surf, surf_rect)
            height += OPTIONS_HEIGHT + 10
            self.options_pos_dict[option] = surf_rect
        self.surface.blit(options_field, options_field_rect)
        circle_play_radius = 75
        self.circle_play = pg.draw.circle(self.surface, 'Red', (options_field_rect.midright[0]-circle_play_radius,
                                                           options_field_rect.midright[1]), circle_play_radius)
        play_text = self.option_fonts.render('Play!', False, 'Green')
        play_text_rect = play_text.get_rect(center=self.circle_play.center)
        self.surface.blit(play_text, play_text_rect)

    def _make_down_screen(self):
        surf = pg.Surface((MENU_SIZE, DOWN_MENU_HEIGHT))
        surf_rect = surf.get_rect(bottomleft=(0, MENU_SIZE))
        pg.draw.aaline(surf, 'Green', (0, 0), (MENU_SIZE, 0), 10)
        logo = pg.image.load(LOGO_PATH).convert_alpha()
        logo_rect = logo.get_rect(midleft=(0, DOWN_MENU_HEIGHT // 2))
        surf.blit(logo, logo_rect)
        title = self.title_font.render('Snake', True, 'Green')
        title_rect = title.get_rect(midleft=(logo_rect.midright[0], logo_rect.midright[1]))
        surf.blit(title, title_rect)
        self.button_surf = pg.Surface((OPTIONS_HEIGHT*2, OPTIONS_HEIGHT*2))
        self.button_surf_rect = self.button_surf.get_rect(midleft=title_rect.midright)
        self.button_surf.fill('Green')
        self.button_text = self.option_fonts.render('pg', True, 'Red')
        self.button_text_rect = self.button_text.get_rect(center=self.button_surf_rect.center)
        surf.blit(self.button_surf, self.button_surf_rect)
        surf.blit(self.button_text, self.button_text_rect)
        self.surface.blit(surf, surf_rect)

    def refresh_options_view(self):
        self._make_options()
        self.screen.blit(self.surface, (0, 0))
        pg.display.update()

    def on_end_of_loop(self):
        pg.display.update()
        self.clock.tick(60)
