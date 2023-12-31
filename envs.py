import gym
from game import UltimateTicTacToe


class TwoPlayerEnv(gym.Env):
    def __init__(self):
        self.pygame = UltimateTicTacToe()
        self.action_space = gym.spaces.Discrete(81)
        self.observation_space = gym.spaces.MultiDiscrete([3]*81)

    def reset(self):
        del self.pygame
        self.pygame = UltimateTicTacToe()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.do_action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def fast_step(self, action):
        self.pygame.do_action(action)
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return reward, done
    
    def ultra_fast_step(self, action): 
        self.pygame.do_action_ultra_fast(action)
        done = self.pygame.is_done()
        return done        

    def render(self, mode="human", close=False):
        self.pygame.view(False)

    def valid_actions(self):
        return self.pygame.board.getListOfPossibleMoves()

    def getState(self):
        b = self.pygame.board
        return (b.grid.copy(), b.largeGrid.copy(), b.possible.copy(), b.currentPlayer, b.state)

    def restoreFromState(self, state):
        b = self.pygame.board
        b.grid = state[0].copy()
        b.largeGrid = state[1].copy()
        b.possible = state[2].copy()
        b.currentPlayer = state[3]
        b.state = state[4]

    def getLastMove(self):
        return self.pygame.move

    def undoMove(self, move):
        if move is None or len(move) == 0: return
        self.pygame.board.possible = move[0]
        self.pygame.board.grid[move[1]] = 0
        if len(move) > 2: self.pygame.board.largeGrid[move[2]] = 0
        self.pygame.board.currentPlayer = 3 - self.pygame.board.currentPlayer
        self.pygame.board.state = 0


class SinglePlayerEnv(TwoPlayerEnv):

    def __init__(self, agent2):
        super().__init__()
        self.agent2 = agent2

    def reset(self):
        self.last_obs = super().reset()
        self.last_done = False
        return self.last_obs

    def step(self, action):
        self.pygame.do_action(action)
        reward = self.pygame.evaluate()
        self.last_done = self.pygame.is_done()

        if self.pygame.error > 0 or self.last_done: 
            self.last_reward = reward
        else: 
            player_opponent = self.pygame.board.currentPlayer
            obs = self.pygame.observe()
            while self.pygame.board.currentPlayer == player_opponent:
                action = self.agent2.getAction(self, obs)

                # if the action is valid we play it in the env
                if action < 81: self.pygame.do_action(action)

            self.last_obs = self.pygame.observe()
            reward2 = self.pygame.evaluate()
            self.last_done = self.pygame.is_done()
            self.last_reward = reward + reward2

        return self.last_obs, self.last_reward, self.last_done, self.pygame.error

