import gym
import time
import pygame


class Reward:
    def __init__(self, board):
        self.value = 0
        self.reward_factor = 1
        self.mode = 1
        self.board = board
        self.reset()

    def reset(self):
        '''
        Resets the reward to zero
        '''
        self.value = 0

    def update(self, reward):
        '''
        Updates self.reward considering the sign based on the current player
        INPUT: reward of the move
        NO OUTPUT -> updates self.reward
        '''
        if self.board.currentPlayer == 1:
            self.value += reward
        else:
            self.value -= 1 * reward

    def update_playing_on(self, large_index, grid_index):
        '''
        Updates the reward playing in the given cell
        INPUT: large_index, grid_index (indexes of the cell)
        NO OUTPUT -> updates self.reward
        '''
        if self.mode == 2:
            valueLargeGrid_prev = Board.gridValue(self.board.largeGrid)
            self.board.largeGrid[large_index] = self.board.currentPlayer
            valueLargeGrid = Board.gridValue(self.board.largeGrid)
            self.board.largeGrid[large_index] = 0

            valueSmallGrid = Board.gridValue(self.board.grid, large_index*9)
            self.board.grid[grid_index] = 0
            valueSmallGrid_prev = Board.gridValue(self.board.grid, large_index*9)
            self.board.grid[grid_index] = self.board.currentPlayer

            reward = abs((valueSmallGrid - valueSmallGrid_prev) * (valueLargeGrid - valueLargeGrid_prev))
            self.update(reward)

    def update_winning_large_cell(self, large_index):
        '''
        Updates the reward winning a given large cell
        INPUT: large_index (index of the large cell)
        NO OUTPUT -> updates self.reward
        '''
        self.reset()

        if self.mode == 1:
            self.update(10)

        elif self.mode == 2:
            valueLargeGrid = Board.gridValue(self.board.largeGrid)
            self.board.largeGrid[large_index] = 0
            valueLargeGrid_prev = Board.gridValue(self.board.largeGrid)
            self.board.largeGrid[large_index] = self.board.currentPlayer

            reward = abs(20 * (valueLargeGrid - valueLargeGrid_prev))
            self.update(reward)

    def update_winning(self):
        '''
        Updates the reward winning the game
        NO INPUT
        NO OUTPUT -> updates self.reward
        '''
        self.reset()

        if self.mode == 0:
            self.update(1)

        elif self.mode == 1:
            self.update(100)

        elif self.mode == 2:
            self.update(400)


