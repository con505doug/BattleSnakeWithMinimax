import math
import copy
import board
import snake
import time

def eval_function(my_board):
  my_moves, my_move_coords = my_board.my_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.opp_snake)
  opp_moves, opp_move_coords = my_board.opp_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.my_snake)
  enemy_close = False
  need_food = False
  #print("Head: ", my_board.my_snake.head)
  #print("Mine: ", my_board.my_snake.body)
  #print("Opp Head: ", my_board.opp_snake.head)
  if my_board.my_snake.head == my_board.opp_snake.head and len(my_board.my_snake.body) <= len(my_board.opp_snake.body):
    #print("DANGER")
    #print("Mine: ", my_board.my_snake.body)
    #print("Opp: ", my_board.opp_snake.body)
    return -math.inf, None

  elif my_board.my_snake.head == my_board.opp_snake.head and len(my_board.my_snake.body) > len(my_board.opp_snake.body):
    #print("ATTACK")
    return math.inf, None
    
  #for move in my_move_coords:
  #  if move in opp_move_coords:
  #    enemy_close = True
  enemy_distance = abs(my_board.my_snake.head["x"] - my_board.opp_snake.head["x"]) + abs(my_board.my_snake.head["y"] - my_board.opp_snake.head["y"])
  if enemy_distance <= 5:
    enemy_close = True

  if my_board.my_snake.health < 50 or len(my_board.my_snake.body) <= len(my_board.opp_snake.body):
    need_food = True

  if enemy_close and need_food:
    food_weight = 40
    safety_weight = 60
    attack_weight = 0
  elif enemy_close and not need_food:
    food_weight = 5
    safety_weight = 70
    attack_weight = 100
  elif not enemy_close and need_food:
    food_weight = 100
    safety_weight = 30
    attack_weight = 0
  else:
    food_weight = 5
    safety_weight = 35
    attack_weight = 60


  closest_food, food_distance = my_board.my_snake.get_closest_food(my_board.food)
  if closest_food == None:
    food_weight = 0
  elif my_board.my_snake.head == closest_food:
    food_distance = .5
    
  enemy_distance = abs(my_board.my_snake.head["x"] - my_board.opp_snake.head["x"]) + abs(my_board.my_snake.head["y"] - my_board.opp_snake.head["y"])

  #print("Food eaten: " , len(my_board.my_snake.eaten_food))
  score = (len(my_board.my_snake.eaten_food) + 1) * (len(my_moves) * safety_weight + (3 / food_distance) * food_weight + (3 / enemy_distance) * attack_weight)
  #print("Food: ", food_distance)
  #print(score)

  return score, None

def minimax(my_board, depth, alpha, beta, maximizing_player, t0):
  t1 = time.perf_counter()
  total_time = t1 - t0
  '''if total_time > .400 and depth%2 == 0:
    print(total_time)
    print(depth)
    depth = 0'''

  if depth == 0 or my_board.is_over:
    return eval_function(my_board)

  if maximizing_player:
    value = -math.inf
    best_move = None
    my_moves, my_move_coords = my_board.my_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.opp_snake)
    ate_food = None

    for move, move_coords in zip(my_moves, my_move_coords):
      future_board = my_board
      #future_board = copy.deepcopy(my_board)
      #future_board = board.board(my_board.height, my_board.width, snake.snake(my_board.my_snake.head.copy(), my_board.my_snake.body.copy(), my_board.my_snake.health, my_board.my_snake.length, my_board.my_snake.eaten_food.copy()), snake.snake(my_board.opp_snake.head.copy(), my_board.opp_snake.body.copy(), my_board.opp_snake.health, my_board.opp_snake.length, my_board.opp_snake.eaten_food.copy()), my_board.food.copy(), my_board.eaten_food.copy())
      #future_board = board.board(my_board.height, my_board.width, copy.deepcopy(my_board.my_snake) , copy.deepcopy(my_board.opp_snake), my_board.food.copy(), my_board.eaten_food.copy())
      #print("in max: ", move_coords)
      #print("in max: ", move_coords)copy.deepcopy(my_board.my_snake)
      #print(my_board.food)
      if move_coords in my_board.food:
        ate_food = move_coords
        future_board.food.remove(move_coords)
        future_board.my_snake.move(move, True)
        future_board.eaten_food.append(move_coords)
        future_board.my_snake.eaten_food.append(move_coords)
      else:
        future_board.my_snake.move(move, False)

      tmp_value, tmp_move = minimax(future_board, depth - 1, alpha, beta, False, t0)
      new_value = max(value, tmp_value)

      if new_value > value:
        value = new_value
        best_move = move

      future_board.my_snake.undo_move()
      if ate_food == move_coords:
        future_board.food.append(move_coords)
        future_board.eaten_food.remove(move_coords)
        future_board.my_snake.eaten_food.remove(move_coords)

      alpha = max(alpha, value)
      if alpha >= beta:
        break

    #print("max: ", value, best_move)
    return value, best_move
      
  else:
    value = math.inf
    best_move = None
    opp_moves, opp_move_coords = my_board.opp_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.my_snake)
    ate_food = None

    for move, move_coords in zip(opp_moves, opp_move_coords):
      future_board = my_board
      #future_board = copy.deepcopy(my_board)
      #future_board = board.board(my_board.height, my_board.width, snake.snake(my_board.my_snake.head.copy(), my_board.my_snake.body.copy(), my_board.my_snake.health, my_board.my_snake.length, my_board.my_snake.eaten_food.copy()), snake.snake(my_board.opp_snake.head.copy(), my_board.opp_snake.body.copy(), my_board.opp_snake.health, my_board.opp_snake.length, my_board.opp_snake.eaten_food.copy()), my_board.food.copy(), my_board.eaten_food.copy())
      #future_board = board.board(my_board.height, my_board.width, copy.deepcopy(my_board.my_snake) , copy.deepcopy(my_board.opp_snake), my_board.food.copy(), my_board.eaten_food.copy())
      #print("in max: ", move_coords)
      if move_coords in my_board.food:
        ate_food = move_coords
        future_board.food.remove(move_coords)
        future_board.opp_snake.move(move, True)
        future_board.eaten_food.append(move_coords)
        future_board.opp_snake.eaten_food.append(move_coords)
      else:
        future_board.opp_snake.move(move, False)
        
      if future_board.opp_snake.head == future_board.my_snake.head:
        future_board.is_over = True

      tmp_value, tmp_move = minimax(future_board, depth - 1, alpha, beta, True, t0)
      new_value = min(value, tmp_value)
      if new_value < value:
        value = new_value
        best_move = move
      
      future_board.opp_snake.undo_move()
      if ate_food == move_coords:
        future_board.food.append(move_coords)
        future_board.eaten_food.remove(move_coords)
        future_board.opp_snake.eaten_food.remove(move_coords)

      beta = min(beta, value)
      if alpha >= beta:
        break

    #print("min: ", value, best_move)
    return value, best_move
    