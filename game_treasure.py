import turtle
turtle.register_shape("Treasure.gif")


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("Treasure.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.gold = 100

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()
