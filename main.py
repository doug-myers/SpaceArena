# Space Arena!
# The Ultimate Python Turtle Graphics Game Tutorial
# Python 3.x Compatible
# Windows, MacOSX, and Linux Compatible
# by @TokyoEdtech
# Blog: https://www.christianthompson.com
# YouTube Channel: https://www.youtube.com/channel/UC2vm-0XX5RkWCXWwtBZGOXg/
# Improvements by Doug Myers:
# - Heal and Multishot Power-up
# - Rework range on radar
# - Game Over screen when lives are gone
# - Added gifs
# - Added star background
# - Double enemies each level
# - Add sound
import time
import turtle
import math
import random
import winsound
from turtlewriter import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
INFO_WIDTH = 200
INFO_CENTER = SCREEN_WIDTH / 2
CAMERA_OFFSET = INFO_WIDTH / 2
COLLISION_CHECK_RANGE = 300

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH + INFO_WIDTH, SCREEN_HEIGHT)
wn.title("Space Arena! by @TokyoEdTech")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

game_speed = 0.3
hs_file = open("highscore.txt", "r")
high_score = int(hs_file.read())
hs_file.close()

wn.register_shape("background.gif")
wn.register_shape("powerup.gif")
wn.register_shape("powerup2.gif")
wn.register_shape("powerup3.gif")
wn.register_shape("bomb.gif")
wn.register_shape("surveillance.gif")
wn.register_shape("mine.gif")
wn.register_shape("hunter.gif")


class Game:
    NUM_FRAME_TIMES = 500

    def __init__(self, width, height):
        self.target_frame_time = 1/60
        self.frame_time_index = 0
        self.total_frame_times = 0
        self.frame_times = []
        for i in range(Game.NUM_FRAME_TIMES):
            self.frame_times.append(0.0)
        self.max_frame_time = 0
        self.last_frame_time = 0
        self.width = width
        self.height = height
        self.level = 1
        self.state = "splash"

    def start_level(self):
        sprites.clear()

        # Add enemy missiles
        for enemy_missile in enemy_missiles:
            sprites.append(enemy_missile)

        # Add player
        sprites.append(player)

        # Add missile
        for missile in missiles:
            sprites.append(missile)

        # Add bomb
        sprites.append(bomb)

        # Add enemies
        Enemy.count = 2**self.level
        for _ in range(2**self.level):
            # Pick a random location away from the player
            while True:
                x = random.randint(-self.width / 2, self.width / 2)
                y = random.randint(-self.height / 2, self.height / 2)
                if abs(player.x - x) > COLLISION_CHECK_RANGE or \
                        abs(player.y - y) > COLLISION_CHECK_RANGE:
                    break
            dx = random.randint(-2, 2) * game_speed
            dy = random.randint(-2, -2) * game_speed
            sprites.append(Enemy(x, y, dx, dy))

        # Add powerups
        for _ in range(1):
            x = random.randint(-self.width / 2, self.width / 2)
            y = random.randint(-self.height / 2, self.height / 2)
            dx = random.randint(-2, 2) * game_speed
            dy = random.randint(-2, -2) * game_speed
            sprites.append(Powerup(x, y, "powerup.gif", "white", "multishot", dx, dy))

        for _ in range(1):
            x = random.randint(-self.width / 2, self.width / 2)
            y = random.randint(-self.height / 2, self.height / 2)
            dx = random.randint(-2, 2) * game_speed
            dy = random.randint(-2, -2) * game_speed
            sprites.append(Powerup(x, y, "powerup2.gif", "green", "heal", dx, dy))

        for _ in range(1):
            x = random.randint(-self.width / 2, self.width / 2)
            y = random.randint(-self.height / 2, self.height / 2)
            dx = random.randint(-2, 2) * game_speed
            dy = random.randint(-2, -2) * game_speed
            sprites.append(Powerup(x, y, "powerup3.gif", "yellow", "bomb", dx, dy))

    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = -self.width / 2.0 - x_offset
        right = self.width / 2.0 - x_offset
        top = self.height / 2.0 - y_offset
        bottom = -self.height / 2.0 - y_offset

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()

    def render_info(self, pen, score, highscore, active_enemies):
        pen.color("#222255")
        pen.penup()
        pen.goto(INFO_CENTER, 0)
        pen.shape("square")
        pen.setheading(90)
        pen.shapesize(10, SCREEN_HEIGHT/20, None)
        pen.stamp()

        separator_x = INFO_CENTER - INFO_WIDTH / 2
        pen.color("white")
        pen.width(3)
        pen.goto(separator_x, SCREEN_HEIGHT / 2)
        pen.pendown()
        pen.goto(separator_x, -SCREEN_HEIGHT / 2)

        pen.penup()
        pen.color("white")
        character_pen.scale = 1.0
        character_pen.draw_string(pen, "SPACE ARENA", INFO_CENTER, 370)
        character_pen.draw_string(pen, "SCORE {}".format(score), INFO_CENTER, 330)
        character_pen.draw_string(pen, "HIGH SCORE", INFO_CENTER, 290)
        character_pen.draw_string(pen, str(highscore), INFO_CENTER, 260)
        character_pen.draw_string(pen, "ENEMIES {}".format(active_enemies), INFO_CENTER, 220)
        character_pen.draw_string(pen, "LIVES {}".format(player.lives), INFO_CENTER, 180)
        character_pen.draw_string(pen, "LEVEL {}".format(game.level), INFO_CENTER, 140)
        character_pen.draw_string(pen, "MULTISHOTS".format(player.multishot), INFO_CENTER, 100)
        character_pen.draw_string(pen, str(player.multishot), INFO_CENTER, 70)
        character_pen.draw_string(pen, "BOMBS {}".format(player.bombs), INFO_CENTER, 30)

    def start(self):
        self.state = "playing"

    def fps_delay(self):
        if self.last_frame_time > 0:
            t = time.time()
            actual = t - self.last_frame_time
            if actual > self.max_frame_time:
                self.max_frame_time = actual
            self.total_frame_times -= self.frame_times[self.frame_time_index]
            self.total_frame_times += actual
            self.frame_times[self.frame_time_index] = actual
            self.frame_time_index += 1
            self.frame_time_index %= Game.NUM_FRAME_TIMES
            delay = self.target_frame_time - actual
            if delay < 0.0001:
                delay = 0.0001
            time.sleep(delay)
        self.last_frame_time = time.time()

    def print_frame_time_stats(self):
        avg_frame_time = self.total_frame_times / Game.NUM_FRAME_TIMES
        print("Target Frame Time:  {}".format(self.target_frame_time))
        print("Average Frame Time: {}".format(avg_frame_time))
        print("Max Frame Time:     {}".format(self.max_frame_time))


