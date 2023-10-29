from agents.agent import Agent
import random
INFINITY = 1000


def minimax(env, stepMax, cumulated_reward = 0, step = 0, maximize = True):
    actions = env.valid_actions()

    chosenMove = None
    chosenReward = 0
    for action in actions:

        reward, done = env.fast_step(action)
        move = env.getLastMove()
        r = cumulated_reward + reward

        if not(done) and step + 1 < stepMax:
            _, r = minimax(env, stepMax, cumulated_reward + reward, step + 1, not(maximize))
        
        if (chosenMove is None) or (maximize and (r > chosenReward)) or (not(maximize) and (r < chosenReward)):
            chosenReward = r
            chosenMove = action

        env.undoMove(move)

    return chosenMove, chosenReward


class MinimaxAgent(Agent):

    def __init__(self, player = 1, stepMax = 4):
        super().__init__(player)
        self.stepMax = stepMax

    def getAction(self, env, observation):
        action, expected_reward = minimax(env, self.stepMax, maximize=(self.player == 1))
        return action


def minimaxPruning(env, depth, alpha = - INFINITY, beta = INFINITY, cumulated_reward = 0, done = False, maximize = True, rand = True, rewardMode = None):
    if(rewardMode != None):
        env.pygame.board.reward.mode = rewardMode

    if (depth == 0) or done:
        return None, cumulated_reward

    actions = env.valid_actions()
    newDepth = depth - 1
    if len(actions) > 9: newDepth = max(0, depth - 2)

    if maximize:
        maxEval = - INFINITY
        maxAction = None
        for action in actions:
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, False, rand = False)
            if eval > maxEval:
                maxEval = eval
                if rand: maxAction = [action]
                else: maxAction = action
            elif rand and eval == maxEval:
                maxAction.append(action)
            env.undoMove(move)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        if rand: return random.choice(maxAction), maxEval
        else: return maxAction, maxEval

    else:
        minEval = + INFINITY
        minAction = None
        for action in actions:
            reward, done = env.fast_step(action)
            move = env.getLastMove()
            _, eval = minimaxPruning(env, newDepth, alpha, beta, cumulated_reward + reward, done, True, rand = False)
            if eval < minEval:
                minEval = eval
                if rand: minAction = [action]
                else: minAction = action
            elif rand and eval == minEval:
                minAction.append(action)
            env.undoMove(move)
            beta = min(beta, eval)
            if beta <= alpha: break
        if rand: return random.choice(minAction), minEval
        else: return minAction, minEval


class MinimaxPruningAgent(Agent):

    def __init__(self, player = 1, stepMax = 4, rand = True, rewardMode = 2):
        super().__init__(player)
        self.stepMax = stepMax
        self.rand = rand
        self.rewardMode = rewardMode
        self.expected_reward = 0

    def getAction(self, env, observation, rewardMode = None, nbSteps = None):
        if rewardMode is None:
            rewardMode = self.rewardMode

        if nbSteps is None:
            nbSteps = self.stepMax

        action, expected_reward = minimaxPruning(env, nbSteps, maximize=(self.player == 1), rand=self.rand, rewardMode=rewardMode)
        self.expected_reward = expected_reward
        return action


class MinimaxPruningAgentSeveralRewards(MinimaxPruningAgent):
    def __init__(self, player = 1, stepMax = 4, rand = True, additionalSteps = 2, startMultipleAtXSteps = 20):
        super().__init__(player, stepMax, rand)
        self.additionalSteps = additionalSteps
        self.startMultipleAtXSteps = startMultipleAtXSteps

    def getAction(self, env, observation):
        env.pygame.plays += 1
        if env.pygame.plays >= self.startMultipleAtXSteps:
            action = super().getAction(env, observation, nbSteps=self.stepMax + self.additionalSteps, rewardMode=1)
            if self.expected_reward*(3-2*self.player) > 50: 
                print("ACTION CHOSEN BY SIMPLE: ", self.expected_reward)
            else: 
                action = super().getAction(env, observation, nbSteps=self.stepMax, rewardMode=2)
            return action
        else:
            return super().getAction(env, observation, nbSteps=self.stepMax, rewardMode=2)    
