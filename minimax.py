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
  avoid_edges = False
  edge_modifer = 0
  trap_modifier = 0

  if my_board.out_of_time:
    return None, None, my_board.out_of_time
  #print("Head: ", my_board.my_snake.head)
  #print("Mine: ", my_board.my_snake.body)
  #print("Opp Head: ", my_board.opp_snake.head)
  if my_board.my_snake.head == my_board.opp_snake.head and len(my_board.my_snake.body) <= len(my_board.opp_snake.body) or len(my_moves) == 0:
    #print("DANGER")
    #print("Mine: ", my_board.my_snake.body)
    #print("Opp: ", my_board.opp_snake.body)
    return -math.inf, None, my_board.out_of_time

  elif my_board.my_snake.head == my_board.opp_snake.head and len(my_board.my_snake.body) > len(my_board.opp_snake.body) or len(opp_moves) == 0:
    #print("ATTACK")
    return math.inf, None, my_board.out_of_time
    
  #for move in my_move_coords:
  #  if move in opp_move_coords:
  #    enemy_close = True
  enemy_distance = abs(my_board.my_snake.head["x"] - my_board.opp_snake.head["x"]) + abs(my_board.my_snake.head["y"] - my_board.opp_snake.head["y"])
  if enemy_distance <= 5:
    enemy_close = True
    avoid_edges = True

  if len(my_board.my_snake.body) <= 10:
    length_adder = 3
  elif len(my_board.my_snake.body) <= 20:
    length_adder = 2
  else:
    length_adder = 1
    
  if my_board.my_snake.health < 50 or len(my_board.my_snake.body) <= len(my_board.opp_snake.body) + length_adder:
    need_food = True
    snake_length_modifer = (len(my_board.my_snake.eaten_food) + 1)
  else:
    snake_length_modifer = 1

  if enemy_close and need_food:
    food_weight = 40
    safety_weight = 60
    attack_weight = 0
  elif enemy_close and not need_food:
    food_weight = 0
    safety_weight = 100
    attack_weight = 70
  elif not enemy_close and need_food:
    food_weight = 100
    safety_weight = 30
    attack_weight = 0
  else:
    food_weight = 0
    safety_weight = 35
    attack_weight = 60

  left_wall_dist = my_board.my_snake.head['x']
  right_wall_dist = my_board.width - my_board.my_snake.head['x']  - 1
  bottom_wall_dist = my_board.my_snake.head['y']
  top_wall_dist = my_board.height - my_board.my_snake.head['y'] - 1

  my_width_edge = min(left_wall_dist, right_wall_dist)
  my_height_edge = min(bottom_wall_dist, top_wall_dist)

  edge_score = my_width_edge + my_height_edge

  left_wall_dist = my_board.opp_snake.head['x']
  right_wall_dist = my_board.width - my_board.opp_snake.head['x']  - 1
  bottom_wall_dist = my_board.opp_snake.head['y']
  top_wall_dist = my_board.height - my_board.opp_snake.head['y'] - 1

  width_edge = min(left_wall_dist, right_wall_dist)
  height_edge = min(bottom_wall_dist, top_wall_dist)

  if (width_edge == my_width_edge - 1 or height_edge == my_height_edge - 1) and enemy_close:
    safety_weight = safety_weight + 100

  if ((width_edge == 0 or height_edge == 0) or (len(opp_moves) == 1)) and enemy_close:
    trap_modifier = 100 / enemy_distance

  closest_food, food_distance = my_board.my_snake.get_closest_food(my_board.food)
  if closest_food == None:
    food_weight = 0
  elif my_board.my_snake.head == closest_food:
    food_distance = .5
    

  #print("Food eaten: " , len(my_board.my_snake.eaten_food))
  score = snake_length_modifer * ((len(my_moves) * safety_weight) * 2 + (3 / food_distance) * food_weight + (3 / enemy_distance) * attack_weight + safety_weight * edge_score + attack_weight * trap_modifier)
  #print("Food: ", food_distance)
  #print(score)

  return score, None, my_board.out_of_time

def minimax(my_board, depth, alpha, beta, maximizing_player, t0):
  t1 = time.perf_counter()
  total_time = t1 - t0
  if total_time > .460:
    depth = 0
    my_board.out_of_time = True


  if depth == 0 or my_board.is_over:
    return eval_function(my_board)

  if maximizing_player:
    value = -math.inf
    best_move = None
    my_moves, my_move_coords = my_board.my_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.opp_snake)
    ate_food = None
    if len(my_moves) == None:
      my_board.is_over = True
      tmp_value, tmp_move, out_of_time = minimax(future_board, depth - 1, alpha, beta, False, t0)
      if out_of_time:
        return None, None, out_of_time
      new_value = max(value, tmp_value)

      if new_value > value:
        value = new_value
        best_move = move

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

      tmp_value, tmp_move, out_of_time = minimax(future_board, depth - 1, alpha, beta, False, t0)
      if out_of_time:
        return None, None, out_of_time
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
    return value, best_move, False
      
  else:
    value = math.inf
    best_move = None
    opp_moves, opp_move_coords = my_board.opp_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.my_snake)
    ate_food = None
    if len(opp_moves) == None:
      my_board.is_over = True
      tmp_value, tmp_move, out_of_time = minimax(future_board, depth - 1, alpha, beta, True, t0)
      if out_of_time:
        return None, None, out_of_time
      new_value = min(value, tmp_value)
      if new_value < value:
        value = new_value
        best_move = move
      


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

      tmp_value, tmp_move, out_of_time = minimax(future_board, depth - 1, alpha, beta, True, t0)
      if out_of_time:
        return None, None, out_of_time
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
    return value, best_move, False
    