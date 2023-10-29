from envs import SinglePlayerEnv
import pygame

from agents.agent import PlayerAgent
from agents.agent import RandomAgent
from agents.agent_minimax import MinimaxPruningAgent
from agents.agent_minimax import MinimaxPruningAgentSeveralRewards
from agents.agent_mcts import MCTSAgent
from agents.agent_dqn import DQNAgent


# Choose your agent here :
agent = MinimaxPruningAgentSeveralRewards(1, 5, True, 3, 15)



display = True
if __name__ == '__main__':
    agent2 =  PlayerAgent(2)
    env = SinglePlayerEnv(agent2)
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
