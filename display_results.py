from envs.env_single_player import SinglePlayerEnv
import pygame

from agents.agent_player import PlayerAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_minimax_pruning import MinimaxPruningAgent
from agents.agent_mcts import MCTSAgent

#agent = MinimaxPruningAgent(1, 5, True)
agent = MCTSAgent(1, 2000)
#agent = MinimaxPruningAgent(1)
display = True


# Please copy-paste the following res from the stats.py output
WINS = [[36, 45, 48, 8, 0, 0, 0, 0, 0, 0], 
[0, 100, 5, 2, 1, 0, 1, 0, 0, 0], 
[0, 0, 100, 1, 0, 0, 2, 0, 0, 0], 
[0, 0, 0, 36, 4, 4, 60, 29, 11, 8], 
[0, 0, 0, 0, 51, 41, 91, 71, 57, 38], 
[0, 0, 0, 0, 0, 45, 97, 72, 61, 54], 
[0, 0, 0, 0, 0, 0, 38, 4, 1, 2], 
[0, 0, 0, 0, 0, 0, 0, 52, 18, 16], 
[0, 0, 0, 0, 0, 0, 0, 0, 47, 46], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 51]]
LOSSES = [[32, 41, 38, 92, 100, 99, 98, 100, 100, 100], 
[0, 0, 95, 95, 98, 99, 95, 100, 100, 100], 
[0, 0, 0, 95, 99, 100, 94, 100, 100, 100], 
[0, 0, 0, 60, 87, 91, 30, 66, 85, 92], 
[0, 0, 0, 0, 39, 43, 5, 18, 25, 48], 
[0, 0, 0, 0, 0, 33, 2, 19, 31, 35], 
[0, 0, 0, 0, 0, 0, 49, 91, 94, 98], 
[0, 0, 0, 0, 0, 0, 0, 39, 72, 77], 
[0, 0, 0, 0, 0, 0, 0, 0, 38, 42], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 39]]
EQUALITIES = [
 [32, 14, 14, 0, 0, 1, 2, 0, 0, 0],
 [0, 0, 0, 4, 1, 0, 4, 0, 0, 0],
 [0, 0, 0, 4, 1, 0, 4, 0, 0, 0],
 [0, 0, 4, 9, 5, 10, 5, 4, 0, 0],
 [0, 0, 0, 0, 22, 1, 9, 8, 11, 0],
 [0, 0, 0, 0, 0, 13, 5, 5, 0, 0],
 [0, 0, 0, 0, 0, 0, 9, 10, 7, 0],
 [0, 0, 0, 0, 0, 0, 0, 15, 12, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
NAMES = ["Random Agent",  "DQN Agent", "Double DQN Agent", "1-step Minimax Agent (random)", "3-step Minimax Agent (random)", "5-step Minimax Agent (random)", "MCTS Agent (N=100)", "MCTS Agent (N=500)", "MCTS Agent (N=1000)", "MCTS Agent (N=2000)"]
n = len(WINS)
N = 100

CELL_SIZE = 80
LINE_SIZE = 7
PADDING = 60
LEGEND_SIZE = 700
SIZE = PADDING + n*(CELL_SIZE + LINE_SIZE) + LINE_SIZE
pygame.init()
screen = pygame.display.set_mode((SIZE+LEGEND_SIZE, SIZE))

# Change color scheme
win_color = (0, 128, 255)  # Blue for wins
draw_color = (128, 128, 128)  # Gray for draws
loss_color = (255, 165, 0)  # Orange for losses

# Draw grid and rectangles
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 50)

# Draw grid lines
for i in range(n + 1):
    pos = PADDING + int(LINE_SIZE * 0.5) + i * (CELL_SIZE + LINE_SIZE)
    pygame.draw.line(screen, (0, 0, 0), (pos, PADDING), (pos, PADDING + n * (CELL_SIZE + LINE_SIZE) + LINE_SIZE),
                     width=LINE_SIZE)  # Vertical
    pygame.draw.line(screen, (0, 0, 0), (PADDING, pos), (PADDING + n * (CELL_SIZE + LINE_SIZE), pos),
                     width=LINE_SIZE)  # Horizontal

# Draw rectangles and text
for i in range(n):
    for j in range(n):
        w = int(round(WINS[i][j] * CELL_SIZE / float(N)))
        l = int(round(LOSSES[i][j] * CELL_SIZE / float(N)))
        e = int(round(EQUALITIES[i][j] * CELL_SIZE / float(N)))

        if j < i:
            w = int(round(LOSSES[j][i] * CELL_SIZE / float(N)))
            l = int(round(WINS[j][i] * CELL_SIZE / float(N)))
            e = int(round(EQUALITIES[j][i] * CELL_SIZE / float(N)))

        px = PADDING + int(LINE_SIZE) + j * (CELL_SIZE + LINE_SIZE)
        py = PADDING + int(LINE_SIZE) + i * (CELL_SIZE + LINE_SIZE)

        pygame.draw.rect(screen, win_color, (px, py, w, CELL_SIZE))
        pygame.draw.rect(screen, draw_color, (px + w, py, e, CELL_SIZE))
        pygame.draw.rect(screen, loss_color, (px + w + e, py, CELL_SIZE - w - e, CELL_SIZE))

        # Text
        score = int(round(100 * (w + 0.5 * e) / (w + e + l)))
        text = font.render(str(score), True, (0, 0, 0))
        text_rect = text.get_rect(center=(px + CELL_SIZE / 2., py + CELL_SIZE / 2.))
        screen.blit(text, text_rect)

for i in range(n):
    text = font.render("(" + str(1+i) + ")", True, (0,0,0))
    p1 = PADDING / 2.
    p2 = LINE_SIZE + PADDING + (i+0.5) * (CELL_SIZE + LINE_SIZE)
    text_rect = text.get_rect(center=(p1, p2))
    screen.blit(text, text_rect)
    text_rect = text.get_rect(center=(p2, p1))
    screen.blit(text, text_rect)

    text2 = font.render("(" + str(1+i) + ") " + NAMES[i], True, (0,0,0))
    text_rect2 = text2.get_rect()
    text_rect2.left = SIZE + 2*p1  # Set the left attribute
    text_rect2.centery = p2  # Keep the vertical centering
    screen.blit(text2, text_rect2)  # Use text2 here


# Save to file
pygame.image.save(screen, "results_image.png")


if __name__ == '__main__':
    game = True
    while game:
        if display:
            # Render the environment

            # Check for pygame event (to close the window)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit cross
                    game = False

            # Delay to not spam
            pygame.time.delay(1)
            pygame.display.flip()

    pygame.quit()
