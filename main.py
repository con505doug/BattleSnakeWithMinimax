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
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

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
    print("Orig Head: ", my_snake.head)
    print("Orig Body: ", my_snake.body)
    my_snake.move("up", True)
    print("Next Head: ", my_snake.head)
    print("Next Body: ", my_snake.body)
    my_snake.move("left", True)
    #my_snake.undo_move()
    print("After Head: ", my_snake.head)
    print("After Body: ", my_snake.body)
    my_snake.move("down", False)
    print("Next Head: ", my_snake.head)
    print("Next Body: ", my_snake.body)
    my_snake.move("down", True)
    print("Next Head: ", my_snake.head)
    print("Next Body: ", my_snake.body)
    my_snake.undo_move()
    print("Next Head: ", my_snake.head)
    print("Next Body: ", my_snake.body)
    my_snake.undo_move()
    print("Next Head: ", my_snake.head)
    print("Next Body: ", my_snake.body)
    


    value, best_move = minimax(my_board, 6, -math.inf, math.inf, True, t0)
    if best_move == None:
      safe_moves, safe_coords = my_snake.get_safe_moves(moves, my_board.height,my_board.width, opp_snake)
      if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
        best_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {best_move}")
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(elapsed)
    return {"move": best_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    gamestate = {"you":{"latency":"15.329","id":"ef8ca03f-fab5-4498-9163-2a7d43c0ac85","health":88,"length":3,"shout":"","head":{"y":9,"x":1},"customizations":{"color":"#66ff33","tail":"default","head":"default"},"body":[{"y":9,"x":1},{"y":8,"x":1},{"y":7,"x":1}],"name":"Snek","squad":""},"turn":12,"board":{"snakes":[{"latency":"0.019497999979649","id":"5679bee1-530c-4fe2-9801-06c14e39ae9f","health":92,"length":4,"shout":"","head":{"y":8,"x":2},"customizations":{"color":"#ffffff","tail":"alligator","head":"all-seeing"},"body":[{"y":8,"x":2},{"y":7,"x":2},{"y":6,"x":2},{"y":5,"x":2}],"name":"Bot","squad":""},{"latency":"15.329","id":"ef8ca03f-fab5-4498-9163-2a7d43c0ac85","health":88,"length":3,"shout":"","head":{"y":9,"x":1},"customizations":{"color":"#66ff33","tail":"default","head":"default"},"body":[{"y":9,"x":1},{"y":8,"x":1},{"y":7,"x":1}],"name":"Snek","squad":""}],"width":11,"hazards":[],"height":11,"food":[{"y":10,"x":4},{"y":6,"x":0}]},"game":{"source":"custom","ruleset":{"version":"Mojave/3.5.2","name":"standard","settings":{"hazardDamagePerTurn":14,"royale":{"shrinkEveryNTurns":25},"squad":{"sharedHealth":True,"sharedLength":True,"allowBodyCollisions":True,"sharedElimination":True},"minimumFood":1,"foodSpawnChance":15}},"timeout":500,"id":"c48ab6a8-76fe-45f4-a33e-1b4e852b31cf"}}
    print(move(gamestate))
