import random
import time
import tkinter
from tkinter import Tk, Canvas, font
import os
from pathlib import Path
from entities import *
from player import Player
from asteroid import Asteroid


class Game:
    def __init__(self):
        self.score = 0
        self.lives = LIVES

        self.window = Tk()
        self.window.title('Астероиды')

        self.state = 'start'

        self.sprites = SPRITES_PATH

        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.bg = StaticEntity(self.canvas,
                               0, 0,
                               (WIDTH, HEIGHT), self,
                               img_name=self.get_path(self.sprites['background']), anchor=tkinter.NW)

        self.logo = StaticEntity(self.canvas,
                                 WIDTH // 2, HEIGHT // 2,
                                 (WIDTH // 4, HEIGHT // 4), self,
                                 img_name=self.get_path(self.sprites['logo']), tag='startTag', anchor=tkinter.CENTER)

        self.canvas.tag_bind('startTag', '<ButtonPress-1>', lambda ev: self.on_start_click(ev))

        self.font = font.Font(family='Arial',
                              size=FONT_SIZE, weight='bold')

        self.score_text = StaticEntity(self.canvas,
                                       50, 50,
                                       anchor=tkinter.NW,
                                       text=f'Очки: {self.score}',
                                       color="white",
                                       font_obj=self.font,
                                       game=self,
                                       size=None)

        self.lives_text = StaticEntity(self.canvas,
                                       WIDTH - 50, 50,
                                       anchor=tkinter.NE,
                                       text=f'Жизни: {self.lives}',
                                       color="white",
                                       font_obj=self.font,
                                       game=self,
                                       size=None)

        self.canvas.tag_raise(self.score_text.id)
        self.canvas.tag_raise(self.lives_text.id)
        self.canvas.tag_lower(self.bg.id)

        self.restart()

        self.ship = None
        self.asteroids = None
        self.explosions = None

        self.untouchables = {self.score_text.id, self.lives_text.id, self.bg.id, self.logo.id}

    def on_start_click(self, event):
        self.state = 'play'
        self.canvas.itemconfig(self.logo.id, state='hidden')

    def restart(self):
        self.state = 'start'
        self.lives = LIVES
        self.score = 0
        self.canvas.itemconfig(self.logo.id, state='normal')
        self.score_text.change_text(f'Очки: {self.score}')
        self.lives_text.change_text(f'Жизни: {self.lives}')
        self.canvas.tag_raise(self.logo.id)

    def game_loop(self):
        while True:
            if self.state == 'start':
                self.start_screen()
            else:
                self.start_game()

    def start_screen(self):
        self.asteroids = set([Asteroid(self.canvas,
                                       random.randint(0, WIDTH), random.randint(0, HEIGHT),
                                       180, BG_ASTEROIDS_SPEED,
                                       (BG_ASTEROIDS_SIZE, BG_ASTEROIDS_SIZE), self,
                                       img_name=self.get_path(self.sprites['asteroid'])) for _ in range(15)])
        while self.state == 'start':
            for asteroid in self.asteroids:
                asteroid.update(toroidal=True)
            self.canvas.tag_raise(self.logo.id)
            self.canvas.tag_raise(self.score_text.id)
            self.canvas.tag_raise(self.lives_text.id)
            self.canvas.update()

        for asteroid in self.asteroids:
            self.canvas.delete(asteroid.id)

        self.asteroids.clear()

    def start_game(self):
        self.ship = Player(self.canvas,
                           WIDTH // 2, HEIGHT // 2,
                           90, PLAYER_SPEED,
                           (PLAYER_SIZE, PLAYER_SIZE), self,
                           img_name=self.get_path(self.sprites['ship']),
                           moving_img_name=self.get_path(self.sprites['ship_charge']))

        self.window.bind('<Left>', lambda event: self.ship.rotate(right=False))
        self.window.bind('<Right>', lambda event: self.ship.rotate())
        self.window.bind('<Up>', lambda event: self.ship.move_forward())
        self.window.bind('<space>', lambda event: self.ship.fire())
        self.window.bind('<Escape>', lambda event: self.restart())

        self.asteroids = set([Asteroid(self.canvas,
                                       random.randint(0, WIDTH), random.randint(0, HEIGHT),
                                       random.randint(0, 360), ASTEROIDS_SPEED,
                                       (ASTEROIDS_SIZE, ASTEROIDS_SIZE), self,
                                       img_name=self.get_path(self.sprites['asteroid']))
                              for _ in range(START_COUNT_OF_ASTEROIDS)])

        self.explosions = set()

        start_time = time.time()

        while self.state == 'play':
            deltaTime = time.time() - start_time

            if deltaTime > 3:
                for _ in range(3):
                    self.asteroids.add(Asteroid(self.canvas,
                                                random.randint(0, WIDTH), random.randint(0, HEIGHT),
                                                random.randint(0, 360), ASTEROIDS_SPEED,
                                                (ASTEROIDS_SIZE, ASTEROIDS_SIZE), self,
                                                img_name=self.get_path(self.sprites['asteroid'])))
                start_time = time.time()

            rockets = set()
            destroyed_asteroids = set()
            explosions = set()

            for rocket in self.ship.rockets:
                for asteroid in rocket.update():
                    destroyed_asteroids.add(asteroid)
                if rocket.isAlive:
                    rockets.add(rocket)
            self.ship.rockets = rockets

            for asteroid in self.ship.update():
                destroyed_asteroids.add(asteroid)

            current_asteroids = self.asteroids.copy()

            self.asteroids = set()

            for asteroid in current_asteroids:
                asteroid.update(toroidal=True)
                if asteroid.id not in destroyed_asteroids:
                    self.asteroids.add(asteroid)

            self.canvas.tag_raise(self.score_text.id)
            self.canvas.tag_raise(self.lives_text.id)
            self.canvas.update()

        for asteroid in self.asteroids:
            self.canvas.delete(asteroid.id)

        self.asteroids.clear()

        self.canvas.delete(self.ship.id)

        for rocket in self.ship.rockets:
            self.canvas.delete(rocket.id)

        self.ship.rockets.clear()
        self.ship = None

    def up_score(self):
        self.score += 1
        self.score_text.change_text(f'Очки: {self.score}')

    def lower_lives(self):
        self.lives -= 1
        self.lives_text.change_text(f'Жизни: {self.lives}')
        if self.lives <= 0:
            self.restart()

    def get_path(self, file_path):
        return os.path.join(os.path.dirname(Path(__file__).absolute()), file_path)


def main():
    game = Game()
    game.game_loop()


if __name__ == "__main__":
    main()
