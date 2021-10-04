import pygame
from board import *
from uielements import *
import sys

class Application:
    def __init__(self):
        pass

    def execute(self):
        # intialize the pygame
        pygame.init()

        pygame.display.set_caption("The Best Lines")
        icon = pygame.image.load('lines.png')
        pygame.display.set_icon(icon)

        # initialize fonts
        score_font = pygame.font.Font('freesansbold.ttf', 32)
        big_font = pygame.font.Font('freesansbold.ttf', 48)

        # create the screen
        size = (2*BOARD_OFFSET_X + SQUARE_SIZE*FIELD_SIZE,
                2*BOARD_OFFSET_X + BOARD_OFFSET_Y + PLAY_BTN_HEIGHT + SQUARE_SIZE*FIELD_SIZE)
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        
        show_game_over = False
        board = Board()       
        score = ScoreDisplay(score_font)
        btn = NewGameButton(big_font)
        game_over = GameOverDisplay(big_font)

        # fill background and display unchangable elements
        screen.fill(BACKGROUND)
        btn.update(screen)

        # TODO ignore events that are not QUIT or MOUSEBUTTONDOWN

        # main game loop
        while True:
            # limit to 60 FPS
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn.was_clicked(event):
                        board.reset_game()
                        show_game_over = False
                        continue
                    if not show_game_over and board.was_clicked(event) and not board.is_animating():
                        if board.handle_event(event) == GameManager.GAME_OVER:
                            show_game_over = True
                    pygame.event.clear(eventtype=pygame.MOUSEBUTTONDOWN) 
                
            
            # update visuals
            score.update(screen, board.get_score())  
            board.update(screen)
            if show_game_over:
                game_over.update(screen)
            pygame.display.update()

if __name__ == '__main__':
    Application().execute()
