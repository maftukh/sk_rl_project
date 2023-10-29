from envs import TwoPlayerEnv, SinglePlayerEnv
import pygame

from agents.agent import PlayerAgent
from agents.agent import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_minimax import MinimaxPruningAgent
from agents.agent_dqn import DQNAgent

agent2 = RandomAgent(2)
env = SinglePlayerEnv(agent2)

agent = DQNAgent(1, env, True)
agent.learnNN(env, False, 1000, 1500, "_test")
display = True


if __name__ == '__main__':
    obs = env.reset()

    done = False
    game = True
    while game:
        if not(done):
            action = agent.getAction(env, obs)
            if action < 0:
                done = True
            elif action < 81:
                obs, reward, done, info = env.step(action)

        if display:
            env.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False
            pygame.time.delay(1)

    pygame.quit()
    print("ENV state:", env.pygame.board.state)
    env.close()
