import arcade
import pathlib


PLAY_GAME = 0
GAME_OVER = 1
SCREEN_HEIGHT = 960
SCREEN_WIDTH = 960

tank_inventory = 4
tank2_inventory = 2

missle_tankP2_speed=4
missle_tankp1_speed = 2

sprite_scaling_missles = 0.8


class TiledWindow (arcade.Window):
    def __init__(self):
        super().__init__(960, 960, "Initial Tiled Map Super Simple Example")
        self.map_location = pathlib.Path.cwd()/'Assets/maps/mpa1tank.json'
        self.current_scene = None

        self.mapscene1 = None
        self.mapscene2 = None

        self.wall_list=None
        self.wall_list2 = None

        self.player: arcade.Sprite = None
        self.player2: arcade.Sprite = None

        self.simple_physics = None

        self.player_list = None
        self.player2_list = None

        self.move_speed = 2
        self.move2_speed = 4

        self.prev_scene: arcade.Scene = None

        self.tank_missles = None
        self.tankP2_missles = None

        self.game_state = PLAY_GAME



    #def setup levels
    #def make_walls(self, ):

    def setup(self):
        sample_map = arcade.tilemap.load_tilemap(self.map_location)
        self.mapscene1 = arcade.Scene.from_tilemap(sample_map)
        self.wall_list = sample_map.sprite_lists["wallLayer"]
        map2 = arcade.tilemap.load_tilemap(pathlib.Path.cwd()/'Assets/maps/map2.json')
        self.mapscene2 = arcade.Scene.from_tilemap(map2)
        self.wall_list2 = map2.sprite_lists['wallLayer']

        self.player = arcade.Sprite(pathlib.Path.cwd() / 'Assets/Tank1/Tank/Hull_04.png')
        self.player2 = arcade.Sprite(pathlib.Path.cwd()/ 'Assets/Tank2/Tank/Hull_06.png')

        self.player.center_x = 96
        self.player.center_y = 224
        self.player2.center_x = 8
        self.player2.center_y = 24

        self.player_list = arcade.SpriteList()
        self.player2_list = arcade.SpriteList()

        self.player2_list.append(self.player2)
        self.player_list.append(self.player)

        self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)
        self.current_scene = self.mapscene1


        self.tank_missles = arcade.SpriteList()
        self.tankP2_missles = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()

        self.current_scene.draw()

        self.tank_missles.draw()
        self.tankP2_missles.draw()

        self.player_list.draw()
        self.player2_list.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if self.game_state == GAME_OVER:
            return

        self.player.center_x = x
        self.player2.center_x = x

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        #prevents spamming
        if len(self.tank_missles) < tank_inventory:
            #arcade.play_sound(self. sSOUND)

            #creates missle
            missle = arcade.Sprite("Assets/Tank1/Tank/bulletRedSilver_outline.png", sprite_scaling_missles)

            missle.angle = 90

            missle.change_y = missle_tankp1_speed

            missle.center_x = self.player.center_x
            missle.bottom = self.player.top

            self.tank_missles.append(missle)

        if len(self.tankP2_missles) < tank2_inventory:
            missle2 = arcade.Sprite('Assets/Tank2/Tank/bulletYellow_outline.png', sprite_scaling_missles)

            missle2.angle = 90
            missle2.change_y = missle_tankP2_speed
            missle2.center_x = self.player2.center_x
            missle2.bottom = self.player2.top

            self.tankP2_missles.append(missle2)


    def missles_fly(self):
        self.tank_missles.update()
        self.tankP2_missles.update()

        for missle in self.tank_missles:

            hit_list = arcade.check_for_collision_with_list(missle, self.wall_list)
            if len(hit_list) > 0:
                missle.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            hit_list = arcade.check_for_collision_with_list(missle, self.player_list)

            if len(hit_list) > 0:
                missle.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

            #removes missle if goes off screen
            if missle.bottom > SCREEN_HEIGHT:
                missle.remove_from_sprite_lists()


    def on_update(self, delta_time: float):
        if self.game_state == GAME_OVER:
            return

        self.missles_fly()
        self.simple_physics.update()


    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y += self.move_speed
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y -= self.move_speed
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x -= self.move_speed
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x += self.move_speed
        if self.player.center_x < -10: # if the player is on map1 and heading off the map
            self.current_scene = self.mapscene2
            self.player.center_x = self.width-self.player.width/2
            self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list2)
        elif self.player.center_x > self.width+10: # if we are on map2 and headed off the scene
            self.current_scene = self.mapscene1
            self.player.center_x = self.player.width/2
            self.simple_physics = arcade.PhysicsEngineSimple(self.player, self.wall_list)



    def on_key_release(self, key: int, modifiers: int):
        if self.player.change_y <0 and (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y =0
        if self.player.change_y >0 and (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y =0
        if self.player.change_x <0 and (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x =0
        if self.player.change_x >0 and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x =0
