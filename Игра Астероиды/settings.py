""" window settings """
WIDTH = 1280
HEIGHT = 720
""" window settings """

""" player settings """
RESISTANCE = 0.05
LIVES = 3
PLAYER_SPEED = 2
PLAYER_SIZE = 75
""" player settings """

""" rocket settings """
ROCKET_SPEED = 5
ROCKET_SIZE = 40
TIME_FOR_LIVE = min(WIDTH, HEIGHT) / ROCKET_SPEED * 10
""" rocket settings """

""" asteroids settings """
ASTEROIDS_SPEED = 1
ASTEROIDS_SIZE = 75

START_COUNT_OF_ASTEROIDS = 5

BG_ASTEROIDS_SPEED = 3
BG_ASTEROIDS_SIZE = 75
""" asteroids settings """

""" sprites settings """
SPRITES_PATH = {'background': 'Resources/background.png',
                'logo': 'Resources/logo.png',
                'ship': 'Resources/ship.png',
                'asteroid': 'Resources/asteroid.png',
                'rocket': 'Resources/rocket.png',
                'ship_charge': 'Resources/ship_charge.png',
                'explosion': 'Resources/explosion/'}
""" sprites settings """

""" font settings """
FONT_SIZE = 18
""" font settings """
