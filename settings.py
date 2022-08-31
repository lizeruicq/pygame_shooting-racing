import pygame as pg
vec = pg.math.Vector2

TITLE = "The last of US RETRO"
FPS = 60

WIDTH = 960
HEIGHT = 600

POST = 'post.png'
COVER = 'cover.jpg'
ENDCOVER = 'endcover.png'
CAR = 'ae86.png'
ARMCAR = 'armcar.png'

JOEL = 'joel.jpg'
EIILE = 'Eiile.jpg'
DOCTOR = 'doctor.jpg'
MALIN = 'malin.jpg'

PLAYER_IMG = 'soldier2.gif'
PLAYERBOW_IMG = 'soldierbow.gif'
PLAYER_IMG2 = 'soldier2[1].gif'
PLAYERDIE_IMG = 'soldierdie.gif'
PLAYER_HEALTH = 1
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_SPEED = 250
BARREL_OFFSET = vec(47, 10)

RANGER_IMG = 'ranger.png'
RANGERDIE = 'rangerdie.gif'

ENEMYSMALL_IMG = 'enemysmall.gif'

ENEMY_IMG = 'enemy.gif'
ENEMYDIE_IMG = 'enemydie.gif'
ENEMY_HIT_RECT = pg.Rect(0, 0, 40 ,40)
ENEMY_SPEED = 200
ENEMY_HEALTH = 1
AVOID_RADIUS = 50
DETECT_RADIUS = 400

DOCTOR_IMG = 'doctor2.gif'
DOCTORDIE_IMG = 'enemy2die.gif'
DOCTOR_HIT_RECT = pg.Rect(0, 0, 40 ,40)
DOCTOR_HEALTH = 1

GIRL = 'girl.png'
GIRLLIE = 'liegirl.png'
BOOM= 'boom.png'

MOB_SPEEDS = 2500
MOB_HEALTH = 1
MOB_IMG = ['mob.gif','mob3.gif']
MOB_IMG2 = 'mob2.gif'
MOBDIE_IMG = 'mobdie.gif'
MOB_HIT_RECT = pg.Rect(0, 0, 40, 40)
MOB_DAMAGE = 10
AVOID_RADIUS = 50
DETECT_RADIUS = 400

MUZZLE_FLASHES = 'whitePuff15.png'

STICK_IMG = 'stick.png'
STICK_EFFECT = '11.png'
STICK_SPEED = 300
STICK_LIFETIME = 100
STICK_RATE = 500
STICK_DAMAGE = 10

ARROW_IMG = 'arrow.png'

AMMO_IMG = 'ammo.png'
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 2000
BULLET_LIFETIME = 140
BULLET_RATE = 200
BULLET_DAMAGE = 10
BULLET_NUMBER = 5

SPLAT = 'blood.gif'
FLASH_DURATION = 50

PLAYER_LAYER = 2
ENEMY_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4

PATH_MUSIC = 'path.mp3'
START_MUSIC = 'last.mp3'
DRIVE_MUSIC = 'heartbeat.mp3'
ENEMYSHOOT_SUD = 'shoot2.mp3'
SHOOT_SUD = 'shoot4.mp3'
ENEMYDIE_SUD='enemydie.mp3'
MOBDIE_SUD='mobdie.mp3'
KNIFE_SUD = 'stick.mp3'
PICKUP_SUD = 'pickup.mp3'
EMPTY_SUD = 'empty.mp3'
CARRUN_SUD = 'carrun.mp3'
DRIFT_SUD = 'drift.mp3'
HITCAR_SUD = 'hitcar.mp3'
BOOMM_SUD = 'boom.mp3'
BOW_SUD ='holdbow.mp3'
ARROW_SUD ='arrow.mp3'

MAP0 = 'map.tmx'
MAP1 = 'map1.tmx'
MAP2 = 'map2.tmx'
MAP3 = 'map3.tmx'
MAP4 = 'map4.tmx'
MAP5 = 'map5.tmx'
