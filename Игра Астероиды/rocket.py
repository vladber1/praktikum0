from entities import MovingEntity
from settings import *
import time
from PIL import Image, ImageTk


class Rocket(MovingEntity):
    def __init__(self, canvas, x, y, angle, speed, size, game, img_name):
        super().__init__(canvas, x, y, angle, speed, size, game, img_name=img_name)

        self.live_timer = 0.0
        self.time_for_live = TIME_FOR_LIVE

        image = Image.open(self.img_name)
        image = image.resize(self.size)

        self.image = ImageTk.PhotoImage(image.rotate(self.angle))

        self.redraw()

    def rotate(self):
        self.rotate_image()

    def rotate_image(self):
        image = Image.open(self.img_name)
        image = image.resize(self.size)

        self.image = ImageTk.PhotoImage(image.rotate(self.angle))

        self.redraw()

    def move(self):
        destroyed = []

        super().move()

        coords = self.canvas.find_overlapping(self.x, self.y,
                                              self.x + self.size[0] - 10, self.y + self.size[1] - 5)

        for coord in coords:
            if (coord != self.id and
                    coord not in self.game.untouchables
                    and coord != self.game.ship.id
                    and coord not in set([rocket.id for rocket in self.game.ship.rockets])):
                self.canvas.delete(coord)

                destroyed.append(coord)

                self.canvas.delete(self.id)
                self.isAlive = False
                self.game.up_score()

                break

        if self.live_timer >= self.time_for_live:
            self.canvas.delete(self.id)
            self.isAlive = False
        else:
            self.live_timer += time.time() / 100_000_000

        return destroyed

    def draw(self, x, y):
        return self.canvas.create_image(self.x, self.y, image=self.image)
