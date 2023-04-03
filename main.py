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
    '''print("Orig Head: ", my_snake.head)
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
    print("Next Body: ", my_snake.body)'''
    


    value, best_move = minimax(my_board, 10, -math.inf, math.inf, True, t0)
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
    gamestate = {"you":{"latency":"51.442","id":"ef8ca03f-fab5-4498-9163-2a7d43c0ac85","health":72,"length":4,"shout":"","head":{"y":7,"x":4},"customizations":{"color":"#66ff33","tail":"default","head":"default"},"body":[{"y":7,"x":4},{"y":8,"x":4},{"y":9,"x":4},{"y":10,"x":4}],"name":"Snek","squad":""},"turn":37,"board":{"snakes":[{"latency":"0.012463199964259","id":"5679bee1-530c-4fe2-9801-06c14e39ae9f","health":99,"length":6,"shout":"","head":{"y":9,"x":8},"customizations":{"color":"#ffffff","tail":"alligator","head":"all-seeing"},"body":[{"y":9,"x":8},{"y":10,"x":8},{"y":10,"x":7},{"y":10,"x":6},{"y":9,"x":6},{"y":8,"x":6}],"name":"Bot","squad":""},{"latency":"51.442","id":"ef8ca03f-fab5-4498-9163-2a7d43c0ac85","health":72,"length":4,"shout":"","head":{"y":7,"x":4},"customizations":{"color":"#66ff33","tail":"default","head":"default"},"body":[{"y":7,"x":4},{"y":8,"x":4},{"y":9,"x":4},{"y":10,"x":4}],"name":"Snek","squad":""}],"width":11,"hazards":[],"height":11,"food":[{"y":4,"x":0},{"y":6,"x":5}]},"game":{"source":"custom","ruleset":{"version":"Mojave/3.5.2","name":"standard","settings":{"hazardDamagePerTurn":14,"royale":{"shrinkEveryNTurns":25},"squad":{"sharedHealth":True,"sharedLength":True,"allowBodyCollisions":True,"sharedElimination":True},"minimumFood":1,"foodSpawnChance":15}},"timeout":500,"id":"dce914c4-9e45-40bb-b491-11b7f996aed2"}}
    print(move(gamestate))
