from game import Game
import pygame

def main():
    pygame.font.init()
    game = Game()
    game.main()

if __name__ == '__main__':
    try:
        main()
    except pygame.error as e:
        if str(e) == 'display Surface quit':
            print('QUIT')