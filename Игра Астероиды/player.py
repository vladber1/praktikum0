from entities import MovingEntity
from settings import *
from rocket import Rocket
from PIL import Image, ImageTk
import math


class Player(MovingEntity):
    def __init__(self, canvas, x, y, angle, speed, size, game, img_name, moving_img_name):
        self.isMoving = False

        self.rockets = set()

        self.dx = 0
        self.dy = 0

        self.moving_img_name = moving_img_name

        super().__init__(canvas, x, y, angle, speed, size, game, img_name=img_name)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if abs(self.dx) < self.speed / 5 and abs(self.dy) < self.speed / 5:
            self.isMoving = False
        else:
            self.isMoving = True

        self.canvas.move(self.id, self.dx, self.dy)

        self.dx *= (1 - RESISTANCE)
        self.dy *= (1 - RESISTANCE)

    def move_forward(self):
        self.dx += math.cos(math.radians(self.angle)) * self.speed
        self.dy += -math.sin(math.radians(self.angle)) * self.speed

    def update(self, toroidal=False, always_moving=True):
        if self.x < 0:
            self.x += WIDTH
            self.canvas.move(self.id, WIDTH, 0)
        elif self.x > WIDTH - 10:
            self.x -= WIDTH
            self.canvas.move(self.id, -WIDTH, 0)
        elif self.y < 0:
            self.y += HEIGHT
            self.canvas.move(self.id, 0, HEIGHT)
        elif self.y > HEIGHT - 10:
            self.y -= HEIGHT
            self.canvas.move(self.id, 0, -HEIGHT)

        self.redraw()

        destroyed = []
        coords = self.canvas.find_overlapping(self.x, self.y, self.x + self.size[0] / 3, self.y + self.size[1] / 3)

        for coord in coords:
            if (coord != self.id and
                    coord not in self.game.untouchables and
                    coord not in set([rocket.id for rocket in self.rockets])):
                self.canvas.delete(coord)
                destroyed.append(coord)

                self.x = WIDTH // 2
                self.y = HEIGHT // 2

                self.redraw()

                self.game.lower_lives()
                break

        self.move()

        return destroyed

    def rotate(self, right=True):
        if right:
            self.angle -= 10
        else:
            self.angle += 10
        self.angle %= 360
        self.rotate_image()

    def rotate_image(self):
        image = Image.open(self.img_name)
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate(self.angle))
        self.redraw()

    def create_image(self, img_name):
        image = Image.open(self.game.get_path(img_name))
        image = image.resize(self.size)
        self.image = ImageTk.PhotoImage(image.rotate(self.angle))
        return self.canvas.create_image(self.x, self.y, image=self.image)

    def redraw(self):
        self.canvas.delete(self.id)
        self.id = self.draw(self.x, self.y)

    def draw(self, x, y):
        if self.isMoving:
            return self.create_image(self.moving_img_name)
        else:
            return self.create_image(self.img_name)

    def fire(self):
        dx = math.cos(math.radians(self.angle)) * 50
        dy = -math.sin(math.radians(self.angle)) * 50

        self.rockets.add(Rocket(self.canvas,
                                self.x + dx, self.y + dy,
                                self.angle, ROCKET_SPEED,
                                (ROCKET_SIZE, ROCKET_SIZE), self.game,
                                img_name=self.game.get_path(self.game.sprites['rocket'])))