# Splash Screen
character_pen = CharacterPen("red", 3.0)
character_pen.draw_string(pen, "SPACE ARENA", 0, 300)
character_pen.scale = 1.0
character_pen.draw_string(pen, "Originally by TOKYOEDTECH", 0, 240)
character_pen.draw_string(pen, "Modified by Doug Myers", 0, 210)

pen.color("white")
pen.shape("triangle")
pen.goto(-400, 140)
pen.shapesize(0.5, 1.0, None)
pen.stamp()
pen.shapesize(1.0, 1.0, None)
character_pen.draw_string(pen, "Player", -400, 100)

pen.shape("powerup2.gif")
pen.goto(-150, 140)
pen.stamp()
character_pen.draw_string(pen, "Heal Powerup", -150, 100)

pen.shape("powerup.gif")
pen.goto(150, 140)
pen.stamp()
character_pen.draw_string(pen, "Multishot Powerup", 150, 100)

pen.shape("powerup3.gif")
pen.goto(400, 140)
pen.stamp()
character_pen.draw_string(pen, "Bomb Powerup", 400, 100)

character_pen.draw_string(pen, "Enemy Droids", 0, 20)
pen.shape("hunter.gif")
pen.goto(-300, -20)
pen.stamp()
character_pen.draw_string(pen, "Hunter", -300, -60)

pen.shape("mine.gif")
pen.goto(0, -20)
pen.stamp()
character_pen.draw_string(pen, "Mine", 0, -60)

pen.shape("surveillance.gif")
pen.goto(300, -20)
pen.stamp()
character_pen.draw_string(pen, "Surveillance", 300, -60)

character_pen.draw_string(pen, "Up Arrow", -400, -160)
character_pen.draw_string(pen, "Accelerate", -400, -200)

character_pen.draw_string(pen, "Left Arrow", -150, -160)
character_pen.draw_string(pen, "Rotate Left", -150, -200)

