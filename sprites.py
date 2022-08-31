import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pandas as pd

vec = pg.math.Vector2


def playsound(clip, volume):  # soundplay function,can be called anywhere
    clip.set_volume(volume)
    clip.play()


def collide_with_walls(sprite, group, dir):  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    # detect and keep the collision between character and wall for x dimension and y dimension.
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Next(pg.sprite.Sprite):
    # when player reach this area, enter the next scene
    def __init__(self, game, x, y, w, h):
        self.groups = game.next
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Talk(pg.sprite.Sprite):
    # when player reach this area in MAP2, trigger the first dialog between docters and joel.
    def __init__(self, game, x, y, w, h):
        self.groups = game.talk
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if self.game.level == MAP0 or self.game.level == MAP1:
            self.image = game.player_img
        else:
            self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0) # the velocity of player
        self.pos = vec(x, y) # the current position
        self.rot = 0 # the rotation of the player
        self.last_shot = 0 # when last time shooting happend  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.health = PLAYER_HEALTH
        self.bullectnumber = BULLET_NUMBER
        self.strength = 1 # calculate the stength when the player holding the bow
        self.arrow = 10 # the player has ten arrows to shoot at MAP1

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]: # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.vel = vec(-PLAYER_SPEED, 0)
        if keys[pg.K_d]: # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.vel = vec(PLAYER_SPEED, 0)
        if keys[pg.K_w]:
            if self.game.level == MAP5: # in early version there were a short car
                # move and dialog for last scene,ignore this
                self.vel = vec(0, -150)
            else:
                self.vel = vec(0, -PLAYER_SPEED)
        if keys[pg.K_s]:
            self.vel = vec(0, PLAYER_SPEED)
        if pg.mouse.get_pressed()[0]:
            if self.game.level == MAP2 or self.game.level == MAP3 or self.game.level == MAP4:
                self.shoot() # in MAP2,MAP3,MAP5 your weapon is a pistol
            if self.game.level == MAP0 or self.game.level == MAP1: # in map1 you use a bow,
                # hold leftmouse to increase the strength before releasing
                if self.strength <= 500:
                    self.strength += 1
                    playsound(self.game.bow_sound, 0.2)
        if keys[pg.K_SPACE]: # press space to use knife to assassinate enemies.
            if self.game.level != MAP5:
                self.vel = vec(0, 0)
                self.image = pg.transform.rotate(self.game.player_img2, self.rot)
                self.knife()

    def bowshot(self): # release the arrow
        now = pg.time.get_ticks()
        if now - self.last_shot > 1000 and self.arrow > 0: # set the time gap for arrows
            self.game.bow_sound.stop()
            playsound(self.game.arrow_sound, 0.2)
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + vec(35, 10).rotate(-self.rot) # set the spawn pos and diriction of the arrow
            Arrow(self.game, pos, dir, BULLET_DAMAGE)
            self.arrow -= 1

    def shoot(self): # fire a bullet
        now = pg.time.get_ticks()
        if now - self.last_shot > BULLET_RATE and self.bullectnumber > 0: # ref:https://github.com/kidscancode/
            # pygame_tutorials/tree/master/tilemap/working
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + vec(35, 10).rotate(-self.rot)
            Bullet(self.game, pos, dir, BULLET_DAMAGE)
            MuzzleFlash(self.game, pos)
            playsound(self.game.weapon_sound, 0.3)
            self.bullectnumber -= 1
        elif self.bullectnumber <= 0:
            playsound(self.game.empty_sound, 0.2)

    def knife(self): # Generate melee actions and attack detection
        now = pg.time.get_ticks()
        if now - self.last_shot > STICK_RATE:
            self.last_shot = now
            dir = vec(0, 1).rotate(-self.rot)
            pos = self.pos + vec(30, -10).rotate(-self.rot)
            Knife(self.game, pos, dir, STICK_DAMAGE)
            playsound(self.game.knife_sound, 0.2)
            Knifeeffect(self.game, self.pos + vec(40, 0).rotate(-self.rot))

    def update(self):
        self.dir = pg.mouse.get_pos() - vec(self.game.camera.camera.topleft) - self.pos
        self.rot = self.dir.angle_to(vec(1, 0))
        if self.game.level == MAP0 or self.game.level == MAP1: #player hold a bow
            self.image = pg.transform.rotate(self.game.playerbow_img, self.rot)
        else: #player hold a gun
            self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.game.level == MAP5:
            self.image = self.game.carimg
        self.get_keys()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        collide_with_walls(self, self.game.walls,
                           'x')  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        collide_with_walls(self, self.game.water,
                           'x')  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.hit_rect.centery = self.pos.y  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        collide_with_walls(self, self.game.water, 'y')
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.game.die()


