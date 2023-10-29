from envs import TwoPlayerEnv
import pygame


if __name__ == '__main__':
    env = TwoPlayerEnv()
    obs = env.reset()

    game = True
    while game:
        pygame.time.delay(1)

        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        if done == True:
            game = False
        env.render()
        
    pygame.quit()
    env.close()
