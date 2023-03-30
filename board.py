class board:
  def __init__(self, height, width, my_snake, opp_snake, food, eaten_food=[]):
    self.height = height
    self.width = width
    self.my_snake = my_snake
    self.opp_snake = opp_snake
    self.food = food
    self.eaten_food = eaten_food
    self.moves = ["up", "down", "left", "right"]
    self.is_over = False