import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import pandas as pd
class Game():
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048) # background music
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screenrect = self.screen.get_rect()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.level = MAP0 # current level
        self.load_data()
        # parameter for dialog
        self.index = 99
        self.lasttime = 99


    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        music_folder = path.join(game_folder, 'music')
        pg.mixer.music.load(path.join(music_folder, PATH_MUSIC))
        self.start_music = pg.mixer.Sound(path.join(music_folder, START_MUSIC))
        self.drive_music = pg.mixer.Sound(path.join(music_folder, DRIVE_MUSIC))
        self.weapon_sound = pg.mixer.Sound(path.join(music_folder, SHOOT_SUD))
        self.enemyweapon_sound = pg.mixer.Sound(path.join(music_folder, ENEMYSHOOT_SUD))
        self.enemydie_sound = pg.mixer.Sound(path.join(music_folder, ENEMYDIE_SUD))
        self.mobdie_sound = pg.mixer.Sound(path.join(music_folder, MOBDIE_SUD))
        self.eiiledie_sound = pg.mixer.Sound(path.join(music_folder,'eiiledie.mp3'))
        self.knife_sound = pg.mixer.Sound(path.join(music_folder, KNIFE_SUD))
        self.empty_sound = pg.mixer.Sound(path.join(music_folder, EMPTY_SUD))
        self.pickup_sound = pg.mixer.Sound(path.join(music_folder, PICKUP_SUD))
        self.carrun_sound = pg.mixer.Sound(path.join(music_folder, CARRUN_SUD))
        self.drift_sound = pg.mixer.Sound(path.join(music_folder, DRIFT_SUD))
        self.hitcar_sound = pg.mixer.Sound(path.join(music_folder, HITCAR_SUD))
        self.boom_sound = pg.mixer.Sound(path.join(music_folder, BOOMM_SUD))
        self.arrow_sound = pg.mixer.Sound(path.join(music_folder, ARROW_SUD))
        self.bow_sound = pg.mixer.Sound(path.join(music_folder, BOW_SUD))
        self.font = pg.font.Font.bold
        self.map_folder = path.join(game_folder,'maps')
        self.player_img = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.player_img2 = pg.image.load(path.join(img_folder, PLAYER_IMG2)).convert_alpha()
        self.playerbow_img = pg.image.load(path.join(img_folder, PLAYERBOW_IMG)).convert_alpha()
        self.playerdie_img = pg.image.load(path.join(img_folder, PLAYERDIE_IMG)).convert_alpha()
        self.enemy_img = pg.image.load(path.join(img_folder,ENEMY_IMG)).convert_alpha()
        self.enemysmall_img = pg.image.load(path.join(img_folder, ENEMYSMALL_IMG)).convert_alpha()
        self.ranger_img = pg.image.load(path.join(img_folder, RANGER_IMG)).convert_alpha()
        self.rangerdie_img = pg.image.load(path.join(img_folder, RANGERDIE)).convert_alpha()
        self.enemydie = pg.image.load(path.join(img_folder, ENEMYDIE_IMG)).convert_alpha()
        self.doctortdimg = pg.image.load(path.join(img_folder, DOCTOR_IMG)).convert_alpha()
        self.doctordie = pg.image.load(path.join(img_folder, DOCTORDIE_IMG)).convert_alpha()
        self.girlimg = pg.image.load(path.join(img_folder, GIRL)).convert_alpha()
        self.girllieimg = pg.image.load(path.join(img_folder, GIRLLIE)).convert_alpha()
        self.carimg = pg.image.load(path.join(img_folder, CAR)).convert_alpha()
        self.armcarimg = pg.image.load(path.join(img_folder, ARMCAR)).convert_alpha()
        self.mob_img2 = pg.image.load(path.join(img_folder, MOB_IMG2)).convert_alpha()
        self.mob_img = []
        for img in MOB_IMG:
            # fake the mob animation by keep refreshing two imgs for mobs.
            self.mob_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.mobdie = pg.image.load(path.join(img_folder, MOBDIE_IMG)).convert_alpha()
        self.bullet_image = pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()
        self.arrow_image = pg.image.load(path.join(img_folder, ARROW_IMG)).convert_alpha()
        self.ammo_image = pg.image.load(path.join(img_folder, AMMO_IMG)).convert_alpha()
        self.knife_image = pg.image.load(path.join(img_folder, STICK_IMG)).convert_alpha()
        self.knife_effect = pg.image.load(path.join(img_folder, STICK_EFFECT)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = pg.image.load(path.join(img_folder, MUZZLE_FLASHES)).convert_alpha()
        self.headimage = pg.image.load(path.join(img_folder, JOEL)).convert_alpha()
        self.eiileimage = pg.image.load(path.join(img_folder, EIILE)).convert_alpha()
        self.doctorimage = pg.image.load(path.join(img_folder, DOCTOR)).convert_alpha()
        self.malinimage = pg.image.load(path.join(img_folder, MALIN)).convert_alpha()
        self.boomimage = pg.image.load(path.join(img_folder, BOOM)).convert_alpha()
        self.endcover = pg.image.load(path.join(img_folder, ENDCOVER)).convert_alpha()
        # pg.mixer.music.play(loops=-1)

    def new(self,level):
        self.all_sprites = pg.sprite.LayeredUpdates() #ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.UI = pg.sprite.Group()
        if self.level == MAP0:
            self.mark = ''          # the name of current scene at right bottom conor
            self.start_music.play(loops=-1)
            pg.mixer.music.pause()
        if self.level == MAP1:
            self.showUI(self.headimage, 'Where is operating room..I aint got time for this') # the dialog window at the left top
            self.mark = 'The River path'
        if self.level==MAP2:
            self.showUI(self.headimage, 'Eiile,where are you?')
            self.mark = 'Fireflies sector'
        if self.level == MAP3:
            self.showUI(self.headimage, 'Eiile,where are you?')
            self.mark = 'St. Marys Hospital'
        if self.level==MAP4:
            self.showUI(self.headimage, 'Follow me,lets go home')
            self.mark = 'The Chicago sub'
        if self.level==MAP5:
            pg.mixer.music.stop()
            self.index = 10 # dialog for last scene will be triggered
            self.lasttime = 0
            self.mark = 'the last of us retro'
        self.walls = pg.sprite.Group()
        self.water = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.ebullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.knife = pg.sprite.Group()
        self.next = pg.sprite.Group()
        self.enemycarg = pg.sprite.Group()
        self.carself = pg.sprite.Group()
        self.talk = pg.sprite.Group()
        self.mobs = pg.sprite.Group()#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.ammo = pg.sprite.Group()
        self.map = TileMap(path.join(self.map_folder, self.level)) # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.map_img = self.map.make_map() # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.map.rect = self.map_img.get_rect() # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        for tile_object in self.map.tmxdata.objects:#load sprites from tilemap,ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if self.level == MAP5:
                if tile_object.name == 'car':
                    self.player = Carself(self, obj_center.x, obj_center.y)
                if tile_object.name == 'carenemy':
                    self.enemycar = Carenemy(self, obj_center.x, obj_center.y)
            if tile_object.name == 'ranger':
                Ranger(self, obj_center.x, obj_center.y)
            if tile_object.name == 'enemy':
                Enemy(self, obj_center.x, obj_center.y)
            if tile_object.name == 'enemysmall':
                Enemysmall(self, obj_center.x, obj_center.y)
            if tile_object.name == 'doctor':
                Doctor(self, obj_center.x, obj_center.y)
            if tile_object.name == 'eiile':
                self.eiile=Eiile(self, obj_center.x, obj_center.y)
            if tile_object.name == 'mob':#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'water':
                Water(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'next':
                Next(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'talk':
                Talk(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'lie':
                self.map_img.blit(self.girllieimg,vec(tile_object.x, tile_object.y))
        self.camera = Camera(self.map.width, self.map.height)#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.paused = False
        self.show = True # wehther the dialog should be showed


    def run(self):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 900
            # if self.level == MAP5:
            #     print(f"{self.player.pos.x},{self.player.pos.y},{self.player.rot}",file=sample)


            self.events()
            self.update()
            if not self.paused and self.level == MAP5: # calculate the track of the AI vehicle by KNeighborsRegressor
                predict = df.append({'x': self.enemycar.pos.x, 'y': self.enemycar.pos.y}, ignore_index=True)
                self.enemycarg.update(clf.predict(predict))
            self.draw()

    def update(self):
        self.showdialog()
        self.all_sprites.update()
        self.UI.update()
        self.camera.update(self.player)#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working

        # collision detection
        hits = pg.sprite.groupcollide(self.enemies, self.mobs, False, False)
        for enemy in hits:
            enemy.health -= 10
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy in hits:
            for bullet in hits[enemy]:
                enemy.health -= bullet.damage
            enemy.vel = vec(0, 0)
        hits = pg.sprite.groupcollide(self.enemies, self.ebullets, False, True)
        for enemy in hits:
            for ebullet in hits[enemy]:
                enemy.health -= ebullet.damage
            enemy.vel = vec(0, 0)
        hits = pg.sprite.groupcollide(self.enemies, self.knife, False, True)
        for enemy in hits:
            for knife in hits[enemy]:
                enemy.health -= knife.damage
            enemy.vel = vec(0, 0)

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)
        hits = pg.sprite.groupcollide(self.mobs, self.ebullets, False, True)
        for mob in hits:
            for ebullet in hits[mob]:
                mob.health -= ebullet.damage
            mob.vel = vec(0, 0)
        hits = pg.sprite.groupcollide(self.mobs, self.knife, False, True)
        for mob in hits:
            for knife in hits[mob]:
                mob.health -= knife.damage
            mob.vel = vec(0, 0)

        hitsplayer = pg.sprite.spritecollide(self.player, self.bullets, True, collide_hit_rect)
        if hitsplayer:
            for bullet in hitsplayer:
                self.player.health -= bullet.damage
            if self.level == MAP5:
                playsound(self.hitcar_sound,0.4)

        if self.level==MAP4:
            hitseiile = pg.sprite.spritecollide(self.eiile, self.bullets, True, collide_hit_rect)
            if hitseiile:
                for bullet in hitseiile:
                    self.eiile.health -= bullet.damage
            hitseiile = pg.sprite.spritecollide(self.eiile, self.knife, True, collide_hit_rect)
            if hitseiile:
                for knife in hitseiile:
                    self.eiile.health -= knife.damage

        hitsmobs = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        if hitsmobs:
            for mob in hitsmobs:
                self.player.health -= mob.damage

        hitsnext = pg.sprite.spritecollide(self.player, self.next, False, collide_hit_rect)
        if hitsnext:
            self.playing=False
        hitsammo = pg.sprite.spritecollide(self.player, self.ammo, True, collide_hit_rect)
        if hitsammo:
            playsound(self.pickup_sound, 0.2)
            if self.player.bullectnumber<4:
                self.player.bullectnumber += randint(1,2)
            elif self.player.bullectnumber == 4:
                self.player.bullectnumber += 1

        hitstalk = pg.sprite.spritecollide(self.player, self.talk, False, collide_hit_rect)
        if hitstalk:
            self.index = 0
            self.lasttime = 0
        hitscar = pg.sprite.spritecollide(self.player, self.enemycarg, False, collide_hit_rect)
        if hitscar:
            self.player.rot-=3
            self.player.pos -= vec(0,-5).rotate(self.player.rot)

        hitscar1 = pg.sprite.groupcollide(self.enemies, self.carself, False, False)
        if hitscar1:
            for enemy in hitscar1:
                 enemy.health-=10
        hitscar2 = pg.sprite.groupcollide(self.enemies, self.enemycarg, False, False)
        if hitscar2:
            for enemy in hitscar2:
                enemy.health -= 10
        hitscar3 = pg.sprite.groupcollide(self.enemycarg, self.bullets, False, False)
        if hitscar3:
            for car in hitscar3:
                car.health -= 10
        hitscar4 = pg.sprite.groupcollide(self.enemycarg, self.next, False, False)
        if hitscar4:
            self.player.health-=1000


    def quit(self):
        pg.quit()
        sys.exit()

    def die(self):
        if self.level == MAP4: # if joel in killed in the hospital(MAP3)
            self.showUI(self.eiileimage, 'Joel!!!!')
        else: # if joel in killed in other scene
            self.showUI(self.headimage, 'Eiile...sorry..')
        self.player.kill()
        if self.level != MAP5:
            self.map_img.blit(self.splat, self.player.pos - vec(32, 32))
            self.map_img.blit(pg.transform.rotate(self.playerdie_img, self.player.rot),
                          self.player.pos - vec(32, 32))
        self.playing=False

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply(self.map)) # draw the ground
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        # self.draw_dialog(self.talk)
        if self.level == MAP5 and self.enemycar.health>0:
            self.screen.blit(self.enemycar.image, self.camera.apply(self.enemycar))
        for ui in self.UI: # draw texts on screen
            self.screen.blit(ui.image, ui.rect)
        self.drawmark()
        pg.display.flip()


    def events(self):
        for event in pg.event.get():
            if self.level == MAP0 or self.level == MAP1: # in MAP1, the arrow will be fired with current strength
                # if player release the leftmouse
                if event.type == pg.MOUSEBUTTONUP:
                    self.player.bowshot()
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_r:
                    self.player.health-=1000


    def draw_text(self,text,font_name,size,color,x,y,align ="center"):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        font = pg.font.SysFont("arial", 32)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)



    def show_go_screen(self): # the player was killed or the player reach the 'next'area
        if self.playing == False and self.player.health<=0 or (self.level == MAP4 and self.eiile.health<0):
            # ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
            self.draw_text("GAME OVER", self.font, 100, (106, 55, 5),
                           WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("Press a key to start", self.font, 75, (106, 55, 5),
                           WIDTH / 2, HEIGHT * 3 / 4, align="center")
            pg.display.flip()
            self.wait_for_key()

        elif self.playing == False and self.player.health>0:
            if self.level==MAP0:
                self.start_music.stop()
                pg.mixer.music.play(loops=-1)
                pg.mixer.music.set_volume(0.5)
                self.level = MAP1
            elif self.level == MAP1:
                self.level = MAP2
            elif self.level==MAP2:
                self.level = MAP3
            elif self.level==MAP3:
                self.level = MAP4
            elif self.level==MAP4:
                pg.mixer.music.stop()
                self.drive_music.set_volume(0.35)
                self.drive_music.play(loops=-1)
                self.level = MAP5
            elif self.level==MAP5:
                self.level = MAP0
                self.drive_music.stop()
                self.screen.blit(self.endcover, self.screenrect)
                pg.display.flip()
                self.wait_for_key()
            self.playing = True


    def wait_for_key(self):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    waiting = False

    def showUI(self,image,text):
        for i in self.UI:
            i.kill()
        Dialoghead(self, image)
        Dialog(self, text)

    def drawmark(self): # show current ammo/arrows ,dialog and instruction
        dialogrect=vec(700,550)
        font = pg.font.SysFont("arial", 30)
        text_surface = font.render(self.mark, True, (255,255,255))
        if self.level != MAP0 and self.level != MAP5:
            ammofig_surface = font.render("Ammo: "+str(self.player.bullectnumber)+"/5", True, (255,255,255))
            arrowfig_surface = font.render("Arrow: " + str(self.player.arrow) + "/10", True, (255, 255, 255))
            notice_surface = font.render("find the green mark to enter next area", True, (255, 255, 255))
            if self.level == MAP1:
                self.screen.blit(arrowfig_surface, vec(0, 550))
            else:
                self.screen.blit(ammofig_surface, vec(0, 550))
            self.screen.blit(notice_surface, vec(0, 500))
        self.screen.blit(text_surface, dialogrect)




    def showdialog(self): # The text in the dialog window
        # will automatically refresh according to the time interval after being triggered
        if self.index == 0 and self.show==True:
            self.showUI(self.headimage,'sweet Jusus?')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 1 and self.show==True:
            self.showUI(self.doctorimage,'What are you doing here?!')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 2 and self.show==True:
            self.showUI(self.doctorimage, 'I wont let you take her,This is our furture.Think of all the lives we will save!')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 3 and self.show==True:
            self.showUI(self.doctorimage, 'Dont come any closer,I mean it')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 4 and self.show == True:
            self.showUI(self.malinimage, 'No! you fucking animal!')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 5 and self.show == True:
            self.showUI(self.malinimage, 'You can still do the right thing here')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 6 and self.show == True:
            self.showUI(self.headimage, 'Shut the hell up!')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 7 and self.show == True:
            self.showUI(self.headimage, 'Come on baby girl, I gotcha..')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if pg.time.get_ticks() - self.lasttime > 3000 and self.index<7:
            self.index += 1
            self.show = True
        elif pg.time.get_ticks() - self.lasttime > 3000 and self.index==7:
            self.index = 99
#         last scene
        if self.index == 10 and self.show==True:
            self.showUI(self.eiileimage,'What happened?')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 11 and self.show==True:
            self.showUI(self.headimage,'We found fireflies,Turns out theres whole lot more like you,Eiile')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 12 and self.show==True:
            self.showUI(self.headimage,'People that are immune,Its dozens actually,Aint done a damn bit of good neither.')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 13 and self.show==True:
            self.showUI(self.headimage,'They actuallys ve stopped looking for a cure')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 14 and self.show==True:
            self.showUI(self.headimage,'Im taking us home...')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 15 and self.show==True:
            self.showUI(self.headimage,'Im sorry.')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 16 and self.show==True:
            self.showUI(self.eiileimage,'Swear to me that everything that you said about the Fireflies is true.')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if self.index == 17 and self.show==True:
            self.showUI(self.headimage,'I swear')
            self.lasttime = pg.time.get_ticks()
            self.show = False
        if pg.time.get_ticks() - self.lasttime > 3000 and self.index<17 and self.index>=10:
            self.index += 1
            self.show = True
        if pg.time.get_ticks() - self.lasttime > 5000 and self.index==17 and self.index>=10:
            for i in self.UI:
                i.kill()
            self.index = 99


g = Game()
drive_data = pd.read_csv('test.csv') # Read the saved track data
X= drive_data.drop(columns="rot")
y= drive_data['rot']
from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor(n_neighbors=2)
clf = neigh.fit(X, y) # Learn data and plan a route by regression
df = pd.DataFrame(columns=['x','y'])
# sample = open("test.csv","w")
# print("x,y,rot",file = sample)

while True:# ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    g.new(g.level)
    g.run()
    g.show_go_screen()


