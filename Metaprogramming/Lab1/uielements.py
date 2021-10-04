import pygame
from visualparameters import *
from gameparameters import *

class ScoreDisplay:
    def __init__(self, font):
        self.rect = pygame.Rect(
            BOARD_OFFSET_X,
            20,
            FIELD_SIZE*SQUARE_SIZE,
            50
        )
        self.surface = pygame.Surface([self.rect.width, self.rect.height])

        self.font = font

    def update(self, screen, score):
        self.surface.fill(BACKGROUND)
        text = self.font.render("SCORE : " + str(score), True, TEXT_COLOR)
        self.surface.blit(text, (0, 0))
        screen.blit(self.surface, (self.rect.left, self.rect.top))

class NewGameButton:
    def __init__(self, font):
        self.rect = pygame.Rect(
            (2*BOARD_OFFSET_X+FIELD_SIZE*SQUARE_SIZE-PLAY_BTN_WIDTH)//2,
            BOARD_OFFSET_Y+FIELD_SIZE*SQUARE_SIZE+BOARD_OFFSET_X,
            PLAY_BTN_WIDTH,
            PLAY_BTN_HEIGHT
        )

        # transparent background
        self.surface = pygame.Surface(
            [self.rect.width, self.rect.height],
            pygame.SRCALPHA,
            32
        ).convert_alpha()

        self.font = font

    def update(self, screen):
        pygame.draw.rect(
            self.surface,
            TEXT_COLOR,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=4
        )
        text = self.font.render("NEW GAME", True, WHITE)
        self.surface.blit(
            text,
            ((self.rect.width - text.get_rect().width)//2,
             (self.rect.height - text.get_rect().height)//2)
        )
        screen.blit(
            self.surface,
            (self.rect.left, self.rect.top)
        )

    def was_clicked(self, event):
        return True if self.rect.collidepoint(event.pos) else False

class GameOverDisplay:
    def __init__(self, font):
        self.rect = pygame.Rect(
            BOARD_OFFSET_X, BOARD_OFFSET_Y, FIELD_SIZE*SQUARE_SIZE, FIELD_SIZE*SQUARE_SIZE)
        self.surface = pygame.Surface(
            [self.rect.width, self.rect.height], pygame.SRCALPHA, 32)

        self.font = font

    def update(self, screen):
        self.surface.fill(SEMI_TRANSPARENT_WHITE)
        text = self.font.render("GAME OVER", True, TEXT_COLOR)
        self.surface.blit(
            text,
            ((self.rect.width - text.get_rect().width)//2,
             (self.rect.height - text.get_rect().height)//2)
        )
        screen.blit(self.surface, (self.rect.left, self.rect.top))
