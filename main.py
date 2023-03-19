import scripts.menu as menu
import scripts.game as game


def main():
    main_menu = menu.Menu()
    while True:
        main_menu.events()
        main_menu.on_end_of_loop()
        if main_menu.start:
            main_game = game.Game()
            while True:
                if not main_game.end:
                    main_game.events()
                    main_game.on_end_of_loop()
                else:
                    main_menu = menu.Menu()
                    break


if __name__ == '__main__':
    main()