character_pen.draw_string(pen, "Right Arrow", 150, -160)
character_pen.draw_string(pen, "Rotate Right", 150, -200)

character_pen.draw_string(pen, "Space", 400, -160)
character_pen.draw_string(pen, "Fire", 400, -200)

character_pen.scale = 1.0
character_pen.draw_string(pen, "PRESS S TO START", 0, -300)

wn.tracer(0)


class Sprite:
    # Constructor
    def __init__(self, x, y, shape, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = dx
        self.dy = dy
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.2 * game_speed
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"
        self.max_dx = 5 * game_speed
        self.max_dy = 5 * game_speed
        self.score = 0
        self.on_screen = True

    def is_collision(self, other):
        if self.on_screen and self.x - self.width/2 < other.x + other.width/2 and \
                self.x + self.width/2 > other.x - other.width/2 and \
                self.y - self.height/2 < other.y + other.height/2 and \
                self.y + self.height/2 > other.y - other.width/2:
            return True
        else:
            return False

    def bounce(self, other):
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dy = other.dy

        other.dx = temp_dx
        other.dy = temp_dy

    def update(self):
        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

        self.x += self.dx
        self.y += self.dy

        self.border_check()

    def border_check(self):
        if self.x > game.width / 2.0 - 10:
            self.x = game.width / 2.0 - 10
            self.dx *= -1

        elif self.x < -game.width / 2.0 + 10:
            self.x = -game.width / 2.0 + 10
            self.dx *= -1

        if self.y > game.height / 2.0 - 10:
            self.y = game.height / 2.0 - 10
            self.dy *= -1

        elif self.y < -game.height / 2.0 + 10:
            self.y = -game.height / 2.0 + 10
            self.dy *= -1

    def is_on_screen(self, x_offset, y_offset):
        if self.state != "active":
            return False
        x = self.x - x_offset + CAMERA_OFFSET
        if abs(x) > SCREEN_WIDTH / 2:
            return False
        y = self.y - y_offset
        if abs(y) > SCREEN_HEIGHT / 2:
            return False
        return True

    def render(self, pen, x_offset, y_offset):
        if self.is_on_screen(x_offset, y_offset):
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            self.render_health_meter(pen, x_offset, y_offset)

    def render_health_meter(self, pen, x_offset, y_offset):
        # Draw health meter
        pen.goto(self.x - x_offset - 10, self.y - y_offset + 20)
        pen.width(3)
        pen.pendown()
        pen.setheading(0)

        if self.health / self.max_health < 0.3:
            pen.color("red")
        elif self.health / self.max_health < 0.7:
            pen.color("yellow")
        else:
            pen.color("green")

        pen.fd(20.0 * (self.health / self.max_health))

        if self.health != self.max_health:
            pen.color("grey")
            pen.fd(20.0 * ((self.max_health - self.health) / self.max_health))

        pen.penup()

    def explode(self):
        winsound.PlaySound("Explosion+7.wav", winsound.SND_ASYNC)
        found = False
        for explosion in explosions:
            if explosion.state == "ready":
                found = True
                break
        if not found:
            explosion = Explosion(self.x, self.y)
            explosions.append(explosion)
        else:
            explosion.reset(self.x, self.y)


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self, 0, 0, "triangle", "white")
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0
        self.max_dx = 10 * game_speed
        self.max_dy = 10 * game_speed
        self.multishot = 0
        self.bombs = 0

    def rotate_left(self):
        self.da = 5

    def rotate_right(self):
        self.da = -5

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        self.thrust += self.acceleration

    def decelerate(self):
        self.thrust = 0.0

    def drop_bomb(self):
        if self.bombs > 0 and bomb.state == "ready":
            bomb.fire(self.x, self.y)
            self.bombs -= 1

    def fire(self):
        num_of_missiles = 0
        for missile in missiles:
            if missile.state == "ready":
                num_of_missiles += 1
        if num_of_missiles == 0:
            return

        winsound.PlaySound("Flash-laser-03.wav", winsound.SND_ASYNC)
        if self.multishot > 0:
            self.multishot -= 1
        else:
            num_of_missiles = 1

        # 1 missile ready
        if num_of_missiles == 1:
            for missile in missiles:
                if missile.state == "ready":
                    missile.fire(self.x, self.y, self.heading, self.dx, self.dy)
                    break

        # 2 missiles ready
        elif num_of_missiles == 2:
            directions = [-3, 3]
            for missile in missiles:
                if missile.state == "ready":
                    missile.fire(self.x, self.y, self.heading + directions.pop(), self.dx, self.dy)

        # 3 missiles ready
        elif num_of_missiles >= 3:
            directions = [0, -5, 5]
            for missile in missiles:
                if missile.state == "ready":
                    missile.fire(self.x, self.y, self.heading + directions.pop(), self.dx, self.dy)

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            # Set max speed
            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx

            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy

            self.x += self.dx
            self.y += self.dy

            self.border_check()

            # Check health
            if self.health <= 0:
                self.reset()

    def reset(self):
        global game_over
        self.lives -= 1
        if self.lives > 0:
            self.x = 0
            self.y = 0
            self.health = self.max_health
            self.heading = 90
            self.dx = 0
            self.dy = 0
        else:
            game_over = True

    def render(self, pen, x_offset, y_offset):
        if self.thrust > 0:
            # Render rocket fire
            flame = self.thrust/2.0
            x = self.x - 10 * math.cos(math.radians(self.heading))
            y = self.y - 10 * math.sin(math.radians(self.heading))
            if flame > 0.5:
                flame = 0.5
            pen.shapesize(0.2, flame, None)
            pen.goto(x - x_offset, y - y_offset)
            pen.setheading(self.heading + 180)
            pen.shape("triangle")
            pen.color("yellow")
            pen.stamp()
        pen.shapesize(0.5, 1.0, None)
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        pen.shapesize(1.0, 1.0, None)

        self.render_health_meter(pen, x_offset, y_offset)


