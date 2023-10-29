import pygame


class Agent:
    def __init__(self, player = 1):
        self.player = player

    def getAction(self, env, observation):
        return 0


class RandomAgent(Agent):

    def __init__(self, player = 1):
        super().__init__(self)

    def getAction(self, env, observation):
        action = env.action_space.sample()
        return action


class PlayerAgent(Agent):

    def __init__(self, player = 1):
        super().__init__(player)

    def getAction(self, env, observation):
        while True:
            pygame.time.delay(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    return -1
                if event.type == pygame.MOUSEBUTTONUP: 
                    x, y = pygame.mouse.get_pos()
                    action = env.pygame.board.getActionFromClick(x, y)
                    if action >= 0:
                        return action

            env.pygame.view(True)