class Carenemy(pg.sprite.Sprite): # the AI vehicle in MAP5 will chase player's vehicle
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.enemycarg
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.armcarimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.acc = vec(0, 0)
        self.lastrot = 0 # the previous direction of enemy's vehicle
        self.health = 400
        self.autodrive = False # whether to start chasing player
        self.last_shot = 0 # when enemy vehicle shot the player's car

    def get_keys(self):
        self.rot_speed = 0
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: # when player's car move,start chasing
            self.autodrive = True

    def update(self, predictrot):
        self.get_keys()
        self.rot = predictrot  # use KNeighborsRegressor to predict the direction for turns
        if abs(self.rot - self.lastrot) > 70:
            self.lastrot = self.rot
        self.image = pg.transform.rotate(self.game.armcarimg, self.rot)
        if self.autodrive:
            self.acc = vec(500, 0).rotate(-self.rot)
        # move and drift, this was based on the mobs's movement
        self.acc += self.vel * -1.2 # The acceleration will continue to receive resistance according to the current speed
        self.vel += self.acc * self.game.dt # Current speed plus acceleration
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        self.target = self.game.player
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < 200 ** 2: # chaing and shoot player's car
            now = pg.time.get_ticks()
            if now - self.last_shot > 400:
                self.last_shot = now
                dir = vec(1, 0).rotate(-target_dist.angle_to(vec(1, 0)) + randint(-20, 20)) # aim the player's car
                pos = self.pos + vec(0, -30).rotate(-self.rot)
                Bullet(self.game, pos, dir, BULLET_DAMAGE)
                MuzzleFlash(self.game, self.pos + vec(0, -30).rotate(-self.rot))
                playsound(self.game.enemyweapon_sound, 0.2)

        if self.health <= 0:
            playsound(self.game.boom_sound, 1)
            self.kill()
            self.game.map_img.blit(self.game.boomimage, self.pos - vec(32, 32))


class Carself(pg.sprite.Sprite): # player
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.carself
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.carimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.acc = vec(0, 0)
        self.lastrot = 0 # the previous direction of player's vehicle
        self.health = 800

    def get_keys(self): # move and turn
        self.rot_speed = 0
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rot_speed = 300
        if keys[pg.K_d]:
            self.rot_speed = -300
        if keys[pg.K_w]:
            self.acc = vec(500, 0).rotate(-self.rot)
        if keys[pg.K_s]:
            self.acc = vec(-200, 0).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        if abs(self.rot - self.lastrot) > 70:
            playsound(self.game.drift_sound, 0.5)
            self.lastrot = self.rot # if current turn is more than 70 degree, play the drift sound
        self.image = pg.transform.rotate(self.game.carimg, self.rot)
        self.acc += self.vel * -1.2 # same as enemy's vehicle
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            playsound(self.game.boom_sound, 1)
            self.kill()
            self.game.map_img.blit(self.game.boomimage, self.pos - vec(32, 32))
            self.game.die()


class Enemy(pg.sprite.Sprite):  # enemy for MAP2,MAP3,MAP4
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.rot = randint(1, 360)
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos
        self.target = game.player
        self.speed = ENEMY_SPEED
        self.last_shot = 0
        self.health = ENEMY_HEALTH
        self.vel = vec(0, 0)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 600:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + vec(50, 10).rotate(-self.rot)
            Bullet(self.game, pos, dir, BULLET_DAMAGE)
            MuzzleFlash(self.game, self.pos + vec(50, 10).rotate(-self.rot))
            playsound(self.game.enemyweapon_sound, 0.2)

    def turns(self): # when player is out of enemy's attack range, enemy will randomly turn around from time to time
        now = pg.time.get_ticks()
        if now - self.last_shot > 2000:
            self.rot = randint(1, 360)
            self.last_shot = now

    def update(self):
        self.turns()
        target_dist = self.target.pos - self.pos
        self.image = pg.transform.rotate(self.game.enemy_img, self.rot)
        if target_dist.length_squared() < DETECT_RADIUS ** 2 and abs(self.game.player.rot - self.rot) > 90 and abs(
                self.game.player.rot - self.rot) < 270: # when player is within enemy's attack range and facing the enemy
            # if the enemy is not facing the player, they wont chase or shoot the player.
            self.shoot()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.enemy_img, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.acc.scale_to_length(self.speed)# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.acc += self.vel * -1# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.vel += self.acc * self.game.dt# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.pos += self.vel * self.game.dt# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            if target_dist.length_squared() < (DETECT_RADIUS / 1.5) ** 2: # the enemy stop moving when close to the player
                self.vel = vec(1, 0)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working

        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            playsound(self.game.enemydie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            # self.game.map_img.blit(self.game.enemydie, self.pos - vec(32, 32))
            self.game.map_img.blit(pg.transform.rotate(self.game.enemydie, self.rot), self.pos - vec(32, 32))
            Ammo(self.game, self.pos)


class Enemysmall(Enemy): # enemy in the MAP5 (shoot player's car at racing track)
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = self.game.enemysmall_img

    def update(self):
        self.turns()
        target_dist = self.target.pos - self.pos
        self.image = pg.transform.rotate(self.game.enemysmall_img, self.rot)
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            now = pg.time.get_ticks()
            if now - self.last_shot > 200:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot + randint(-20, 20))
                pos = self.pos + vec(50, 10).rotate(-self.rot)
                Bullet(self.game, pos, dir, BULLET_DAMAGE)
                MuzzleFlash(self.game, self.pos + vec(50, 10).rotate(-self.rot))
                playsound(self.game.enemyweapon_sound, 0.2)
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.enemysmall_img, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt
            if target_dist.length_squared() < (DETECT_RADIUS / 1.5) ** 2:
                self.vel = vec(1, 0)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            playsound(self.game.enemydie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))


