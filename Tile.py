import pygame as pg
import random

DRAW_SIDE_CONNECTIONS = False
DRAW_ENTROPY = False
DRAW_ROTATION = False

Stupid_green_reduction = False
OPTIMIZE_DRAW = True


class AllImages:
    def __init__(self, size):
        self.images = []
        self.rotations = []
        self.edges = []
        self.size = size

    def add_image(self, imageString, rotationQuantities, TRBLedges):
        self.images.append(pg.transform.scale(pg.image.load(imageString), (self.size, self.size)))
        self.rotations.append(rotationQuantities)
        self.edges.append(TRBLedges)


class SuperPosition:
    def __init__(self):
        # dict from image number to the possible rotations it can have
        self.positions = {}
        self.entropy = -1

    def create_all_positions(self, allImages):
        for x in range(len(allImages.rotations)):
            self.positions[x] = []
            for y in range(allImages.rotations[x]):
                self.positions[x].append(y)
        return

    def get_entropy(self):
        count = 0
        for x in self.positions:
            count += len(self.positions[x])
        return count

    def pick_random_superposition(self):
        if self.get_entropy() == 0:
            while True:
                print("0 entropy tile :(")

        position = random.randint(0, self.get_entropy() - 1)
        x = 0
        for i in self.positions:
            for j in self.positions[i]:
                if x == position:
                    if i or j is None:
                        x += 1

                    if Stupid_green_reduction and i <= 5 and random.random() < .95:
                        return self.pick_random_superposition()
                    self.positions = {i: [j]}
                    return i, j
                x += 1


class Tile:
    def __init__(self, posX, posY, tileSize, images, i, j) -> None:
        self.x = posX
        self.y = posY
        self.i = i
        self.j = j
        self.size = tileSize
        self.images = images

        self.collapsed = False

        self.imageNumber = -1
        self.finalImage = None

        # rotation 0 is normal, 1 is 90 deg cw, ect
        self.rotation = None

        self.superposition = SuperPosition()

        self.drawTile = False

    def create_superpositions(self):
        self.superposition.create_all_positions(self.images)
        return

    def get_location(self):
        return self.i, self.j

    # get possible designs for tile
    def get_superposition(self):
        return self.superposition

    def is_collapsed(self):
        return self.collapsed

    def get_entropy(self):
        if self.collapsed:
            return 1
        return self.superposition.get_entropy()

    def set_random_superposition(self):
        shape, rotation = self.superposition.pick_random_superposition()
        self.rotation = rotation
        self.imageNumber = shape
        self.finalImage = self.images.images[shape]
        self.collapsed = True
        self.drawTile = True

    def draw_tile(self, screen):
        if self.drawTile is False and OPTIMIZE_DRAW:
            return
        self.drawTile = False
        if self.collapsed:
            self.finalImage = pg.transform.rotate(self.finalImage, self.rotation*90)
            screen.blit(self.finalImage, (self.x, self.y))
            self.finalImage = pg.transform.rotate(self.finalImage, self.rotation * -90)
            if DRAW_ROTATION:
                font = pg.font.SysFont(None, 24)
                img = font.render(str(self.rotation), True, [0, 0, 0])
                screen.blit(img, (self.x + self.size / 2 - 5, self.y + self.size / 2 - 8))  # middle

        if DRAW_ENTROPY:
            font = pg.font.SysFont(None, 24)
            img = font.render(str(self.get_entropy()), True, [0, 0, 0])
            screen.blit(img, (self.x + self.size / 2 - 5, self.y + self.size / 2 - 8))  # middle

        if DRAW_SIDE_CONNECTIONS and self.collapsed:
            font = pg.font.SysFont(None, 24)

            edges = self.images.edges[self.imageNumber]

            screen.blit(font.render(str(edges[(0 + self.rotation) % 4]), True, [0, 0, 0]),
                        (self.x + self.size / 2 - 5, self.y))  # top
            screen.blit(font.render(str(edges[(1 + self.rotation) % 4]), True, [0, 0, 0]),
                        (self.x + self.size - 20, self.y + self.size / 2 - 8))  # right
            screen.blit(font.render(str(edges[(2 + self.rotation) % 4]), True, [0, 0, 0]),
                        (self.x + self.size / 2 - 5, self.y + self.size - 14))  # bottom
            screen.blit(font.render(str(edges[(3 + self.rotation) % 4]), True, [0, 0, 0]),
                        (self.x + 4, self.y + self.size / 2 - 8))  # left

        return

    def reverse_edge(self, edge):
        return edge[::-1]

    def define(self, from_direction, edge_color, rotation):
        match = edge_color[(from_direction + 2 + rotation) % 4]
        remove_key = []
        for key in self.superposition.positions:
            remove_val = []
            for val in self.superposition.positions[key]:
                if match != self.reverse_edge(self.images.edges[key][(val + from_direction) % 4]):
                    remove_val.append(val)
            for item in remove_val:
                self.superposition.positions[key].remove(item)

            if len(self.superposition.positions[key]) == 0:
                remove_key.append(key)
        for k in remove_key:
            self.superposition.positions.pop(k)

        return