class Board:
    SIZE = 500
    BOTTOM_SIZE = 50

    COLOR_BACKGROUND = (255, 255, 255)
    COLOR_LARGE_GRID = (0, 0, 0)
    COLOR_SMALL_GRID = (184, 187, 194)
    WIDTH_LARGE_GRID = 8
    WIDTH_SMALL_GRID = 4

    COLOR_PLAYER_1 = (255, 51, 51)
    COLOR_PLAYER_2 = (51, 51, 255)
    WIDTH_PLAYER_1 = 5
    WIDTH_PLAYER_2 = 4
    BIG_WIDTH_PLAYER_1 = 10
    BIG_WIDTH_PLAYER_2 = 8
    COLOR_BACKGROUND_PLAYER_1 = (255, 148, 148)
    COLOR_BACKGROUND_PLAYER_2 = (133, 180, 255)

    COLOR_BACKGROUND_AVAILABLE = (235, 235, 235)
    TIME_BLINK_AVAILABLE = 500
    FONT = None

    def __init__(self):
        self.reward = Reward(self)
        Board.FONT = pygame.font.Font(None, 50)
        self.reset()

    def reset(self):
        self.reward.reset()
        self.resetGrid()
        self.currentPlayer = 1
        self.text = "Player 1 plays"
        self.textColor = Board.COLOR_PLAYER_1
        self.state = 0
        self.possible = [i for i in range(9)]

    def resetGrid(self):
        self.grid = [0] * 81
        self.largeGrid = [0] * 9

    def play(self, ixLarge, iyLarge, ixSmall, iySmall):
        large_index = Board.getLargeIndex(ixLarge, iyLarge)
        grid_index = Board.getIndex(ixLarge, iyLarge, ixSmall, iySmall)
        if self.state != 0:
            return 1, None
        if not(large_index in self.possible):
            return 2, None
        elif self.grid[grid_index] != 0:
            return 3, None

        self.reward.reset()

        self.grid[grid_index] = self.currentPlayer
        move = [self.possible.copy(), grid_index]
        self.reward.update_playing_on(large_index, grid_index)

        self.checkWinLargeCell(large_index, move)

        self.updatePossible(ixSmall, iySmall)

        self.currentPlayer = 3 - self.currentPlayer

        if self.state == 0:
            self.text = "Player " + str(self.currentPlayer) + " plays"
            self.textColor = Board.COLOR_PLAYER_2 if self.currentPlayer == 1 else Board.COLOR_PLAYER_1

        return 0, move

    def play_ultra_fast(self, ixLarge, iyLarge, ixSmall, iySmall):
        large_index = Board.getLargeIndex(ixLarge, iyLarge)
        grid_index = Board.getIndex(ixLarge,iyLarge,ixSmall,iySmall)
        if self.state != 0:
            return 1, None
        
        if not(large_index in self.possible):
            return 2, None
        
        elif self.grid[grid_index] != 0:
            return 3, None

        self.reward.reset()
        self.grid[grid_index] = self.currentPlayer
        self.checkWinLargeCell(large_index, None, True)
        self.updatePossible(ixSmall, iySmall)
        self.currentPlayer = 3 - self.currentPlayer

        return 0

    def checkWinLargeCell(self, large_index, move, fast = False):
        '''
        Checks if a player won the large cell queried. If so, it also checks if the player globally won the game
        Input: ix, iy (indexes of the large cell)
        NO OUTPUT -> Automatically updates self.largeGrid and self.state'''
        res = Board.checkWinBoard(self.grid, 9*large_index)
        if res != 0:
            # Win lage cell
            self.largeGrid[large_index] = res
            
            if not(fast):
                self.reward.update_winning_large_cell(large_index)
                move.append(large_index)

            # Check if the game was won
            resWin = Board.checkWinBoard(self.largeGrid)
            if resWin != 0: # A player won
                self.state = resWin

                if not(fast):
                    self.reward.update_winning()

                    # Display winning message
                    self.textColor = Board.COLOR_PLAYER_2
                    if resWin == 1:
                        self.textColor = Board.COLOR_PLAYER_1
                    self.text = "Player " + str(self.state) + " won !"



    def checkWinLargeCell(self, large_index, move, fast=False):
        res = Board.checkWinBoard(self.grid, 9 * large_index)
        if res != 0:
            self.largeGrid[large_index] = res

            if not fast:
                self.reward.update_winning_large_cell(large_index)
                move.append(large_index)

            resWin = Board.checkWinBoard(self.largeGrid)
            if resWin != 0:
                self.state = resWin

                if not fast:
                    self.reward.update_winning()
                    self.textColor = Board.COLOR_PLAYER_2 if resWin == 1 else Board.COLOR_PLAYER_1
                    self.text = "Player " + str(self.state) + " won !"

    def updatePossible(self, ix, iy):
        large_index = Board.getLargeIndex(ix, iy)
        if self.largeGrid[large_index] != 0:
            self.getAvailableLargeCells()
        elif Board.gridIsFull(self.grid, 9 * large_index):
            self.getAvailableLargeCells()
        else:
            self.possible = [large_index]

    def getAvailableLargeCells(self):
        self.possible = []
        for large_index in range(9):
            if self.largeGrid[large_index] != 0:
                pass
            else:
                i = 0
                continuer = True
                while continuer and (i < 9):
                    if self.grid[9 * large_index + i] == 0:
                        continer = False
                        self.possible.append(large_index)
                    i += 1

        if self.state == 0 and len(self.possible) == 0:
            self.state = 3

    def draw(self, screen, blinkAvailableCells=True):
        pygame.display.set_caption("Ultimate Tic-Tac-Toe")

        s = Board.getSizeLargeCell()
        for ix in range(3):
            for iy in range(3):
                large_index = Board.getLargeIndex(ix, iy)
                gridValue = self.largeGrid[large_index]
                pos = Board.getLargeTopLeftPx(ix, iy)
                color = Board.COLOR_BACKGROUND
                if gridValue == 1:
                    color = Board.COLOR_BACKGROUND_PLAYER_1
                elif gridValue == 2:
                    color = Board.COLOR_BACKGROUND_PLAYER_2
                elif blinkAvailableCells and (self.state == 0):
                    if large_index in self.possible:
                        if round(time.time() * 1000) % Board.TIME_BLINK_AVAILABLE > 0.5 * Board.TIME_BLINK_AVAILABLE:
                            color = Board.COLOR_BACKGROUND_AVAILABLE
                pygame.draw.rect(screen, color, (pos[0], pos[1], s, s))

        for i in range(10):
            pos = 0.5 * Board.WIDTH_LARGE_GRID + (Board.SIZE - Board.WIDTH_LARGE_GRID) * i / 9. - 1
            pygame.draw.line(screen, Board.COLOR_SMALL_GRID, (pos, 0), (pos, Board.SIZE), width=Board.WIDTH_SMALL_GRID)
            pygame.draw.line(screen, Board.COLOR_SMALL_GRID, (0, pos), (Board.SIZE, pos), width=Board.WIDTH_SMALL_GRID)

        for i in range(4):
            pos = Board.getLargeTopLeftPx(i, 0)[0]
            pygame.draw.line(screen, Board.COLOR_LARGE_GRID, (pos, 0), (pos, Board.SIZE), width=Board.WIDTH_LARGE_GRID)
            pygame.draw.line(screen, Board.COLOR_LARGE_GRID, (0, pos), (Board.SIZE, pos), width=Board.WIDTH_LARGE_GRID)

        inc = 0.3 * Board.getSizeSmallCell()
        for ixLarge in range(3):
            for iyLarge in range(3):
                for ixSmall in range(3):
                    for iySmall in range(3):
                        grid_index = Board.getIndex(ixLarge, iyLarge, ixSmall, iySmall)
                        gridValue = self.grid[grid_index]
                        pos = Board.getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall)
                        if gridValue == 1:
                            pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] - inc, pos[1] - inc), (pos[0] + inc, pos[1] + inc), width=Board.WIDTH_PLAYER_1)
                            pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] - inc, pos[1] + inc), (pos[0] + inc, pos[1] - inc), width=Board.WIDTH_PLAYER_1)
                        elif gridValue == 2:
                            pygame.draw.circle(screen, Board.COLOR_PLAYER_2, pos, 1.2 * inc, width=Board.WIDTH_PLAYER_2)

        s = Board.getSizeLargeCell()
        inc = 0.05 * Board.getSizeLargeCell()
        for ix in range(3):
            for iy in range(3):
                large_index = Board.getLargeIndex(ix, iy)
                gridValue = self.largeGrid[large_index]
                pos = Board.getLargeTopLeftPx(ix, iy)
                color = Board.COLOR_BACKGROUND
                if gridValue == 1:
                    pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] + inc, pos[1] + inc), (pos[0] + s - inc, pos[1] + s - inc), width=Board.BIG_WIDTH_PLAYER_1)
                    pygame.draw.line(screen, Board.COLOR_PLAYER_1, (pos[0] + inc, pos[1] + s - inc), (pos[0] + s - inc, pos[1] + inc), width=Board.BIG_WIDTH_PLAYER_1)
                elif gridValue == 2:
                    pygame.draw.circle(screen, Board.COLOR_PLAYER_2, (pos[0] + int(s / 2), pos[1] + int(s / 2)), (s / 2 - inc), width=Board.BIG_WIDTH_PLAYER_2)

        pygame.draw.rect(screen, Board.COLOR_BACKGROUND, (0, Board.SIZE, Board.SIZE, Board.BOTTOM_SIZE))
        text = Board.FONT.render(self.text, True, self.textColor)
        text_rect = text.get_rect(center=(Board.SIZE / 2., Board.SIZE + Board.BOTTOM_SIZE / 2.))
        screen.blit(text, text_rect)

    def getActionFromClick(self, px, py):
        (ixLarge, iyLarge, ixSmall, iySmall) = Board.getCellFromPx(px, py)
        if (ixLarge >= 3) or (iyLarge >= 3) or (ixSmall >= 3) or (iySmall >= 3):
            return -1
        return Board.getIndex(ixLarge, iyLarge, ixSmall, iySmall)

    def click(self, px, py):
        (ixLarge, iyLarge, ixSmall, iySmall) = Board.getCellFromPx(px, py)
        if (ixLarge >= 3) or (iyLarge >= 3) or (ixSmall >= 3) or (iySmall >= 3):
            return 4, None
        return self.play(ixLarge, iyLarge, ixSmall, iySmall)

    def getListOfPossibleMoves(self):
        moves = []
        for large_index in self.possible:
            for i in range(9):
                grid_index = 9 * large_index + i
                if self.grid[grid_index] == 0:
                    moves.append(grid_index)
        return moves

    @staticmethod
    def checkWinBoard(grid, start=0):
        for i in range(3):
            if grid[start + 3 * i + 0] == grid[start + 3 * i + 1] == grid[start + 3 * i + 2] != 0:
                return grid[start + 3 * i + 0]
            if grid[start + 3 * 0 + i] == grid[start + 3 * 1 + i] == grid[start + 3 * 2 + i] != 0:
                return grid[start + 3 * 0 + i]

        if grid[start] == grid[start + 4] == grid[start + 8] != 0:
            return grid[start]
        if grid[start + 2] == grid[start + 4] == grid[start + 6] != 0:
            return grid[start + 2]

        return 0

    @staticmethod
    def gridIsFull(grid, start=0):
        for i in range(9):
            if grid[start + i] == 0:
                return False
        return True

    @staticmethod
    def getCellFromPx(px, py):
        start = Board.getLargeTopLeftPx(0, 0)
        ixLarge = int((px - start[0]) // Board.getSizeLargeCell())
        iyLarge = int((py - start[1]) // Board.getSizeLargeCell())
        px2 = px - start[0] - ixLarge * Board.getSizeLargeCell()
        py2 = py - start[1] - iyLarge * Board.getSizeLargeCell()
        ixSmall = int(px2 // Board.getSizeSmallCell())
        iySmall = int(py2 // Board.getSizeSmallCell())
        return (ixLarge, iyLarge, ixSmall, iySmall)

    @staticmethod
    def getSizeLargeCell():
        return (Board.SIZE - Board.WIDTH_LARGE_GRID) / 3.

    @staticmethod
    def getSizeSmallCell():
        return (Board.SIZE - Board.WIDTH_LARGE_GRID) / 9.

    @staticmethod
    def getLargeTopLeftPx(ix, iy):
        px = 0.5 * Board.WIDTH_LARGE_GRID + ix * Board.getSizeLargeCell() - 1
        py = 0.5 * Board.WIDTH_LARGE_GRID + iy * Board.getSizeLargeCell() - 1
        return (px, py)

    @staticmethod
    def getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall):
        (pxLarge, pyLarge) = Board.getLargeTopLeftPx(ixLarge, iyLarge)
        px = pxLarge + ixSmall * Board.getSizeSmallCell()
        py = pyLarge + iySmall * Board.getSizeSmallCell()
        return (px, py)

    @staticmethod
    def getSmallMidddlePx(ixLarge, iyLarge, ixSmall, iySmall):
        (px, py) = Board.getSmallTopLeftPx(ixLarge, iyLarge, ixSmall, iySmall)
        px += 0.5 * Board.getSizeSmallCell()
        py += 0.5 * Board.getSizeSmallCell()
        return (px, py)

    @staticmethod
    def getLargeIndex(ix, iy):
        return 3 * ix + iy

    @staticmethod
    def getIndex(ixLarge, iyLarge, ixSmall, iySmall):
        return 27 * ixLarge + 9 * iyLarge + 3 * ixSmall + iySmall

    @staticmethod
    def gridValue(grid, start=0):
        value = 0

        if True:
            lines1, lines2, used = set(), set(), set()

            # Lignes horizontales
            for i in range(3):
                nb1, nb2 = 0, 0
                zero, addToUsed = None, False
                for j in range(3):
                    index = start +3*i +j
                    if grid[index] == 1: nb1 += 1
                    elif grid[index] == 2: nb2 += 1
                    else: zero = index
                if nb1 == 2 and nb2 == 0:
                    lines1.add(zero)
                    addToUsed = True
                elif nb2 == 2 and nb1 == 0:
                    lines2.add(zero)
                    addToUsed = True
                if addToUsed:
                    for j in range(3):
                        used.add(start +3*i +j)

            # Lignes verticales
            for j in range(3):
                nb1 = 0
                nb2 = 0
                zero = None
                addToUsed = False
                for i in range(3):
                    index = start +3*i +j
                    if grid[index] == 1: nb1 += 1
                    elif grid[index] == 2: nb2 += 1
                    else: zero = index
                if nb1 == 2 and nb2 == 0:
                    lines1.add(zero)
                    addToUsed = True
                elif nb2 == 2 and nb1 == 0:
                    lines2.add(zero)
                    addToUsed = True
                if addToUsed:
                    for i in range(3):
                        used.add(start +3*i +j)

            # Diagonale 1
            nb1 = 0
            nb2 = 0
            zero = None
            addToUsed = False
            for i in range(3):
                index = start +3*i +i
                if grid[index] == 1: nb1 += 1
                elif grid[index] == 2: nb2 += 1
                else: zero = index
            if nb1 == 2 and nb2 == 0:
                lines1.add(zero)
                addToUsed = True
            elif nb2 == 2 and nb1 == 0:
                lines2.add(zero)
                addToUsed = True
            if addToUsed:
                for i in range(3):
                    used.add(start +3*i +i)

            # Diagonale 2
            nb1 = 0
            nb2 = 0
            zero = None
            addToUsed = False
            for i in range(3):
                index = start +3*(2-i) +i
                if grid[index] == 1: nb1 += 1
                elif grid[index] == 2: nb2 += 1
                else: zero = index
            if nb1 == 2 and nb2 == 0:
                lines1.add(zero)
                addToUsed = True
            elif nb2 == 2 and nb1 == 0:
                lines2.add(zero)
                addToUsed = True
            if addToUsed:
                for i in range(3):
                    used.add(start +3*(2-i) +i)

            value += 5 * min(2, len(lines1))
            value -= 5 * min(2, len(lines2))

            for i in range(3):
                for j in range(3):
                    index = start + 3*i + j
                    if grid[index] != 0 and not(index in used):
                        val = 1 # edge
                        if i == j == 1: # Middle
                            val = 2
                        elif (i != 1) and (j != 1): # Corner
                            val = 1.5
                        value += val * (3-2*grid[index])

            return value



class UltimateTicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Board.SIZE, Board.SIZE + Board.BOTTOM_SIZE))
        self.board = Board()
        self.error = 0
        self.move = None
        self.action_space = gym.spaces.Discrete(81)
        self.observation_space = gym.spaces.MultiDiscrete([3]*81 + [3]*9 + [2]*9)
        self.plays = 0

    def observe(self):
        return (self.board.grid, self.board.largeGrid, self.board.possible)

    def is_done(self):
        return (self.board.state != 0)

    def do_action(self, action):
        ixLarge, iyLarge, ixSmall, iySmall = self._decode_action(action)
        self.error, self.move = self.board.play(ixLarge, iyLarge, ixSmall, iySmall)

    def do_action_ultra_fast(self, action):
        ixLarge, iyLarge, ixSmall, iySmall = self._decode_action(action)
        self.error = self.board.play_ultra_fast(ixLarge, iyLarge, ixSmall, iySmall)

    def evaluate(self):
        if self.error > 0:
            return -100
        return self.board.reward.value

    def view(self, blink):
        self.board.draw(self.screen, blink)
        pygame.display.flip()

    def _decode_action(self, action):
        iySmall = action % 3
        action = int((action - iySmall) // 3)
        ixSmall = action % 3
        action = int((action - ixSmall) // 3)
        iyLarge = action % 3
        action = int((action - iyLarge) // 3)
        ixLarge = action % 3
        return ixLarge, iyLarge, ixSmall, iySmall
