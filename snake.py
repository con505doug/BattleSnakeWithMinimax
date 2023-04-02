class snake:
  def __init__(self, head, body, health, length, eaten_food=[]):
    self.head = head
    self.body = body
    self.health = health
    self.length = length
    self.eaten_food = []
    self.previous_tail = []
    self.ate_food = []


  def get_closest_food(self, all_food):
    closest_food = None
    food_distance = 10000
    for food in all_food:
      x_distance = abs(self.head["x"] - food["x"])
      y_distance = abs(self.head["y"] - food["y"])
      total_distance = x_distance + y_distance
      if total_distance < food_distance:
        food_distance = total_distance
        closest_food = food
        
    return closest_food, food_distance

  def get_move_coords(self, move):
    if move == "right":
      return {"x": self.head["x"] + 1, "y": self.head["y"]}
    elif move == "left":
      return {"x": self.head["x"] - 1, "y": self.head["y"]}
    elif move == "up":
      return {"x": self.head["x"], "y": self.head["y"] + 1}
    else:
      return {"x": self.head["x"], "y": self.head["y"] - 1}
    
                          # R L U D            
  def get_safe_moves(self, possible_moves, board_height, board_width, enemy_snake):
    safe_moves = []
    safe_coords = []
    for move in possible_moves:
      move_coords = self.get_move_coords(move)
      if move_coords in self.body[:-1]:
        continue
      if move_coords["x"] == board_width or move_coords["x"] < 0:
        continue
      if move_coords["y"] == board_height or move_coords["y"] < 0:
        continue
      if move_coords in enemy_snake.body[1:-1]:
        continue
      safe_moves.append(move)
      safe_coords.append(move_coords)
    return safe_moves, safe_coords

  def move(self, move, eats_food):
    self.head = self.get_move_coords(move)
    self.body.insert(0, self.head)
    if not eats_food:
      self.previous_tail.append(self.body.pop())
      self.ate_food.append(False)
    else:
      self.previous_tail.append(self.previous_tail[-1])
      self.length = self.length + 1
      self.ate_food.append(True)
      
    return
    
  def undo_move(self):
    self.head = self.body[1]
    self.body.pop(0)
    self.body.append(self.previous_tail.pop())
    if self.ate_food.pop() == True:
      self.body.pop()
      self.length = self.length - 1

    return
    