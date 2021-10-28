import pathlib
from pathlib import Path

home = Path.home()
assests: Path = Path(__file__).parent / 'assets'

PLAY_GAME = 0
GAME_OVER = 1

SCREEN_HEIGHT = 960
SCREEN_WIDTH = 960
SCREEN_TITLE = "battle of tanks"


tank_inventory = 4
tank2_inventory = 2

missle_tankp1_speed = 6
missle_tankP2_speed = 2


angle_tankP1_speed = 2
angle_tankP2_speed = 4

#health bar
tank_health = 300
HP_Y_OFFSET = 40
HP_X_OFFSET = 10
HP_HEIGHT = 30
HP_PADDING = 5
HP_WIDTH = 300
HP_X = HP_WIDTH

TANK1_HP = 100
TANK2_HP = 100

sprite_scaling_missles = 0.8
MISSLE_X_SCALE = 7
MISSLE_Y_SCALE = 7

sprite_scaling_player = 0.8
sprite_scaling_bonus = 0.4
sprite_scaling_random_bomb = 0.4

VERTICAL_MARGIN = 15
RIGHT_BORDER = SCREEN_WIDTH - VERTICAL_MARGIN
LEFT_BORDER = VERTICAL_MARGIN


HEALTH_BONUS_SPRITE = ('Assets/Bonus_Icon.png')
nuke_bonus = 80

X_CONSTANT = 860
Y_CONSTANT = 540


#8 sounds here
vicory_sound = ('Assets/sounds/you_win.ogg')
gameOver_sound = ('Assets/sounds/gameover.wav')

tankP1_shoot = ('Assets/Tank1/sounds/shoot.wav')
tankP2_shoot = ('Assets/Tank2/sounds/shoot.wav')

tankP1_DEAD = ('Assets/Tank1/sounds/gotgot.wav')
tankP2_DEAD = ('Assets/Tank2/sounds/gotgot.wav')

wall_destroyed_sound = ("Assets/sounds/Explosion+7.wav")

nuke_sound = ('Assets/sounds/power_up.ogg')

default_volume = 0.2

