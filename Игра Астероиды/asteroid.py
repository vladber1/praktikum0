from entities import MovingEntity


class Asteroid(MovingEntity):
    def __init__(self, canvas, x, y, angle, speed, size, game, img_name):
        super().__init__(canvas, x, y, angle, speed, size, game, img_name=img_name)

    def draw(self, x, y):
        return self.canvas.create_image(self.x, self.y, image=self.image)
