from gameparameters import *
import random
import numpy as np

class GameManager:
    SUCCESS = 100
    INVALID_PATH = 101
    GAME_OVER = 102
    SAME_POS = 104
    NO_BALL = 105

    def __init__(self):
        # initialize game board
        self.board = [[0 for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
        self.__fill_board()
        
        self.score = 0 

    def __randomize_ball(self, place_ball = True):
        def randomize_position():
            return random.randrange(FIELD_SIZE), random.randrange(FIELD_SIZE)
        
        color = random.randrange(1,COLORS+1)
        row, column = randomize_position()
        
        # if a position isn't free, randomize until a free position is found
        while self.board[row][column] != 0:
            row, column = randomize_position()

        self.board[row][column] =  color if place_ball else -color

    def __fill_board(self):
        for i in range(BALLS_ON_START):
            self.__randomize_ball()
        for i in range(BALLS_PER_MOVE):
            self.__randomize_ball(False)

    def move_ball(self, fr, to):
        if fr == to:
            return GameManager.SAME_POS

        if self.board[fr[0]][fr[1]] == 0:
            return GameManager.NO_BALL

        path = self.__check_path(fr, to)
        if path == None :
            return GameManager.INVALID_PATH, None

        self.board[to[0]][to[1]] = self.board[fr[0]][fr[1]]
        self.board[fr[0]][fr[1]] = 0
        
        free = self.__update_board()

        if free == 0:
            return GameManager.GAME_OVER, path

        return GameManager.SUCCESS, path

    def __check_path(self, fr, to):
        steps = [[9999 for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
        steps[fr[0]][fr[1]] = 0
        
        stack = [fr]

        while len(stack) != 0:
            row = stack[0][0]
            column = stack[0][1]
            
            # checks if neighboring cells are empty
            def check(modifier_1,modifier_2):
                if 0 <= modifier_1(row) and modifier_1(row) < FIELD_SIZE \
                and 0 <= modifier_2(column) and modifier_2(column) < FIELD_SIZE \
                and self.board[modifier_1(row)][modifier_2(column)] <= 0:
                    
                    if steps[row][column] + 1 < steps[modifier_1(row)][modifier_2(column)]:
                        steps[modifier_1(row)][modifier_2(column)] = steps[row][column] + 1
                        stack.append([modifier_1(row), modifier_2(column)])
                        if [modifier_1(row), modifier_2(column)] == to:
                            return True

            # top
            if check(lambda x: x+1, lambda x: x):
                break
           
            # right
            if check(lambda x: x, lambda x: x+1):
                break
            
             # bottom
            if check(lambda x: x-1, lambda x: x):
                break

            # left
            if check(lambda x: x, lambda x: x-1):
                break

            stack.pop(0)
            
        # retract path
        if len(stack) != 0:
            current = to
            path = [to]

            while current != fr:
                neighbors = []

                # top
                if current[0] > 0:
                    neighbors.append([current[0]-1,current[1]])
                
                # right
                if current[1] < FIELD_SIZE-1:
                    neighbors.append([current[0], current[1]+1])
                
                # bottom
                if current[0] < FIELD_SIZE-1:
                    neighbors.append([current[0]+1, current[1]])
                
                # left
                if current[1] > 0:
                    neighbors.append([current[0], current[1]-1])

                def pick_min(neighbors):
                    list = []
                    for pos in neighbors:
                        list.append(steps[pos[0]][pos[1]])
                    min_index = np.argmin(list)
                    return neighbors[min_index]

                current = pick_min(neighbors)
                path.insert(0,current)
          
            return path


        return None

    def __update_board(self):
        def delete_clusters():
            deletion_matrix = [[False for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]

            def mark_in_deletion_matrix(last_pos, sequence, modifier_1, modifier_2):
                row = last_pos[0]
                column = last_pos[1]
                for i in range(sequence,0,-1):
                    deletion_matrix[row][column] = True
                    row = modifier_1(row)
                    column = modifier_2(column)

            class Parameters:
                def __init__(self):
                    self.color = 0
                    self.sequence = 0

            def update_sequence(parameters, modifier_1, modifier_2, check_last):
                end_of_line = check_last(i,j)
                color_changed = False

                def same_color():
                    return parameters.color > 0 and parameters.color == abs(self.board[i][j])

                if same_color():
                    parameters.sequence += 1
                else:
                    color_changed = True
                
                if end_of_line:
                    if parameters.sequence >= SHRINK:
                        if not color_changed:
                            last_pos = [i, j]
                        else:
                            last_pos = [modifier_1(i), modifier_2(j)]
                        mark_in_deletion_matrix(
                            last_pos,
                            parameters.sequence,
                            modifier_1,
                            modifier_2
                        )
                else:
                    if color_changed and parameters.sequence >= SHRINK:
                        last_pos = [modifier_1(i), modifier_2(j)]
                        mark_in_deletion_matrix(
                            last_pos,
                            parameters.sequence,
                            modifier_1,
                            modifier_2
                        )

                if color_changed:
                    parameters.color = abs(self.board[i][j])
                    parameters.sequence = 1 if parameters.color != 0 else 0
                    

            # rows
            for i in range(FIELD_SIZE):
                param = Parameters()
                for j in range(FIELD_SIZE):
                    update_sequence(
                        parameters = param, 
                        modifier_1 = lambda x: x, 
                        modifier_2 = lambda x: x-1,
                        check_last = lambda x, y: y == FIELD_SIZE-1 
                    )

            # columns
            for j in range(FIELD_SIZE):
                param = Parameters()
                for i in range(FIELD_SIZE):
                    update_sequence(
                        parameters = param,
                        modifier_1 = lambda x: x-1,
                        modifier_2 = lambda x: x,
                        check_last = lambda x, y: x == FIELD_SIZE-1
                    )

            # main diagonal, lower half
            for r in range(FIELD_SIZE - SHRINK + 1):
                param = Parameters()
                i = r
                j = 0
                while i < FIELD_SIZE:
                    update_sequence(
                        parameters = param,
                        modifier_1 = lambda x: x-1,
                        modifier_2 = lambda x: x-1,
                        check_last = lambda x, y: x == FIELD_SIZE-1
                    )
                    i += 1
                    j += 1

            # main diagonal, upper half
            for r in range(FIELD_SIZE - SHRINK + 1):
                param = Parameters()
                i = 0
                j = r
                while j < FIELD_SIZE:
                    update_sequence(
                        parameters = param, 
                        modifier_1 = lambda x: x-1, 
                        modifier_2 = lambda x: x-1,
                        check_last = lambda x, y: y == FIELD_SIZE-1 
                    )
                    i += 1
                    j += 1

            # secondary diagonal, lower half
            for r in range(FIELD_SIZE - SHRINK + 1):
                param = Parameters()
                i = r
                j = FIELD_SIZE - 1
                while i < FIELD_SIZE:
                    update_sequence(
                        parameters = param,
                        modifier_1 = lambda x: x-1,
                        modifier_2 = lambda x: x+1,
                        check_last = lambda x,y: x == FIELD_SIZE-1
                    )
                    i += 1
                    j -= 1

            # secondary diagonal, upper half
            for r in range(FIELD_SIZE - SHRINK + 1):
                param = Parameters()
                i = 0
                j = FIELD_SIZE - 1 - r
                while j >= 0:
                    update_sequence(
                        parameters = param, 
                        modifier_1 = lambda x: x-1, 
                        modifier_2 = lambda x: x+1,
                        check_last = lambda x, y: y == 0
                    )
                    i += 1
                    j -= 1
            
            deleted = 0
            free = 0
            for i in range(FIELD_SIZE):
                for j in range(FIELD_SIZE):
                    if deletion_matrix[i][j]:
                        self.board[i][j] = 0
                        deleted += 1
                    if self.board[i][j] < 0:
                        self.board[i][j] = abs(self.board[i][j])
                    elif self.board[i][j] == 0:
                        free += 1

            self.score += deleted
            return free

        free = delete_clusters()

        if free > 1:
            for i in range(min(BALLS_PER_MOVE, free)):
                self.__randomize_ball(False)
        elif free == 1:
            while free == 1:
                self.__randomize_ball()
                free = delete_clusters()
        
        return free
