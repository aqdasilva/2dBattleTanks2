from random import randint
import arcade
import pathlib


import constants
from constants import missle_tankp1_speed, missle_tankP2_speed, PLAY_GAME, \
    sprite_scaling_player, HP_PADDING, HP_X, HP_WIDTH, HP_HEIGHT, angle_tankP1_speed, \
    sprite_scaling_missles, angle_tankP2_speed, GAME_OVER, SCREEN_HEIGHT


class TiledWindow(arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Battle of the Tanks")
        self.map_location = pathlib.Path.cwd() / f'Assets/maps/map1tank.json'
        self.current_scene = None

        self.mapscene1 = None
        self.mapscene2 = None
        self.mapscene3 = None

        self.wall_list = None
        self.wall_list2 = None
        self.wall_list3 = None

        self.power_list = None

        self.simple_physics = None
        self.simple_physics2 = None

        # sets up player info
        self.player: arcade.Sprite = None
        self.player2: arcade.Sprite = None
        self.power: arcade.Sprite = None

        self.simple_physics = None
        self.simple_physics2 = None

        self.player_list = None
        self.player2_list = None

        self.player_shoot_speed = missle_tankp1_speed
        self.player2_shoot_speed = missle_tankP2_speed

        self.move_speed = 2
        self.move2_speed = 4

        self.prev_scene: arcade.Scene = None

        self.tank_missles_list = None
        self.tankP2_missles = None

        self.tank1_hp = 200
        self.tank2_hp = 200

        # next level after player dies
        self.level = 1
        self.score = 0

        # 8 sounds here
        self.vicory_sound = arcade.load_sound('Assets/sounds/you_win.ogg')
        self.gameOver_sound = arcade.load_sound('Assets/sounds/gameover.wav')

        self.tankP1_shoot = arcade.load_sound('Assets/Tank1/sounds/shoot.wav')
        self.tankP2_shoot = arcade.load_sound('Assets/Tank2/sounds/shoot.wav')

        self.tankP1_DEAD = arcade.load_sound('Assets/Tank1/sounds/gotgot.wav')
        self.tankP2_DEAD = arcade.load_sound('Assets/Tank2/sounds/gotgot.wav')

        self.wall_destroyed_sound = arcade.load_sound("Assets/sounds/Explosion+7.wav")
        self.wall_destroyed_sound2 = arcade.load_sound("Assets/sounds/Explosion+7.wav")

        self.nuke_sound = arcade.load_sound('Assets/sounds/power_up.ogg')

        self.game_state = PLAY_GAME

    def setup(self):
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene1 = arcade.Scene.from_tilemap(sample_map)
        self.wall_list = sample_map.sprite_lists["wallLayer"]
        self.ice_layer = sample_map.sprite_lists["ice"]
        self.nuke_bonus = sample_map.sprite_lists["nuke"]


        map2 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / f'Assets/maps/map2.json')
        self.mapscene2 = arcade.Scene.from_tilemap(map2)
        self.wall_list2 = map2.sprite_lists['brick']


        map3 = arcade.tilemap.load_tilemap(pathlib.Path.cwd() / 'Assets/maps/map3.json')
        self.mapscene3 = arcade.Scene.from_tilemap(map3)
        self.wall_list3 = map3.sprite_lists['wallLayer']


        self.power = arcade.Sprite(pathlib.Path.cwd() / 'Assets/Bonus_Icon.png')
        self.player = arcade.Sprite(pathlib.Path.cwd() / 'Assets/Tank1/Tank/tank_bigRed.png', sprite_scaling_player)
        self.player2 = arcade.Sprite(pathlib.Path.cwd() / 'Assets/Tank2/Tank/tank_blue.png', sprite_scaling_player)

        self.player.center_x = 100
        self.player.center_y = 280

        self.player2.center_x = 900
        self.player2.center_y = 620

        self.shoot_tank1_direction = "right"
        self.shoot_tank2_direction = "left"

        self.player_list = arcade.SpriteList()
        self.player2_list = arcade.SpriteList()

        self.player2_list.append(self.player2)
        self.player_list.append(self.player)

        self.power_list = arcade.SpriteList()
        self.power_list.append(self.power)

        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.simple_physics2 = arcade.PhysicsEngineSimple(self.player2, self.wall_list)
        self.simple_physics3 = arcade.PhysicsEngineSimple(self.power, self.wall_list)

        self.current_scene = self.mapscene1

        self.missle_P1_list = arcade.SpriteList()
        self.missle_P2_list = arcade.SpriteList()

        self.score = 0
        self.speed = 0

        self.scale = constants.sprite_scaling_player/ 2
        self.power.center_y = randint(25, constants.Y_CONSTANT - 25)
        self.power.center_x = randint(25, constants.X_CONSTANT - 25)

    def on_draw(self):
        #draws up sprites and scenes
        arcade.start_render()
        self.current_scene.draw()

        self.player_list.draw()
        self.player2_list.draw()

        self.missle_P1_list.draw()
        self.missle_P2_list.draw()
        self.nuke_bonus.draw()


        # draws hp
        arcade.draw_text(f"Player 1 ", 150, 10, arcade.color.NEON_GREEN, 14, anchor_x="right")
        arcade.draw_text(f"Player 2 ", 850, 10, arcade.color.NEON_GREEN, 14, anchor_x="left")

        arcade.draw_rectangle_filled(center_x=HP_X, center_y=20,
                                     width=((HP_WIDTH - HP_PADDING) * constants.TANK1_HP / 100) // 1,
                                     height=HP_HEIGHT - HP_PADDING, color=arcade.color.GREEN)
        arcade.draw_rectangle_filled(center_x=700, center_y=20,
                                     width=((HP_WIDTH - HP_PADDING) * constants.TANK2_HP / 100) // 1,
                                     height=HP_HEIGHT - HP_PADDING, color=arcade.color.GREEN)

    def on_key_press(self, key: int, modifiers: int):
        # tank 1 controls
        if key == arcade.key.W:
            self.player.change_y += self.move_speed
            self.shoot_tank1_direction = "up"
        elif key == arcade.key.S:
            self.player.change_y -= self.move_speed
            self.shoot_tank1_direction = "down"
        elif key == arcade.key.A:
            self.player.change_x -= self.move_speed
            self.shoot_tank1_direction = "left"
        elif key == arcade.key.D:
            self.player.change_x += self.move_speed
            self.shoot_tank1_direction = "right"

        # rotates tank
        if key == arcade.key.Q:
            self.player.change_angle = angle_tankP1_speed
            self.shoot_tank1_direction = "left"
        if key == arcade.key.E:
            self.player.change_angle = -angle_tankP1_speed
            self.shoot_tank1_direction = "right"

        # rotates tank
        if key == arcade.key.Q:
            self.player.change_angle = angle_tankP1_speed
            self.shoot_tank1_direction = "left"
        if key == arcade.key.E:
            self.player.change_angle = -angle_tankP1_speed
            self.shoot_tank1_direction = "right"

        # creates missle
        if key == arcade.key.SPACE:
            arcade.play_sound(self.tankP1_shoot)
            missle = arcade.Sprite("Assets/Tank1/Tank/bulletRedSilver_outline.png", sprite_scaling_missles)
            missle.center_x = self.player.center_x
            missle.center_y = self.player.center_y - 10
            missle.bottom = self.player.top

            #controls direction the missle goes by the way the tank is facing
            if self.shoot_tank1_direction == "left":
                missle.change_x = -missle_tankp1_speed
            elif self.shoot_tank1_direction == "right":
                missle.change_x = missle_tankp1_speed
            elif self.shoot_tank1_direction == "up":
                missle.change_y = missle_tankp1_speed
            elif self.shoot_tank1_direction == "down":
                missle.change_y = -missle_tankp1_speed
                missle.angle = 180
            self.missle_P1_list.append(missle)


        # tank 2 fire button
        if key == arcade.key.RSHIFT:
            arcade.play_sound(self.tankP2_shoot)
            missle2 = arcade.Sprite("Assets/Tank2/Tank/bulletYellow_outline.png", sprite_scaling_missles)
            missle2.center_x = self.player2.center_x
            missle2.center_y = self.player2.center_y - 10
            missle2.bottom = self.player2.top
            missle2.change_y = missle_tankP2_speed
            if self.shoot_tank2_direction == "right":
                missle2.change_x = missle_tankP2_speed
            elif self.shoot_tank2_direction == "left":
                missle2.change_x = -missle_tankP2_speed
            elif self.shoot_tank2_direction == "up":
                missle2.change_y = missle_tankP2_speed
            elif self.shoot_tank2_direction == "down":
                missle2.change_y = -missle_tankP2_speed
                missle2.angle = 180
            self.missle_P2_list.append(missle2)

        # player2 controls
        elif key == arcade.key.I:
            self.player2.change_y += self.move2_speed
            self.shoot_tank2_direction = "up"
        elif key == arcade.key.K:
            self.player2.change_y -= self.move2_speed
            self.shoot_tank2_direction = "down"
        elif key == arcade.key.J:
            self.player2.change_x -= self.move2_speed
            self.shoot_tank2_direction = "left"
        elif key == arcade.key.L:
            self.player2.change_x += self.move2_speed
            self.shoot_tank2_direction = "right"

        # tank 2 rotation
        if key == arcade.key.U:
            self.player2.change_angle = angle_tankP2_speed
            self.shoot_tank2_direction = "left"
        elif key == arcade.key.O:
            self.player2.change_angle = -angle_tankP2_speed
            self.shoot_tank2_direction = "right"
            arcade.play_sound(self.tankP1_shoot)

    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y < 0 and (key == arcade.key.S):
            self.player.change_y = 0
        if self.player.change_y > 0 and (key == arcade.key.W):
            self.player.change_y = 0
        if self.player.change_x < 0 and (key == arcade.key.A):
            self.player.change_x = 0
        if self.player.change_x > 0 and (key == arcade.key.D):
            self.player.change_x = 0

        if self.player2.change_y < 0 and (key == arcade.key.K):
            self.player2.change_y = 0
        if self.player2.change_y > 0 and (key == arcade.key.I):
            self.player2.change_y = 0
        if self.player2.change_x < 0 and (key == arcade.key.J):
            self.player2.change_x = 0
        if self.player2.change_x > 0 and (key == arcade.key.L):
            self.player2.change_x = 0


        elif key == arcade.key.Q or key == arcade.key.E:
            self.player.change_angle = 0
        elif key == arcade.key.U or key == arcade.key.O:
            self.player2.change_angle = 0

    def spawnRandomPower(self):
        for nuke in self.power_list:
            hit_list = arcade.check_for_collision_with_list(nuke, self.player_list)
            nuke.remove_from_sprite_lists()
            self.tank1_hp += 500




    def missles_fly(self):
        self.missle_P1_list.update()
        self.missle_P2_list.update()

        for missle in self.missle_P1_list:
            hit_list = arcade.check_for_collision_with_list(missle, self.wall_list)
            if len(hit_list) > 0:
                missle.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                    arcade.play_sound(self.wall_destroyed_sound)
                continue

            sprites = arcade.check_for_collision_with_list(missle, self.player2_list)
            for player in sprites:
                missle.remove_from_sprite_lists()
                self.tank1_hp += -50
                if self.tank1_hp == 0:
                    print("Player 2 has merked you")


            hit_list = arcade.check_for_collision_with_list(missle, self.player2_list)
            if len(hit_list) > 0:
                missle.remove_from_sprite_lists()
                self.level += 1
                self.setup()
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.tankP1_DEAD)
                arcade.play_sound(self.gameOver_sound)

                self.current_scene = self.mapscene2
                self.player.center_x = 100
                self.player.center_y = 280
                self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)
                continue
                self.player2.center_x = 900
                self.player2.center_y = 620
                self.simple_physics2 = arcade.PhysicsEngineSimple(self.player2, self.wall_list2)


            # removes missle if goes off screen
            if missle.bottom > SCREEN_HEIGHT:
                missle.remove_from_sprite_lists()


        for missle in self.missle_P2_list:
            hit_list = arcade.check_for_collision_with_list(missle, self.wall_list)
            if len(hit_list) > 0:
                missle.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                    arcade.play_sound(self.wall_destroyed_sound2)
                continue

            hit_list = arcade.check_for_collision_with_list(missle, self.player_list)

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(self.tankP2_DEAD)
                arcade.play_sound(self.gameOver_sound)

                self.current_scene = self.mapscene2
                self.player2.center_x = 900
                self.player2.center_y = 620
                self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)
                continue
                self.player.center_x = 100
                self.player.center_y = 280
                self.simple_physics2 = arcade.PhysicsEngineSimple(self.player2, self.wall_list2)




            # removes missle if goes off screen
            if missle.bottom > SCREEN_HEIGHT:
                missle.remove_from_sprite_lists()

    def damage_tank(self, amount: int):
        self.tank_health -= amount

    def game_over(self):
        return self.tank_health <= 0

    def on_update(self, delta_time: float):
        if self.game_state == GAME_OVER:
            return

        self.spawnRandomPower()
        self.missles_fly()
        self.simple_physics.update()
        self.simple_physics2.update()
        self.simple_physics3.update()
