import pygame as pg
import pytmx
from settings import *


def collide_hit_rect(one, two):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    return one.hit_rect.colliderect(two.rect)

class TileMap:#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    def __init__(self,filename):
        print(filename)
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self,surface):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile,(x*self.tmxdata.tilewidth,
                                     y * self.tmxdata.tileheight))
    def make_map(self):#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
        temp_surface = pg.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:#ref:https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/working
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)