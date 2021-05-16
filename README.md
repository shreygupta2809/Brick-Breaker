# Inheritance

All child classes have been inherited from parent general class and so on.

# Polymorphism

There is a powerup class. All child classes override the power and remove_power function of that class. Also there is an exploding brick class which overrides destroy function of the parent brick class

> Encapsulation and Abstraction have also been implemented.

# Movememt

| Key   | Function          |
| ----- | ----------------- |
| a     | Move paddle left  |
| d     | Move paddle right |
| Space | Launch the ball   |
| q     | Quit              |
| l     | Level Change      |

# PowerUps

| PowerUp         | Role                                                    |
| --------------- | ------------------------------------------------------- |
| Expand Paddle   | Increases paddle size by constant                       |
| Shrink Paddle   | Decreases paddle size by constant                       |
| Ball Multiplier | Each ball splits into 2                                 |
| Fast Ball       | Spped of each ball is increased                         |
| Thru Ball       | Ball become strong and can break any break with one hit |
| Paddle Grab     | Allows the paddle to grab the ball                      |
| Shooting Paddle | Allows the paddle to shoot lasers automatically         |

> In Paddle Grab only one ball is allowed at a time to be held on the paddle. Other balls just bounce off

> All powerups except Ball Multiplier are valid for only a fixed duration of time.

# Score

Reducing health of any brick by one unit gives 100 score.

| Brick   | Score | Health               |
| ------- | ----- | -------------------- |
| Green   | 100   | 1                    |
| Blue    | 200   | 2                    |
| Magenta | 300   | 3                    |
| Yellow  | 400   | Unbreakable          |
| Red     | 100   | Exploding / 1        |
| Rainbow | 100   | Depends on first hit |

> Unbreakable Bricks are only destroyed they are adjacent to exploding bricks. Otherwise they are indestructible

# Winning / Losing

If all the breakable bricks are destroyed (all except unbreakable) then the player wins that level and moves to the next level.  
There is a boss level at the end and if you kill the boss then you win the game

> ***H*int**: There is any way to defeat the boss. You just have to figure it out!

A player gets 3 lives. If the player is unable to break all the bricks within 3 lives(i.e., loses all live) then the player loses. You also lose if your paddle health reaches 0.
You can also lose if the falling bricks reach your paddle.

# How to Play

```bash
cd 2019101058
pip install -r requirements/requirements.text
python3 main.py
```
