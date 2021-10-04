import pygame
from visualparameters import *
from gamemanager import *
import copy

class Board:
    def __init__(self):
        # initialize board surface
        self.rect = pygame.Rect(
            BOARD_OFFSET_X, BOARD_OFFSET_Y, FIELD_SIZE*SQUARE_SIZE, FIELD_SIZE*SQUARE_SIZE)
        self.surface = pygame.Surface(
            [self.rect.width, self.rect.height])

        self.cells = [[Board.__Cell(i, j) for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
        self.game = GameManager()
        self.board_buffer = copy.deepcopy(self.game.board)

        # position of selected ball
        self.selected = None

        self.animation = None

    def is_animating(self):
        return True if self.animation != None else False

    def get_score(self):
        return self.game.score

    def reset_game(self):
        self.game = GameManager()
        self.board_buffer = copy.deepcopy(self.game.board)
        self.selected = None
        self.animation = None

    def update(self, screen):
        self.surface.fill(WHITE)
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                self.cells[i][j].update(
                    self.surface,
                    self.board_buffer[i][j],
                    True if self.selected == [i, j] else False,
                    True if self.animation != None and self.animation.is_animated([i, j]) else False
                )
        self.__draw_board()

        if self.animation != None:
            self.animation.update(self.surface)
            if self.animation.is_finished():
                self.animation = None
                self.board_buffer = copy.deepcopy(self.game.board)

        screen.blit(
            self.surface,
            (self.rect.left, self.rect.top)
        )

    def __draw_board(self):
        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                pygame.draw.rect(
                    self.surface,
                    BACKGROUND,
                    (j*SQUARE_SIZE, i*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    width=5
                )

    def __pick_cell(self, event):
        x = event.pos[0]
        y = event.pos[1]

        return (y - BOARD_OFFSET_Y) // SQUARE_SIZE, (x - BOARD_OFFSET_X) // SQUARE_SIZE

    def was_clicked(self, event):
        return True if self.rect.collidepoint(event.pos) else False

    def handle_event(self, event):
        i, j = self.__pick_cell(event)

        result = 0
        if self.selected == None:
            if self.game.board[i][j] > 0:
                self.selected = [i, j]
        else:
            if self.game.board[i][j] > 0 and self.selected != [i, j]:
                self.selected = [i, j]
                return result

            if self.selected != [i, j]:
                result, path = self.game.move_ball(fr=self.selected, to=[i, j])
                if path != None:
                    self.animation = Board.__BallAnimation(
                        self.board_buffer[self.selected[0]][self.selected[1]],
                        path
                    )

            self.selected = None

        return result
  
    class __Cell:
        def __init__(self, row, column):
            self.surface = pygame.Surface([SQUARE_SIZE, SQUARE_SIZE])

            self.row = row
            self.column = column

        def update(self, screen, color, selected, animated):
            self.surface.fill(WHITE)

            # cell is not empty, there is some static ball
            if not animated and color != 0:
                r = RADIUS if color > 0 else SMALL_RADIUS
                pygame.draw.circle(
                    self.surface,
                    colors[abs(color)],
                    (SQUARE_SIZE//2, SQUARE_SIZE//2),
                    r
                )

                if selected:
                    pygame.draw.circle(
                        self.surface,
                        TEXT_COLOR,
                        (SQUARE_SIZE//2, SQUARE_SIZE//2),
                        r,
                        width=5
                    )

            screen.blit(
                self.surface,
                (self.column*SQUARE_SIZE, self.row*SQUARE_SIZE)
            )

    class __BallAnimation:
        def __init__(self, color, path):
            self.path = path
            self.current_x = path[0][1]*SQUARE_SIZE
            self.current_y = path[0][0]*SQUARE_SIZE
            self.moving_towards = 1

            # transparent background
            self.surface = pygame.Surface(
                [SQUARE_SIZE, SQUARE_SIZE],
                pygame.SRCALPHA,
                32
            ).convert_alpha()

            pygame.draw.circle(
                self.surface,
                colors[abs(color)],
                (SQUARE_SIZE//2, SQUARE_SIZE//2),
                RADIUS
            )

        def is_animated(self, pos):
            return True if self.path[0] == pos else False

        def is_finished(self):
            return True if self.moving_towards == len(self.path) else False

        def update(self, screen):
            target_x = self.path[self.moving_towards][1]*SQUARE_SIZE
            target_y = self.path[self.moving_towards][0]*SQUARE_SIZE

            # correct x y
            if self.current_x != target_x:
                if self.current_x < target_x:
                    self.current_x = min(
                        self.current_x + ANIMATION_STEP,
                        target_x
                    )
                else:
                    self.current_x = max(
                        self.current_x - ANIMATION_STEP,
                        target_x
                    )
            if self.current_y != target_y:
                if self.current_y < target_y:
                    self.current_y = min(
                        self.current_y + ANIMATION_STEP,
                        target_y
                    )
                else:
                    self.current_y = max(
                        self.current_y - ANIMATION_STEP,
                        target_y
                    )

            # check if we've reached next turn
            if self.current_x == target_x and self.current_y == target_y:
                self.moving_towards += 1

            screen.blit(
                self.surface,
                (self.current_x, self.current_y)
            )