class Missile(Sprite):
    max_fuel = 200

    def __init__(self):
        Sprite.__init__(self, 0, 0, "circle", "yellow")
        self.state = "ready"
        self.thrust = 8.0
        self.fuel = Missile.max_fuel
        self.height = 4
        self.width = 4

    def fire(self, x, y, heading, dx, dy):
        if self.state == "ready":
            self.state = "active"
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.fuel = Missile.max_fuel
        self.dx = 0
        self.dy = 0
        self.state = "ready"

    def render(self, pen, x_offset, y_offset):
        if self.is_on_screen(x_offset, y_offset):
            pen.shapesize(0.2, 0.2, None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(1.0, 1.0, None)


class Bomb(Sprite):
    max_fuse = 50

    def __init__(self):
        Sprite.__init__(self, 0, 0, "bomb.gif", "yellow")
        self.state = "ready"
        self.thrust = 8.0
        self.fuse = Bomb.max_fuse
        self.height = 10
        self.width = 10

    def fire(self, x, y):
        if self.state == "ready":
            self.state = "active"
            self.x = x
            self.y = y

    def update(self):
        if self.state == "active":
            self.fuse -= 1
            if self.fuse <= 0:
                self.reset()
                self.explode()

    def reset(self):
        self.fuse = Bomb.max_fuse
        self.state = "ready"

    def render(self, pen, x_offset, y_offset):
        if self.is_on_screen(x_offset, y_offset):
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

    def explode(self):
        winsound.PlaySound("Explosion+7.wav", winsound.SND_ASYNC)
        bomb_explosion.reset(self.x, self.y)


class EnemyMissile(Sprite):
    max_fuel = 200

    def __init__(self):
        Sprite.__init__(self, 0, 0, "circle", "red")
        self.state = "ready"
        self.thrust = 8.0
        self.fuel = EnemyMissile.max_fuel
        self.height = 4
        self.width = 4

    def fire(self, x, y, heading, dx, dy):
        if self.state == "ready":
            winsound.PlaySound("Flash-laser-02.wav", winsound.SND_ASYNC)
            self.state = "active"
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.fuel = EnemyMissile.max_fuel
        self.dx = 0
        self.dy = 0
        self.state = "ready"

    def render(self, pen, x_offset, y_offset):
        if self.is_on_screen(x_offset, y_offset):
            pen.shapesize(0.2, 0.2, None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(1.0, 1.0, None)


class Explosion(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, x, y, "circle", "yellow")
        self.time = 0
        self.max_time = 10
        self.max_size = 60
        self.colors = ["yellow", "orange", "red", "dark red"]

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        self.width = 20
        self.height = 20
        self.state = "active"

    def update(self):
        if self.state == "active":
            self.time += 1
            self.width = 20 + (self.max_size-20) * self.time / self.max_time
            self.height = self.width
            if self.time >= self.max_time:
                self.state = "ready"

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            if self.is_on_screen(x_offset, y_offset):
                i = len(self.colors) * self.time // (self.max_time+1)
                size = self.width / 20
                pen.shapesize(size, size, None)
                pen.goto(self.x - x_offset, self.y - y_offset)
                pen.shape(self.shape)
                pen.color(self.colors[i])
                pen.stamp()

                pen.shapesize(1.0, 1.0, None)


class BombExplosion(Explosion):
    def __init__(self):
        Explosion.__init__(self, 0, 0)
        self.max_size = 200.0
        self.state = "ready"

class Enemy(Sprite):
    count = 0

    def __init__(self, x, y, dx, dy):
        self.type = random.choice(["hunter", "mine", "surveillance"])
        if self.type == "hunter":
            Sprite.__init__(self, x, y, "hunter.gif", "red", dx, dy)
            self.score = 10
        elif self.type == "mine":
            Sprite.__init__(self, x, y, "mine.gif", "orange", dx, dy)
            self.score = 5
        else:
            Sprite.__init__(self, x, y, "surveillance.gif", "pink", dx, dy)
            self.score = 5

        self.max_health = 20
        self.health = self.max_health

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_check()

            # Check health
            if self.health <= 0:
                self.reset()

            # Code for different types
            if self.type == "hunter":
                if random.random() < 0.75:
                    if self.x < player.x and player.x - self.x < 200:
                        self.dx += 0.05
                    elif self.x > player.x and self.x - player.x < 200:
                        self.dx -= 0.05
                    if self.y < player.y and player.y - self.y < 200:
                        self.dy += 0.05
                    elif self.y > player.y and self.y - player.y < 200:
                        self.dy -= 0.05

            elif self.type == "mine":
                self.dx = 0
                self.dy = 0

            elif self.type == "surveillance":
                if self.x < player.x and player.x - self.x < 100:
                    self.dx -= 0.05
                elif self.x > player.x and self.x - player.x < 100:
                    self.dx += 0.05
                if self.y < player.y and player.y - self.y < 100:
                    self.dy -= 0.05
                elif self.y > player.y and self.y - player.y < 100:
                    self.dy += 0.05

            # Set max speed
            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx

            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy

    def reset(self):
        global high_score
        self.state = "inactive"
        Enemy.count -= 1
        self.explode()
        player.score += self.score
        if player.score > high_score:
            high_score = player.score
            hs_file = open("highscore.txt", "w")
            hs_file.write(str(high_score))
            hs_file.close()


class Powerup(Sprite):
    def __init__(self, x, y, shape, color, type, dx, dy):
        Sprite.__init__(self, x, y, shape, color, dx, dy)
        self.type = type

    def reset(self):
        winsound.PlaySound("powerup.wav", winsound.SND_ASYNC)
        if self.type == "multishot":
            player.multishot += 20
            if player.multishot > 50:
                player.multishot = 50
        elif self.type == "heal":
            player.health += 50
            if player.health > 100:
                player.health = 100
        else:  # bomb
            player.bombs += 1
            if player.bombs > 1:
                player.bombs = 1

        self.x = random.randint(-game.width / 2, game.width / 2)
        self.y = random.randint(-game.height / 2, game.height / 2)


class Camera():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y


class Radar():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.range = 1000

    def render(self, pen, sprites):

        # Draw radar circle
        pen.color("white")
        pen.setheading(90)
        pen.goto(self.x + self.radius, self.y)
        pen.pendown()
        pen.circle(self.radius)
        pen.penup()

        # Draw sprites
        for sprite in sprites:
            if sprite.state == "active":

                # Make sure the sprite is close to the player
                distance = ((player.x - sprite.x) ** 2 + (player.y - sprite.y) ** 2) ** 0.5
                if distance < self.range:
                    radar_x = self.x + (sprite.x - player.x) * (self.radius/self.range)
                    radar_y = self.y + (sprite.y - player.y) * (self.radius/self.range)
                    pen.goto(radar_x, radar_y)
                    pen.color(sprite.color)
                    pen.shape("circle")
                    pen.shapesize(0.1, 0.1, None)
                    pen.stamp()


# Create game object
game = Game(2000, 2000)

# Create the radar object
radar = Radar(INFO_CENTER, -SCREEN_HEIGHT / 2 + 100, 90)

# Create player sprite
player = Player()

# Create camera
camera = Camera(player.x + CAMERA_OFFSET, player.y)

# Create missile objects
missiles = []
for _ in range(3):
    missiles.append(Missile())

enemy_missiles = []
for _ in range(3):
    enemy_missiles.append(EnemyMissile())

# Create bomb object
bomb = Bomb()
bomb_explosion = BombExplosion()

explosions = []

# Sprites list
sprites = []

# Setup the level
game.start_level()

# Keyboard bindings
wn.listen()
wn.onkeypress(player.rotate_left, "Left")
wn.onkeypress(player.rotate_right, "Right")

wn.onkeyrelease(player.stop_rotation, "Left")
wn.onkeyrelease(player.stop_rotation, "Right")

wn.onkeypress(player.accelerate, "Up")
wn.onkeyrelease(player.decelerate, "Up")

wn.onkeypress(player.fire, "space")
wn.onkeypress(player.drop_bomb, "Down")

wn.onkeypress(game.start, "s")
wn.onkeypress(game.start, "S")

wn.onkeypress(game.print_frame_time_stats, "f")

# Main Loop
game_over = False
while not game_over:
    # Splash
    if game.state == "splash":
        wn.update()

    elif game.state == "playing":
        # Main Game
        # Clear screen
        pen.clear()

        # Render background
        pen.goto(-camera.x, -camera.y)
        pen.shape("background.gif")
        pen.stamp()

        # Do game stuff
        # Update sprites
        for sprite in sprites:
            sprite.update()

        # Update explosions
        for explosion in explosions:
            explosion.update()
        bomb_explosion.update()

        # Fire enemy missiles
        for sprite in sprites:
            if abs(player.x - sprite.x) < COLLISION_CHECK_RANGE and \
                    abs(player.y - sprite.y) < COLLISION_CHECK_RANGE:
                if isinstance(sprite, Enemy) and sprite.state == "active":
                    for enemy_missile in enemy_missiles:
                        if enemy_missile.state == "ready" and random.random() < 0.01:
                            # Fire the missile
                            heading = math.atan2(player.y - sprite.y, player.x - sprite.x)
                            heading = heading * (180 / 3.14159)
                            enemy_missile.fire(sprite.x, sprite.y, heading, sprite.dx, sprite.dy)
                            break

                    # Check for collisions
                    if player.is_collision(sprite):
                        sprite.health -= 10
                        player.health -= 10
                        player.bounce(sprite)

                    for missile in missiles:
                        if missile.state == "active" and missile.is_collision(sprite):
                            sprite.health -= 10
                            missile.reset()

                    if bomb.state == "active" and bomb.is_collision(sprite):
                        bomb.fuse = 0

                    if bomb_explosion.state == "active" and bomb_explosion.is_collision(sprite):
                        sprite.health -= 10

                if isinstance(sprite, Powerup):
                    if player.is_collision(sprite):
                        sprite.reset()
                    else:
                        for missile in missiles:
                            if missile.state == "active" and missile.is_collision(sprite):
                                sprite.reset()
                                missile.reset()

                # Enemy Missile Collisions with Player
                if isinstance(sprite, EnemyMissile):
                    if sprite.state == "active" and sprite.is_collision(player):
                        sprite.reset()
                        player.health -= 10

        if bomb_explosion.state == "active" and bomb_explosion.is_collision(player):
            player.health -= 10

        # Update the camera
        camera.update(player.x + CAMERA_OFFSET, player.y)

        # Render sprites
        for sprite in sprites:
            sprite.render(pen, camera.x, camera.y)

        # Render explosions
        for explosion in explosions:
            explosion.render(pen, camera.x, camera.y)
        bomb_explosion.render(pen, camera.x, camera.y)

        game.render_border(pen, camera.x, camera.y)

        # Check for end of level
        if Enemy.count == 0:
            game.level += 1
            game.start_level()

        # Draw text
        game.render_info(pen, player.score, high_score, Enemy.count)

        # Render the radar
        radar.render(pen, sprites)

        game.fps_delay()

        # Update the screen
        wn.update()

character_pen.scale = 3.0
character_pen.draw_string(pen, "GAME OVER", 0, 0)
wn.mainloop()

