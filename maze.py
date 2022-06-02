import turtle
import levels
import game_treasure
import random
import math

images = ["player.gif", "wall.gif", "Character.gif", "path.gif", "maze_final.gif"]
for image in images:
    turtle.register_shape(image)


class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        self.mypen = turtle.Turtle()
        self.mypen.hideturtle()
        self.scorepen = turtle.Turtle()
        self.scorepen.hideturtle()

    def set_pen(self, x, y):
        self.mypen.color("lightgrey")
        self.mypen.pensize(3)
        self.mypen.penup()
        self.mypen.setposition(x, y)
        self.mypen.pendown()

    def draw_border(self):
        self.mypen.color("white")
        self.mypen.forward(620)
        self.mypen.left(90)
        self.mypen.forward(735)
        self.mypen.left(90)
        self.mypen.forward(620)
        self.mypen.left(90)
        self.mypen.forward(735)
        self.mypen.left(90)
        self.mypen.hideturtle()

    def score_pen(self):
        self.scorepen.color("lightgrey")
        self.scorepen.penup()
        self.scorepen.hideturtle()
        self.scorepen.goto(190, -345)
        self.scorepen.write(f"Score: {player.gold}", align="left", font=("Arial", 16, "bold"))


class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("player.gif")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_x = self.xcor()
        move_y = self.ycor() + 24

        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def go_down(self):
        move_x = self.xcor()
        move_y = self.ycor() - 24

        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def go_left(self):
        move_x = self.xcor() - 24
        move_y = self.ycor()

        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def go_right(self):
        move_x = self.xcor() + 24
        move_y = self.ycor()

        if (move_x, move_y) not in walls:
            self.goto(move_x, move_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 4:
            return True
        else:
            return False


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("Character.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            dx = -24
            dy = 0
        elif self.direction == "right":
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


wn = turtle.Screen()
wn.title("Maze Game")
wn.setup(700, 800)
# Treasures list
treasures = []
enemies = []
walls = []
pen = Pen()
player = Player()
game_on = True


def play_again(x, y):
    wn.clearscreen()
    wn.ontimer(splashscreen, 50)


def splashscreen():
    a = turtle.Turtle()
    wn = turtle.Screen()
    wn.bgpic("maze_final.gif")
    a.hideturtle()
    wn.setup(700, 800)
    player.hideturtle()
    wn.tracer(0)
    wn.update()
    wn.ontimer(game, 3000)


def level_screen():
    wn.bgcolor("black")
    wn.tracer(0)


def bindings():

    # Key binding
    turtle.listen()
    turtle.onkey(player.go_up, "Up")
    turtle.onkey(player.go_down, "Down")
    turtle.onkey(player.go_left, "Left")
    turtle.onkey(player.go_right, "Right")

    wn.tracer(0)

    for enemy in enemies:
        turtle.ontimer(enemy.move, t=250)


def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            # get the character at each x, y coordinate
            character = level[y][x]
            # calculating the screen x, y coordinates
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            # checking if there is a wall
            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))
            if character == "P":
                player.goto(screen_x, screen_y)
            if character == "T":
                treasures.append(game_treasure.Treasure(screen_x, screen_y))
            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))


def game():
    global game_on, treasures, player, walls, pen, enemies
    treasures = []
    enemies = []
    walls = []
    win = False
    wn.clearscreen()
    wn.update()
    while game_on:
        pen = Pen()
        wn.clearscreen()
        level_screen()
        pen.set_pen(-310, -310)
        pen.draw_border()
        player = Player()
        setup_maze(levels.levels[1])
        bindings()
        pen.set_pen(-310, -360)
        pen.draw_border()

        pen.set_pen(-290, -345)
        pen.mypen.write("Level: 1", False, align="left", font=("Arial", 16, "bold"))
        pen.score_pen()
        level_1_completed = False
        while not level_1_completed:
            # Player collision with treasure
            for treasure in treasures:
                if player.is_collision(treasure):
                    player.gold += treasure.gold
                    pen.scorepen.clear()
                    pen.score_pen()
                    print("Player Gold: {}".format(player.gold))
                    # Destroying and removing the found treasure from the list
                    treasure.destroy()
                    treasures.remove(treasure)
                    if player.gold == 300:
                        level_1_completed = True
            wn.update()

        treasures = []
        walls = []

        pen = Pen()
        wn.clearscreen()
        level_screen()
        pen.set_pen(-310, -310)
        pen.draw_border()
        player = Player()

        setup_maze(levels.levels[2])
        bindings()
        pen.set_pen(-310, -360)
        pen.draw_border()
        pen.set_pen(-300, -340)
        pen.mypen.write("Level: 2", False, align="left", font=("Arial", 16, "bold"))
        pen.score_pen()
        level_2_completed = False
        gameover = False
        while not level_2_completed:

            # Player collision with treasure
            for treasure in treasures:
                if player.is_collision(treasure):
                    player.gold += treasure.gold
                    pen.scorepen.clear()
                    pen.score_pen()

                    print("Player Gold: {}".format(player.gold))
                    # Destroying and removing the found treasure from the list
                    treasure.destroy()
                    treasures.remove(treasure)
                    if player.gold == 300:
                        level_2_completed = True
            for enemy in enemies:
                if player.is_collision(enemy):
                    level_2_completed = True
                    gameover = True
            wn.update()
        if gameover:
            pen.set_pen(0, 320)
            pen.mypen.write("Game Over", False, align="center", font=("Arial", 24, "bold"))
            wn.listen()
            wn.onscreenclick(play_again)
            break
        treasures = []
        walls = []
        enemies = []

        pen = Pen()
        wn.clearscreen()
        level_screen()
        pen.set_pen(-310, -310)
        pen.draw_border()
        player = Player()

        level_3_completed = False
        setup_maze(levels.levels[3])
        bindings()
        pen.set_pen(-310, -360)
        pen.draw_border()
        pen.set_pen(-300, -340)
        pen.mypen.write("Level: 3", False, align="left", font=("Arial", 16, "bold"))
        pen.score_pen()
        while not level_3_completed:
            # Player collision with treasure
            for treasure in treasures:
                if player.is_collision(treasure):
                    player.gold += treasure.gold
                    pen.scorepen.clear()
                    pen.score_pen()
                    print("Player Gold: {}".format(player.gold))
                    # Destroying and removing the found treasure from the list
                    treasure.destroy()
                    treasures.remove(treasure)
                    if player.gold == 300:
                        level_3_completed = True
                        win = True
                        break
            for enemy in enemies:
                if player.is_collision(enemy):
                    level_3_completed = True
                    gameover = True

            wn.update()
        if gameover:
            pen.set_pen(0, 320)
            pen.mypen.write("Game Over", False, align="center", font=("Arial", 24, "bold"))
            wn.listen()
            wn.onscreenclick(play_again)
            break
        if win:
            pen.set_pen(0, 320)
            pen.mypen.write("You Win !", False, align="center", font=("Arial", 24, "bold"))

        game_on = False


splashscreen()

wn.mainloop()
