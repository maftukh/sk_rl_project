from agents.agent import Agent
import random
import math

class Node:
    def __init__(self, env, previousPlayer, previousAction=None, parent=None):
        self.previousAction = previousAction 
        self.parent = parent  
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untriedActions = env.valid_actions()  
        self.previousPlayer = previousPlayer 

    def selectChild(self):
        sortedChildren = sorted(self.children, key=lambda node: node.wins / node.visits + math.sqrt(2*math.log(self.visits / node.visits)))
        return sortedChildren[-1]

    def addChild(self, action, env):
        child = Node(env, previousPlayer = 3-self.previousPlayer, previousAction=action, parent=self)
        self.untriedActions.remove(action)
        self.children.append(child)
        return child

def getResult(winner, player):
    if winner == player: 
        return 1
    elif winner == 3 - player: 
        return 0
    else: 
        return 0.5
        
def UCT(rootEnv, previousPlayer, nb_iter):
    rootNode = Node(rootEnv, previousPlayer)
    rootState = rootEnv.getState()

    for i in range(nb_iter):
        node = rootNode
        while node.untriedActions == [] and node.children != []:
            node = node.selectChild()
            rootEnv.ultra_fast_step(node.previousAction) 

        if node.untriedActions != []:
            action = random.choice(node.untriedActions)
            done = rootEnv.ultra_fast_step(action) 
            node = node.addChild(action, rootEnv) 

        while not done:
            actions = rootEnv.valid_actions()
            done = rootEnv.ultra_fast_step(random.choice(actions))
        winner = rootEnv.pygame.board.state
        
        while node is not None:
            node.visits += 1
            node.wins += getResult(winner, node.previousPlayer)
            node = node.parent

        rootEnv.restoreFromState(rootState)

    sortedChildren = sorted(rootNode.children, key = lambda node: node.visits)
    return sortedChildren[-1].previousAction

class MCTSAgent(Agent):

    def __init__(self, player = 1, nb_iter = 1000):
        super().__init__(player)
        self.nb_iter = nb_iter

    def getAction(self, env, observation):
        action = UCT(env, 3 - self.player, self.nb_iter)
        return action
