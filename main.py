# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import snake
import board
from minimax import *
import math
#import minimax
import time


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Snek",  # TODO: Your Battlesnake Username
        "color": "#66ff33",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    t0 = time.perf_counter()
    t1 = 0

    moves = ["up", "down", "left", "right"]
    my_snake = snake.snake(game_state["you"]["head"], game_state["you"]["body"], game_state["you"]["health"], game_state["you"]["length"])

    if len(game_state["board"]["snakes"]) == 1:
      return {"move": random.choice(moves)}
      
    for against in game_state["board"]["snakes"]:
      if against != game_state["you"]:
        opp_snake = snake.snake(against["head"], against["body"], against["health"], against["length"])

    my_board = board.board(game_state["board"]["height"], game_state["board"]["width"], my_snake, opp_snake, game_state["board"]["food"])      
    #score = eval_function(my_board)
    #print(score)

    
    #safe_moves, safe_coords = my_snake.get_safe_moves(moves, my_board.height,my_board.width, opp_snake)

    #print("Head Actual: ", game_state["you"]["head"])
    #print("Opp Head Actual: ", opp_snake.head)
    depth = 2
    while (t1 - t0) < .460:
        value, temp_move, out_of_time = minimax(my_board, depth, -math.inf, math.inf, True, t0)
        if not out_of_time:
            depth = depth + 4
            best_move = temp_move
        t1 = time.perf_counter()

    if best_move == None:
      safe_moves, safe_coords = my_snake.get_safe_moves(moves, my_board.height,my_board.width, opp_snake)
      if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
      best_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {best_move}\n")
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(elapsed)
    return {"move": best_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
