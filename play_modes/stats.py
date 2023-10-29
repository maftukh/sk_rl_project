from envs import SinglePlayerEnv
import pygame
import tqdm

from agents.agent import PlayerAgent
from agents.agent import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_minimax import MinimaxPruningAgent
from agents.agent_minimax import MinimaxPruningAgentSeveralRewards
from agents.agent_mcts import MCTSAgent
from agents.agent_dqn import DQNAgent
from agents.agent_dqn import DoubleDQNAgent

env = SinglePlayerEnv(RandomAgent(2))

agents1 = [
    RandomAgent(1),
    MinimaxPruningAgent(1,1,True),
    MinimaxPruningAgent(1,3,True),
    MinimaxPruningAgent(1,5,True),
    MCTSAgent(1, 100),
    MCTSAgent(1, 500),
    MCTSAgent(1, 1000),
    MCTSAgent(1, 2000),
    DQNAgent(1, env, False),
    DoubleDQNAgent(1, env, False)
]

agents2 = [
    MinimaxPruningAgent(2,3,True),
    MinimaxPruningAgent(2,5,True),
    MCTSAgent(2, 100),
    MCTSAgent(2, 500),
    MCTSAgent(2, 1000),
    MCTSAgent(2, 2000),
    DQNAgent(2, env, False),
    DoubleDQNAgent(2, env, False)
]

display = False

if __name__ == '__main__':
    N = 20
    n = len(agents1)
    n2 = len(agents2)
    wins = [[0 for i in range(n2)] for j in range(n)]
    equalities = [[0 for i in range(n2)] for j in range(n)]
    losses = [[0 for i in range(n2)] for j in range(n)]

    for it in tqdm.tqdm(range(N)):
        for i1 in range(n):
            for i2 in range(n2):
                #print(i1,i2)
                agent = agents1[i1]
                agent2 = agents2[i2]
                
                env.agent2 = agent2
                obs = env.reset()

                done = False
                game = True
                while not(done):

                    if not(done):
                        action = agent.getAction(env, obs)

                        if action < 0:
                            done = True
                        elif action < 81:
                            obs, reward, done, info = env.step(action)
                        if display:
                            env.render()

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT: 
                                    game = False
                            pygame.time.delay(1)

                if env.pygame.board.state == 1:
                    wins[i1][i2] += 1
                elif env.pygame.board.state == 2:
                    losses[i1][i2] += 1
                elif env.pygame.board.state == 3:
                    equalities[i1][i2] += 1


    print("WINS=")
    print(wins)
    print("\nLOSSES=")
    print(losses)
    print("\nEQUALITIES=")
    print(equalities)

    pygame.quit()
    env.close()
