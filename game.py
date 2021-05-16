import numpy as np
import colorama as col
import random
import time
import os

from screen import Screen
from boss import Boss, Bomb
from paddle import Paddle
from ball import Ball
from brick import Brick, ExplodingBrick, RainbowBrick
from khbit import KBHit
from powerup import (
    ExpandPaddle,
    ShrinkPaddle,
    PaddleGrab,
    BallMultiplier,
    ThruBall,
    FastBall,
    PaddleShoot,
    Bullet,
    # FireBall,
)

import config
import graphics
import utils


class Game:
    def __init__(self):
        col.init()
        print("\033[?25l\033[2J", end="")
        self._kb = KBHit()

        self._screen = Screen()
        utils.clear_screen()

        self._paddle = Paddle()
        self._boss = None

        x = random.randint(
            int(config.WIDTH / 2 - config.PADDLE_LEN / 2) + 1,
            int(config.WIDTH / 2 + config.PADDLE_LEN / 2) - 1,
        )

        position = np.array([x, config.HEIGHT - 3 - 1])

        velocity = np.array([0.0, 0.0])

        self._ball = Ball(position=position, velocity=velocity)
        # self._layouts = [
        #     config.LAYOUT_SMALL_RAIN.split("\n"),
        #     config.LAYOUT_SMALL.split("\n"),
        #     config.LAYOUT_BIG.split("\n"),
        #     config.LAYOUT_BONUS.split("\n"),
        # ]

        self._lives = 10
        self._level = 0
        self._score = 0
        self._timer = 0
        self._lasertimeleft = 0
        self._firerate = 0
        self._bombrate = 0
        self._maxheight = 0
        self._init_time = time.time()
        self._refresh_time = 0.05

        self._paddle_bounce_vel = np.array([0.0, 0.0])

        self._objects = {
            "paddle": [self._paddle],
            "ball": [self._ball],
            "brick": [],
            "powerup": [],
            "bullet": [],
            "boss": [],
            "bomb": [],
            "bossdef": [],
        }

        self._power_lookup = {
            "class_1": ShrinkPaddle,
            "class_2": ExpandPaddle,
            "class_3": BallMultiplier,
            "class_4": FastBall,
            "class_5": ThruBall,
            "class_6": PaddleGrab,
            "class_7": PaddleShoot,
            # "class_8": FireBall,
        }

        self._active_powers = []

        self._total_breakable_bricks = 0

        if config.WIDTH < 100:
            self._layouts = [
                config.LAYOUT_SMALL_RAIN.split("\n"),
                config.LAYOUT_SMALL.split("\n"),
            ]
        else:
            self._layouts = [
                config.LAYOUT_SMALL_RAIN.split("\n"),
                config.LAYOUT_SMALL.split("\n"),
                config.LAYOUT_BIG.split("\n"),
                config.LAYOUT_BONUS.split("\n"),
            ]

        # layout = config.LAYOUT_SMALL_RAIN.split("\n")

        # for i in range(len(layout)):
        #     for j in range(len(layout[i])):
        #         health = int(layout[i][j])
        #         if health != 4:
        #             self._total_breakable_bricks += 1
        #         position = np.array(
        #             [9 * j + (config.WIDTH - len(layout[i]) * 9) / 2, 5 + 2 * i]
        #         )
        #         self._maxheight = max(self._maxheight, 5 + 2 * i)
        #         if health <= 4:
        #             brick = Brick(health, position)
        #         elif health == 5:
        #             brick = ExplodingBrick(health, position)
        #         elif health == 6:
        #             brick = RainbowBrick(1, position)

        #         self._objects["brick"].append(brick)

        self._colliders = [
            ("ball", "paddle"),
            ("ball", "brick"),
            ("powerup", "paddle"),
            ("bullet", "brick"),
            ("bomb", "paddle"),
            ("ball", "boss"),
            ("bullet", "boss"),
            ("ball", "bossdef"),
        ]
        self.level(self._level)

    def level(self, index):
        self._paddle = Paddle()

        x = random.randint(
            int(config.WIDTH / 2 - config.PADDLE_LEN / 2) + 1,
            int(config.WIDTH / 2 + config.PADDLE_LEN / 2) - 1,
        )

        position = np.array([x, config.HEIGHT - 3 - 1])

        velocity = np.array([0.0, 0.0])

        self._ball = Ball(position=position, velocity=velocity)

        self._timer = 0
        self._firerate = 0
        self._lasertimeleft = 0
        self._bombrate = 0
        self._maxheight = 0

        self._paddle_bounce_vel = np.array([0.0, 0.0])

        self._objects = {
            "paddle": [self._paddle],
            "ball": [self._ball],
            "brick": [],
            "powerup": [],
            "bullet": [],
            "boss": [],
            "bomb": [],
            "bossdef": [],
        }

        self._active_powers = []
        self._total_breakable_bricks = 0

        layout = self._layouts[index]

        for i in range(len(layout)):
            for j in range(len(layout[i])):
                health = int(layout[i][j])
                if health != 4:
                    self._total_breakable_bricks += 1
                position = np.array(
                    [9 * j + (config.WIDTH - len(layout[i]) * 9) / 2, 5 + 2 * i]
                )
                self._maxheight = max(self._maxheight, 5 + 2 * i)
                if health <= 4:
                    brick = Brick(health, position)
                elif health == 5:
                    brick = ExplodingBrick(health, position)
                elif health == 6:
                    brick = RainbowBrick(1, position)

                self._objects["brick"].append(brick)

    def boss_level(self):
        self._paddle = Paddle()
        self._boss = Boss()

        x = random.randint(
            int(config.WIDTH / 2 - config.PADDLE_LEN / 2) + 1,
            int(config.WIDTH / 2 + config.PADDLE_LEN / 2) - 1,
        )

        position = np.array([x, config.HEIGHT - 3 - 1])

        velocity = np.array([0.0, 0.0])

        self._ball = Ball(position=position, velocity=velocity)

        self._timer = 0
        self._firerate = 0
        self._bombrate = 0
        self._lasertimeleft = 0
        self._maxheight = 0

        self._paddle_bounce_vel = np.array([0.0, 0.0])

        self._objects = {
            "paddle": [self._paddle],
            "ball": [self._ball],
            "brick": [],
            "powerup": [],
            "bullet": [],
            "boss": [self._boss],
            "bomb": [],
            "bossdef": [],
        }

        self._active_powers = []
        self._total_breakable_bricks = 0

        for i in range(9):
            position = np.array([config.WIDTH / 2 - 20 * (4.3 - i), 25 + (i % 2) * 5])
            self._maxheight = max(self._maxheight, 30)
            brick = Brick(4, position)
            self._objects["brick"].append(brick)

    def clear(self):
        self._screen.clear()
        utils.clear_screen()

    def start(self):
        while self._lives > 0:
            paddle_x, paddle_y = self._paddle.get_position()
            if self._paddle.get_health() == 0 or (
                self._boss and self._boss.get_health() == 0
            ):
                break
            if self._maxheight >= paddle_y:
                break
            if self._level < len(self._layouts):
                if self._total_breakable_bricks == 0:
                    self._level += 1
                    self.level(self._level)
            self._timer += 1
            start_time = time.perf_counter()
            self.clear()
            tmp_obj = {
                "paddle": [],
                "ball": [],
                "brick": [],
                "powerup": [],
                "bullet": [],
                "bomb": [],
                "boss": [],
                "bossdef": [],
            }

            if self._kb.kbhit():
                if self.manage_keys(self._kb.getch()):
                    break
            else:
                self._kb.clear()

            self.check_active_powers()

            if self._paddle.get_shoot():
                self._firerate += 1
                if self._firerate >= config.BULLET_INTERVAL:
                    self._firerate = 0
                    self.fire_bullets()

            if self._boss:
                self._bombrate += 1
                if self._bombrate >= config.BOMB_INTERVAL:
                    self._bombrate = 0
                    self.drop_bomb()

                if self._boss.get_health() <= 14:
                    if self._boss.get_defense() == 0:
                        self._boss.set_defense(1)
                        num_bricks = config.WIDTH // 9
                        margin = (config.WIDTH % 9) / 2
                        self._total_breakable_bricks += num_bricks
                        for i in range(num_bricks):
                            health = (i % 2) + 1
                            position = np.array([margin + 9 * i, 18])
                            self._maxheight = max(self._maxheight, 20)
                            brick = Brick(health, position)
                            tmp_obj["bossdef"].append(brick)

                if self._boss.get_health() <= 7:
                    if self._boss.get_defense() == 1:
                        self._boss.set_defense(2)
                        num_bricks = config.WIDTH // 9
                        margin = (config.WIDTH % 9) / 2
                        self._total_breakable_bricks += num_bricks
                        for i in range(num_bricks):
                            health = ((i + 1) % 2) + 1
                            position = np.array([margin + 9 * i, 13])
                            self._maxheight = max(self._maxheight, 20)
                            brick = Brick(health, position)
                            tmp_obj["bossdef"].append(brick)

            self.wall_collisions()
            self.check_collisions()

            for bricks in self._objects["brick"]:
                if bricks.get_type() == "r" and bricks.get_num_collisions() == 0:
                    health = bricks.get_health()
                    if health == 2:
                        new_health = 3
                    else:
                        new_health = (health + 1) % 3
                    bricks.set_health(new_health)

                    config_bg_color = "BRICK_BG_COL_" + str(new_health)
                    config_color = "BRICK_COL_" + str(new_health)
                    color_bg_string = getattr(config, config_bg_color)
                    color_string = getattr(config, config_color)
                    color = [[[color_bg_string, color_string]]]
                    bricks.set_color(color)

            for obj_type in self._objects:
                for obj in self._objects[obj_type]:
                    if obj.get_active():
                        if obj_type == "ball":
                            # obj.update_position(self._paddle)
                            obj.update_position()
                            x, y = obj.get_position()
                            h, w = obj.get_dimensions()

                            if y + h >= config.HEIGHT:
                                if (
                                    sum(
                                        list(
                                            map(
                                                lambda x: x.get_active(),
                                                self._objects["ball"],
                                            )
                                        )
                                    )
                                ) == 1:
                                    self._lives -= 1
                                    self._lasertimeleft = 0
                                    self._paddle.set_figure_unit("=")
                                    unit = self._paddle.get_figure_unit()
                                    figure = np.full((1, config.PADDLE_LEN), unit)
                                    self._paddle.set_figure(figure)
                                    paddle_x, paddle_y = self._paddle.get_position()
                                    paddle_h, paddle_w = self._paddle.get_dimensions()
                                    x = random.randint(
                                        int(paddle_x),
                                        int(paddle_x + paddle_w) - w,
                                    )
                                    obj.set_position([x, paddle_y - h - 1])
                                    obj.set_velocity([0.0, 0.0])
                                    obj.set_strong(False)
                                    # obj.set_fire(False)
                                    color = [[[config.BALL_BG_COL, config.BALL_COL]]]
                                    obj.set_color(color)
                                    self._paddle.set_sticky(False)
                                    self._paddle.set_shoot(False)
                                    self._paddle_bounce_vel = np.array([0.0, 0.0])
                                    self._active_powers = []
                                else:
                                    obj.set_active()

                        if obj_type == "powerup":
                            obj.update_position()
                            x, y = obj.get_position()
                            h, w = obj.get_dimensions()
                            if y + h >= config.HEIGHT:
                                obj.set_active()

                        if obj_type == "bullet":
                            obj.update_position()
                            x, y = obj.get_position()
                            if y <= 0:
                                obj.set_active()

                        if obj_type == "bomb":
                            obj.update_position()
                            x, y = obj.get_position()
                            h, w = obj.get_dimensions()
                            if y + h >= config.HEIGHT:
                                obj.set_active()

                        if obj.get_active():
                            self._screen.draw(obj)
                            tmp_obj[obj_type].append(obj)

            self._objects = tmp_obj
            self.show_score()
            self._screen.show()
            while time.perf_counter() - start_time < self._refresh_time:
                pass

    def fire_bullets(self):
        paddle_x, paddle_y = self._paddle.get_position()
        paddle_h, paddle_w = self._paddle.get_dimensions()
        left_bullet = Bullet(position=np.array([paddle_x, paddle_y]))
        right_bullet = Bullet(position=np.array([paddle_x + paddle_w, paddle_y]))
        self._objects["bullet"].append(left_bullet)
        self._objects["bullet"].append(right_bullet)

    def drop_bomb(self):
        boss_x, boss_y = self._boss.get_position()
        boss_h, boss_w = self._boss.get_dimensions()
        bomb = Bomb(position=np.array([boss_x + boss_w / 2, boss_y + boss_h]))
        self._objects["bomb"].append(bomb)

    def manage_keys(self, char):
        if char == config.QUIT_CHAR:
            return True

        if char == "h":
            if self._boss:
                self._boss.hit()

        if char == config.LEVEL_CHAR:
            self._level += 1
            if self._level == len(self._layouts) + 1:
                return True
            elif self._level == len(self._layouts):
                self.boss_level()
            else:
                self.level(self._level)

        if char == config.LAUNCH_CHAR:
            for bal in self._objects["ball"]:
                if np.array_equal(np.array([0.0, 0.0]), bal.get_velocity()):
                    if np.array_equal(np.array([0.0, 0.0]), self._paddle_bounce_vel):
                        paddlex, paddley = self._paddle.get_position()
                        paddleh, paddlew = self._paddle.get_dimensions()
                        ballx, bally = bal.get_position()
                        ballh, ballw = bal.get_dimensions()
                        ballspeedx = (ballx - (paddlex + paddlew / 2)) / paddlew
                        if ballspeedx == 0:
                            ballspeedx = config.BALL_SPEED_X
                        bal.set_velocity([ballspeedx, config.BALL_SPEED_Y])
                    else:
                        bal.set_velocity(self._paddle_bounce_vel)
                    self._paddle.set_space(True)

        if char == config.LEFT_CHAR or char == config.RIGHT_CHAR:
            self._paddle.move(char, self._objects["ball"], self._boss)

        return False

    def show_score(self):
        _t = time.time()
        if self._boss:
            # print(
            #     f"❤️ {int(self._lives): >5} | 🤑 {int(self._score): >5} | 🕒 {(_t - self._init_time): .2f} | 🧱 {int(self._total_breakable_bricks): >5} | 🏆 {int(self._level + 1): >5} | 👽 {int(self._boss.get_health()): >5} | ⚕️ {int(self._paddle.get_health()): >5} ",
            #     " " * 15,
            # )
            print(
                f"❤️ {int(self._lives): >5} | 🤑 {int(self._score): >5} | 🕒 {(_t - self._init_time): .2f} | 🧱 {int(self._total_breakable_bricks): >5} | 🏆 {int(self._level + 1): >5} | 👽 ",
                "*" * self._boss.get_health(),
                f"| ⚕️ {int(self._paddle.get_health()): >5} ",
                " " * 15,
            )
        elif self._lasertimeleft != 0:
            print(
                f"❤️ {int(self._lives): >5} | 🤑 {int(self._score): >5} | 🕒 {(_t - self._init_time): .2f} | 🧱 {int(self._total_breakable_bricks): >5} | 🏆 {int(self._level + 1): >5} | ⏰ {(self._lasertimeleft / 20): .2f}",
                " " * 15,
            )
        else:
            print(
                f"❤️ {int(self._lives): >5} | 🤑 {int(self._score): >5} | 🕒 {(_t - self._init_time): .2f} | 🧱 {int(self._total_breakable_bricks): >5} | 🏆 {int(self._level + 1): >5}",
                " " * 15,
            )

    def wall_collisions(self):
        for obj_type in self._objects:
            if obj_type == "ball" or obj_type == "powerup":
                for obj in self._objects[obj_type]:
                    x, y = obj.get_position()
                    v_x, v_y = obj.get_velocity()
                    h, w = obj.get_dimensions()

                    if x + w >= config.WIDTH or x <= 0:
                        obj.set_velocity([-v_x, v_y])

                    if y + h >= config.HEIGHT or y <= 0:
                        obj.set_velocity([v_x, -v_y])

    def check_bounding(self, obj1, obj2):
        x_1, y_1 = obj1.get_position()
        x_2, y_2 = obj2.get_position()
        vx, vy = obj1.get_velocity()

        h_1, w_1 = obj1.get_dimensions()
        h_2, w_2 = obj2.get_dimensions()

        if (
            (y_1 < y_2)
            and (y_1 + h_1 >= y_2)
            and (x_1 + w_1 >= x_2)
            and (x_2 + w_2 >= x_1)
        ):
            if x_1 < x_2:
                if vx < 0 and vy > 0:
                    return 1
                elif vx > 0 and vy < 0:
                    return 4
                elif vx > 0 and vy > 0:
                    if x_1 + w_1 - x_2 >= y_1 + h_1 - y_2:
                        return 1
                    else:
                        return 4
                else:
                    return 1
            elif x_1 + w_1 > x_2 + w_2:
                if vx > 0 and vy > 0:
                    return 1
                elif vx < 0 and vy < 0:
                    return 2
                elif vx < 0 and vy > 0:
                    if x_2 + w_2 - x_1 >= y_1 + h_1 - y_2:
                        return 1
                    else:
                        return 2
                else:
                    return 1
            else:
                return 1  # TOP

        if (
            (y_2 < y_1)
            and (y_2 + h_2 >= y_1)
            and (x_2 + w_2 >= x_1)
            and (x_1 + w_1 >= x_2)
            and (y_2 + h_2 <= y_1 + h_1)
        ):
            if x_1 < x_2:
                if vx < 0 and vy < 0:
                    return 3
                elif vx > 0 and vy > 0:
                    return 4
                elif vx > 0 and vy < 0:
                    if x_1 + w_1 - x_2 >= y_2 + h_2 - y_1:
                        return 3
                    else:
                        return 4
                else:
                    return 3
            elif x_1 + w_1 > x_2 + w_2:
                if vx > 0 and vy < 0:
                    return 3
                elif vx < 0 and vy > 0:
                    return 2
                elif vx < 0 and vy < 0:
                    if x_2 + w_2 - x_1 >= y_2 + h_2 - y_1:
                        return 3
                    else:
                        return 2
                else:
                    return 3
            else:
                return 3  # BOTTOM

        if (
            (x_2 < x_1)
            and (x_2 + w_2 >= x_1)
            and (y_2 + h_2 >= y_1)
            and (y_1 + h_1 >= y_2)
            and (x_2 + w_2 <= x_1 + w_1)
        ):
            return 2  # RIGHT

        if (
            (x_1 < x_2)
            and (x_1 + w_1 >= x_2)
            and (y_1 + h_1 >= y_2)
            and (y_2 + h_2 >= y_1)
        ):
            return 4  # LEFT

        return 0

    def fall_bricks(self):
        for obj_name in ["brick", "bossdef"]:
            for brick in self._objects[obj_name]:
                if brick.get_active():
                    x, y = brick.get_position()
                    h, w = brick.get_dimensions()
                    brick.set_position([x, y + 1])
                    self._maxheight = max(self._maxheight, y + 1 + h)

    def check_collisions(self):
        for pair in self._colliders:
            for obj in self._objects[pair[0]]:
                for target in self._objects[pair[1]]:
                    if obj.get_active() and target.get_active():
                        type_col = self.check_bounding(obj, target)
                        if type_col:
                            obj_name = pair[0]
                            target_name = pair[1]

                            if (
                                obj_name == "ball"
                                and target_name == "paddle"
                                and type_col == 1
                            ):
                                v_x, v_y = obj.get_velocity()

                                x_1, y_1 = obj.get_position()
                                h_1, w_1 = obj.get_dimensions()
                                x_2, y_2 = target.get_position()

                                h_2, w_2 = target.get_dimensions()

                                new_v_x = v_x + (x_1 - (x_2 + w_2 / 2)) / (w_2)

                                obj.set_position([x_1, y_2 - h_1 - 0.1])

                                if target.get_sticky() and target.get_space():
                                    obj.set_velocity([0.0, 0.0])
                                    target.set_space(False)
                                    self._paddle_bounce_vel = np.array([new_v_x, -v_y])
                                else:
                                    obj.set_velocity([new_v_x, -v_y])

                                if self._timer >= config.FALL_TIME:
                                    self._timer = 0
                                    self.fall_bricks()

                            if (obj_name == "ball" or obj_name == "bullet") and (
                                target_name == "brick" or target_name == "bossdef"
                            ):
                                v_x, v_y = obj.get_velocity()
                                x_1, y_1 = obj.get_position()
                                x_2, y_2 = target.get_position()
                                h_1, w_1 = obj.get_dimensions()
                                h_2, w_2 = target.get_dimensions()

                                if type_col == 1:
                                    y_1 = y_2 - h_1 - 0.1
                                    v_y = -v_y
                                elif type_col == 2:
                                    x_1 = x_2 + w_2 + 0.1
                                    v_x = -v_x
                                elif type_col == 3:
                                    y_1 = y_2 + h_2 + 0.1
                                    v_y = -v_y
                                elif type_col == 4:
                                    x_1 = x_2 - w_1 - 0.1
                                    v_x = -v_x

                                if target_name == "brick":
                                    if target.get_health() == 5:
                                        score, count, broken_bricks = target.destroy(
                                            obj_name, obj, self._objects["brick"]
                                        )
                                    else:
                                        score, count, broken_bricks = target.destroy(
                                            obj_name, obj, False, self._objects["brick"]
                                        )
                                elif target_name == "bossdef":
                                    score, count, broken_bricks = target.destroy(
                                        obj_name, obj, False, self._objects["brick"]
                                    )

                                self._score += score
                                self._total_breakable_bricks -= count

                                if target_name == "brick":
                                    if not target.get_active():
                                        power_chance = random.random()
                                        if power_chance > 0.5:
                                            bvx, bvy = obj.get_velocity()
                                            power_num = random.randint(1, 7)
                                            power = self._power_lookup[
                                                "class_" + str(power_num)
                                            ](
                                                position=np.array([x_2, y_2]),
                                                velocity=np.array([bvx, bvy]),
                                            )
                                            self._objects["powerup"].append(power)

                                    for brokenBrick in broken_bricks:
                                        power_chance = random.random()
                                        if power_chance > 0.8:
                                            bvx, bvy = obj.get_velocity()
                                            power_num = random.randint(1, 7)
                                            power = self._power_lookup[
                                                "class_" + str(power_num)
                                            ](
                                                position=np.array(brokenBrick),
                                                velocity=np.array([bvx, bvy]),
                                            )
                                            self._objects["powerup"].append(power)

                                if obj_name == "ball":
                                    obj.set_position([x_1, y_1])
                                    obj.set_velocity([v_x, v_y])
                                elif obj_name == "bullet":
                                    obj.set_active()

                            if obj_name == "bomb" and target_name == "paddle":
                                target.set_health()
                                obj.set_active()

                            if (
                                obj_name == "ball"
                                and target_name == "boss"
                                and type_col != 1
                            ):
                                v_x, v_y = obj.get_velocity()
                                x_1, y_1 = obj.get_position()
                                x_2, y_2 = target.get_position()
                                h_1, w_1 = obj.get_dimensions()
                                h_2, w_2 = target.get_dimensions()

                                if type_col == 2:
                                    x_1 = x_2 + w_2 + 3
                                    v_x = -v_x
                                elif type_col == 3:
                                    y_1 = y_2 + h_2 + 0.1
                                    v_y = -v_y
                                elif type_col == 4:
                                    x_1 = x_2 - w_1 - 3
                                    v_x = -v_x

                                self._score += target.hit()

                                obj.set_position([x_1, y_1])
                                obj.set_velocity([v_x, v_y])

                            if obj_name == "powerup" and target_name == "paddle":
                                power_type = obj.get_type()
                                if power_type == "s" or power_type == "e":
                                    obj.power(target)
                                    obj.set_start()
                                    self._active_powers.append(obj)
                                elif power_type == "f":
                                    for balls in self._objects["ball"]:
                                        if balls.get_active():
                                            obj.power(balls)
                                            if np.array_equal(
                                                balls.get_velocity(),
                                                np.array([0.0, 0.0]),
                                            ):
                                                self._paddle_bounce_vel *= (
                                                    config.BALL_DEC
                                                )
                                    obj.set_start()
                                    self._active_powers.append(obj)
                                elif power_type == "t":
                                    for balls in self._objects["ball"]:
                                        if balls.get_active():
                                            obj.power(balls)
                                    obj.set_start()
                                    temp_powers = [
                                        power_up
                                        for power_up in self._active_powers
                                        if power_up.get_type() != "t"
                                    ]
                                    temp_powers.append(obj)
                                    self._active_powers = temp_powers
                                # elif power_type == "fi":
                                #     for balls in self._objects["ball"]:
                                #         if balls.get_active():
                                #             obj.power(balls)
                                #     obj.set_start()
                                #     temp_powers = [
                                #         power_up
                                #         for power_up in self._active_powers
                                #         if power_up.get_type() != "fi"
                                #     ]
                                #     temp_powers.append(obj)
                                #     self._active_powers = temp_powers
                                elif power_type == "b":
                                    temp_balls = []
                                    for balls in self._objects["ball"]:
                                        new_ball = obj.power(balls)
                                        temp_balls.append(balls)
                                        temp_balls.append(new_ball)
                                    self._objects["ball"] = temp_balls
                                elif power_type == "p":
                                    obj.power(target)
                                    obj.set_start()
                                    temp_powers = [
                                        power_up
                                        for power_up in self._active_powers
                                        if power_up.get_type() != "p"
                                    ]
                                    temp_powers.append(obj)
                                    self._active_powers = temp_powers
                                elif power_type == "ps":
                                    obj.power(target)
                                    obj.set_start()
                                    temp_powers = [
                                        power_up
                                        for power_up in self._active_powers
                                        if power_up.get_type() != "ps"
                                    ]
                                    temp_powers.append(obj)
                                    self._active_powers = temp_powers
                                    self._lasertimeleft = config.POWER_DUR
                                obj.set_active()

    def check_active_powers(self):
        temp_power = []
        self._lasertimeleft -= 1
        if self._lasertimeleft < 0:
            self._lasertimeleft = 0

        for p in self._active_powers:
            if p.get_start():
                p.reduce_frames()
                if p.get_frames() <= 0:
                    type_power = p.get_type()
                    if type_power == "s" or type_power == "e":
                        p.remove_power(self._paddle)

                    elif type_power == "f":
                        for balls in self._objects["ball"]:
                            if balls.get_active():
                                p.remove_power(balls)
                                if np.array_equal(
                                    balls.get_velocity(),
                                    np.array([0.0, 0.0]),
                                ):
                                    self._paddle_bounce_vel /= config.BALL_DEC

                    elif type_power == "t":
                        for balls in self._objects["ball"]:
                            if balls.get_active():
                                p.remove_power(balls)

                    elif type_power == "p" or type_power == "ps":
                        if type_power == "ps":
                            self._lasertimeleft = 0
                        p.remove_power(self._paddle)
                else:

                    temp_power.append(p)

        self._active_powers = temp_power

    def end_game(self):
        paddle_x, paddle_y = self._paddle.get_position()
        if (
            self._lives == 0
            or self._maxheight >= paddle_y
            or self._paddle.get_health() == 0
        ):
            print(graphics.LOST_MSG)
        elif self._boss and self._boss.get_health() == 0:
            print(graphics.WON_MSG)
        else:
            print(graphics.BYE)

    def __del__(self):

        print(col.Style.RESET_ALL)
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")
        self.end_game()
        print("\033[?25h")