class Ranger(pg.sprite.Sprite): # enemy in MAP1
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = None
        self.master_image = game.ranger_img
        self.old_frame = -1
        self.bigrect = self.master_image.get_rect()
        self.frame_width = self.bigrect.copy().width // 4
        self.frame_height = self.bigrect.copy().height
        self.rect = pg.Rect(0, 0, 60, 60)
        self.rect.center = vec(x, y)
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rot = randint(1, 360)
        self.columns = 4
        self.last_frame = (self.bigrect.width // self.frame_width) \
                          * (self.bigrect.height // self.frame_height) - 1
        self.frame = 0
        self.first_frame = 0
        self.last_time = 0
        self.target = game.player
        self.speed = 200
        self.last_shot = 0
        self.health = ENEMY_HEALTH
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def playani(self): # play framing animation when move
        current_time = pg.time.get_ticks()
        if current_time > self.last_time + 150:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            pic = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(pic)
            self.image = pg.transform.rotate(self.image, self.rot)
            self.old_frame = self.frame

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 1000:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + vec(50, 0).rotate(-self.rot)
            Bullet(self.game, pos, dir, BULLET_DAMAGE)
            playsound(self.game.enemyweapon_sound, 0.1)

    def turns(self):
        self.vel = vec(30, 0).rotate(-self.rot) * self.game.dt
        self.pos += self.vel
        now = pg.time.get_ticks()
        if now - self.last_shot > 3000:
            self.rot = randint(1, 360)
            self.last_shot = now

    def chasing(self):
        target_dist = self.target.pos - self.pos
        self.shoot()
        self.rot = target_dist.angle_to(vec(1, 0))
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        if target_dist.length_squared() < (DETECT_RADIUS / 4) ** 2:
            self.vel = vec(1, 0)

    def avoid(self):  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        for guy in self.game.enemies:
            if guy != self:
                dist = self.pos - guy.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.playani()
        target_dist = self.target.pos - self.pos
        self.avoid()
        if target_dist.length_squared() < 350 ** 2 and abs(self.game.player.rot - self.rot) > 90 and abs(
                self.game.player.rot - self.rot) < 270:
            self.chasing()
        else:
            self.turns()
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.water, 'x')
        collide_with_walls(self, self.game.water, 'y')
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            playsound(self.game.enemydie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.map_img.blit(pg.transform.rotate(self.game.rangerdie_img, self.rot), self.pos - vec(32, 32))
            if self.game.level == MAP2:
                Ammo(self.game, self.pos)


class Doctor(pg.sprite.Sprite): #NPC Character
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAYER
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.doctortdimg.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.rot = randint(1, 360)
        self.hit_rect = DOCTOR_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = self.pos
        self.target = game.player
        self.speed = ENEMY_SPEED
        self.health = DOCTOR_HEALTH

    def update(self):

        target_dist = self.target.pos - self.pos
        self.image = pg.transform.rotate(self.game.doctortdimg, self.rot)
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.doctortdimg, self.rot)
            self.rect.center = self.pos

        if self.health <= 0:
            playsound(self.game.enemydie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.map_img.blit(pg.transform.rotate(self.game.doctordie, self.rot), self.pos - vec(32, 32))


class Eiile(pg.sprite.Sprite): # become teammate in the MAP4, after being rescued from hospital
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.girlimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = randint(1, 360)
        self.health = PLAYER_HEALTH
        self.speed = 150
        self.last_shot = 0
        self.target = game.player

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > 2000:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + vec(50, 10).rotate(-self.rot)
            EBullet(self.game, pos, dir, BULLET_DAMAGE)
            MuzzleFlash(self.game, self.pos + vec(50, 10).rotate(-self.rot))
            playsound(self.game.enemyweapon_sound, 0.2)

    def update(self): # search zombies and shoot
        for enemy in self.game.mobs:
            if (enemy.pos - self.pos).length_squared() < DETECT_RADIUS ** 2 and enemy.health > 0:
                self.rot = (enemy.pos - self.pos).angle_to(vec(1, 0))
                self.shoot()

        target_dist = self.target.pos - self.pos
        self.image = pg.transform.rotate(self.game.girlimg, self.rot)
        if target_dist.length_squared() > 100 ** 2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.girlimg, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.hit_rect.centerx = self.pos.x
            self.pos += self.vel * self.game.dt
            if target_dist.length_squared() < 50 ** 2:
                self.vel = vec(1, 0)

        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.water, 'x')
        collide_with_walls(self, self.game.water, 'y')
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.game.showUI(self.game.headimage, 'Eiile!!!!')
            playsound(self.game.eiiledie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.map_img.blit(pg.transform.rotate(self.game.girllieimg, self.rot), self.pos - vec(32, 32))
            self.game.playing = False


class Mob(pg.sprite.Sprite): # zombies class, can kill player as long as they collied with the player
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_img2
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = randint(1, 360)
        self.health = MOB_HEALTH
        self.damage = MOB_DAMAGE
        self.speed = MOB_SPEEDS
        self.target = game.player

    def avoid_mobs(self):  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.image = pg.transform.rotate(self.game.mob_img2, self.rot)
        for enemy in self.game.enemies:
            self.target2 = enemy
        target2_dist = self.target2.pos - self.pos # search enemy soldiers and chasing
        if target2_dist.length_squared() < DETECT_RADIUS ** 2:
            self.rot = target2_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(choice(self.game.mob_img), self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -3
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS ** 2: # search the player and chasing
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(choice(self.game.mob_img), self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -3
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

        if self.health <= 0:
            playsound(self.game.mobdie_sound, 0.5)
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.game.map_img.blit(pg.transform.rotate(self.game.mobdie, self.rot), self.pos - vec(32, 32))


class Obstacle(pg.sprite.Sprite): # the wall class, ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Water(pg.sprite.Sprite): # the water class can be crossed by bullets but not by any character
    def __init__(self, game, x, y, w, h):
        self.groups = game.water
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Ammo(pg.sprite.Sprite): # droped by dead enemy
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.ammo
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.ammo_image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos


class Bullet(pg.sprite.Sprite):  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()


class Arrow(Bullet):
    def __init__(self, game, pos, dir, damage):
        super(Arrow, self).__init__(game, pos, dir, damage)
        self.rot = self.game.player.rot
        self.image = pg.transform.rotate(self.game.arrow_image, self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = pos

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > self.game.player.strength * 3:
            self.kill()
            self.game.player.strength = 0


class Knife(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.game = game
        self.groups = game.all_sprites, game.knife
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rot = self.game.player.rot
        self.image = pg.transform.rotate(game.knife_image, self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * STICK_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.rot = self.game.player.rot
        self.image = pg.transform.rotate(self.game.knife_image, self.game.player.rot)
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > STICK_LIFETIME:
            self.kill()


class EBullet(pg.sprite.Sprite): # Eiile's bullet, won't hurt the player
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.ebullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > 150:
            self.kill()


class MuzzleFlash(pg.sprite.Sprite):  # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        size = randint(20, 50)
        self.image = pg.transform.scale(game.gun_flashes, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Knifeeffect(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.rotate(game.knife_effect, self.game.player.rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Dialoghead(pg.sprite.Sprite): # the profile picture in dialog at top left on screen
    def __init__(self, game, image):
        self.game = game
        self.groups = game.UI
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.spawn_time = pg.time.get_ticks()


class Dialog(pg.sprite.Sprite): # the text in dialog at top left on screen
    def __init__(self, game, text):
        self.game = game
        self.groups = game.UI
        pg.sprite.Sprite.__init__(self, self.groups)
        self.text = pg.font.SysFont("arial", 32).render(text, True, (255, 255, 255))
        self.image = self.text
        self.rect = pg.Rect(102, 0, 300, 50)
        self.spawn_time = pg.time.get_ticks()
