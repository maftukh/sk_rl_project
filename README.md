# RL breaking Ultimate Tic-Tac-Toe :x: :o:

The main goal of this project  is to design an AI using RL to play Ultimate Tic Tac Toe.
To achive this goa we improved and implemented different algorithms that play U3T

## Rules of the game

+ The game starts with X playing wherever they want in any of the 81 empty spots.
+ Next the opponent plays, however they are forced to play in the small board indicated by the relative location of the previous move. Playing any of the available spots decides in which small board the next player plays.
+ If a move is played so that it is to win a small board by the rules of normal tic-tac-toe, then the entire small board is marked as won by the player in the larger board.
+ Once a small board is won by a player or it is filled completely, no more moves may be played in that board.
+ If a player is sent to such a board, then that player may play in any other board.
+ Game play ends when either a player wins the larger board or there are no legal moves remaining, in which case the game is a draw

> [!IMPORTANT]
> This additonal rules that makes it far more complex than you think in a first glance and create some difficulties not only for AI by human player itself

## Installation

To install this repo use

```shell
git clone https://github.com/maftukh/sk_rl_project.git
```

For preventing potential path-related issues, we recommend setting correct PYTHONPATH

```shell
cd sk_rl_project
export PYTHONPATH=${PYTHONPATH}:${pwd}
```

and then to install all the nessery packages from `requirements.txt`

```shell
pip install -r requirements.txt
```

or by creating custom conda environment by simply running:

```shell
conda env create -f environment.yml
```
<!-- To install all

```shell
pip install pygame numpy gym torchvision time 
``` -->

## This repo is...

Our code is based on another GitHub repository. We reproduced the results of [paper](https://josselinsomervilleroberts.github.io/papers/Report_INF581.pdf) and made several improvements.

## How to launch

You need to launch from the root of the folder the scripts in `play_modes` directory.

You can use `agent_in_single_player_env.py` to make 2 agent fight each other (one of them can be you).

```shell
python play_modes/agent_in_single_player_env.py
```

The best agent is `MinimaxPruningAgentSeveralRewards` so try to beat him!

We also added bash scripts that we've used for reproducibility of our experiments

<br/>

## How to recreate the results 

You can launch `play_modes/stats.py` to make each agent fight against each other for several games in order to get statistics. However, this process takes dozen of hours so you need to be patient. To then visualize the figure presented in the paper, you can then use `display_results.py` with the values printed by the previous script. 

or run bash scrips in `bash_scripts` folder

## Conclusions

In this work, we have conducted a research on different agents that play Ultimate Tic-Tac-Toe
The minimax and MCTS agents need a trade-off between decision time and performance
The reward function has its own drawbacks but we can improve DQL agent by increasing training time

## Team

+ Kira Kuznetsova
+ Vladislav Mityukov
+ Saydash Miftakhov
