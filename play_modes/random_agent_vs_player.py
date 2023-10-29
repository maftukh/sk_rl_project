from envs import TwoPlayerEnv
import pygame


if __name__ == '__main__':
    env = TwoPlayerEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        if env.pygame.board.currentPlayer == 1: # Player
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False
                if event.type == pygame.MOUSEBUTTONUP: # Mouse click released
                    x, y = pygame.mouse.get_pos()
                    env.pygame.board.click(x, y)
            env.pygame.view(True)

        else: 
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            if done == True:
                game = False
            env.render()

    pygame.quit()
    env.close()
