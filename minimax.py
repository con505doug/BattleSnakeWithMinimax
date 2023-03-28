import math
import copy

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
    safety_weight = 35
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
  if my_board.my_snake.head == closest_food:
    food_distance = .8
    
  enemy_distance = abs(my_board.my_snake.head["x"] - my_board.opp_snake.head["x"]) + abs(my_board.my_snake.head["y"] - my_board.opp_snake.head["y"])

  print("Food eaten: " , len(my_board.my_snake.eaten_food))
  score = (len(my_board.my_snake.eaten_food) + 1) * (len(my_moves) * safety_weight + (3 / food_distance) * food_weight + (3 / enemy_distance) * attack_weight)
  #print("Food: ", food_distance)
  print(score)

  return score, None

def minimax(my_board, depth, maximizing_player):
  if depth == 0 or my_board.is_over:
    return eval_function(my_board)

  if maximizing_player:
    print("OK")
    value = -math.inf
    best_move = None
    my_moves, my_move_coords = my_board.my_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.opp_snake)
    
    for move in my_moves:
      future_board = copy.deepcopy(my_board)
      if move in my_board.food:
        future_board.food.remove(move)
        future_board.my_snake.move(move, True)
        future_board.eaten_food.append(move)
        future_board.my_snake.eaten_food.append(move)
      else:
        future_board.my_snake.move(move, False)

      tmp_value, tmp_move = minimax(future_board, depth - 1, False)
      new_value = max(value, tmp_value)
      if new_value > value:
        value = new_value
        best_move = move

    #print("max: ", value, best_move)
    return value, best_move
      
  else:
    value = math.inf
    best_move = None
    opp_moves, opp_move_coords = my_board.opp_snake.get_safe_moves(my_board.moves, my_board.height, my_board.width, my_board.my_snake)

    for move in opp_moves:
      future_board = copy.deepcopy(my_board)
      if move in my_board.food:
        future_board.food.remove(move)
        future_board.opp_snake.move(move, True)
        future_board.eaten_food.append(move)
        future_board.opp_snake.eaten_food.append(move)
      else:
        future_board.opp_snake.move(move, False)
        
      if future_board.opp_snake.head == future_board.my_snake.head:
        future_board.is_over = True

      tmp_value, tmp_move = minimax(future_board, depth - 1, True)
      new_value = min(value, tmp_value)
      if new_value < value:
        value = new_value
        best_move = move

    #print("min: ", value, best_move)
    return value, best_move
    