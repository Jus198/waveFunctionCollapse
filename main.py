import random

import pygame as pg
import sys

from pygame import time

import Tile as t

#fullscreen
screen_width = 2550
screen_height = 1600
tileSize = 50

# # mediumscreen
# screen_width = 1000
# screen_height = 800
# tileSize = 100

# # #row
# screen_width = 100
# screen_height = 500
# tileSize = 100

# #2x2
# screen_width = 600
# screen_height = 600
# tileSize = 300

#tileSize = 50
fullScreen = True

DRAW_GRID = True

OPTIMIZATION_DRAWING = True

TilesToCollapse = (screen_height//tileSize)*(screen_width//tileSize)

border_top = screen_height % tileSize
border_sides = screen_width % tileSize
top_offset = border_top/2
side_offset = border_sides/2

#TilesToCollapse = screen_height * screen_width / (tileSize * tileSize)


def collapse():
    def update_superpositions(update_surrounding):
        i, j = update_surrounding.get_location()
        adj_tiles = surrounding_tiles(i, j)
        for i_j in adj_tiles:
            adj_i, adj_j, direction = i_j
            if not tiles[adj_i][adj_j].is_collapsed():
                tiles[adj_i][adj_j].define(direction, images.edges[update_surrounding.imageNumber], update_surrounding.rotation)
                # for each adjacent tile, tell it what edges is on its _ side
                # pop_key = []
                # for key in tiles[adj_i][adj_j].get_superposition().positions:
                #     for rotation in tiles[adj_i][adj_j].get_superposition().positions[key]:
                #         if not tile.possible_position(adj_i, adj_j, key, rotation):
                #             tiles[adj_i][adj_j].get_superposition().positions[key].remove(rotation)
                #             if len(tiles[adj_i][adj_j].get_superposition().positions[key]) == 0:
                #                 pop_key.append(key)
                #                 #tiles[adj_i][adj_j].get_superposition().positions.pop(key)
                # for key in pop_key:
                #     tiles[adj_i][adj_j].get_superposition().positions.pop(key)
                #             # remove position
                # if 0 in tiles[adj_i][adj_j].get_superposition().positions:
                #     tiles[adj_i][adj_j].get_superposition().positions.pop(0)
        return
                #tiles[adj_i][adj_j].update_superpositions(lowest_e_tile)

    pg.init()
    clock = pg.time.Clock()
    if fullScreen:
        screen = pg.display.set_mode([screen_width, screen_height], pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode([screen_width, screen_height])

    images = t.AllImages(tileSize)
    add_images(images)

    tiles = create_tiles(tileSize, images)

    tilesCollapsed = 0

    for row in tiles:
        for tile in row:
            tile.create_superpositions()

    #print(tiles[0][0].get_superpositions())
    #print(TilesToCollapse)

    screen.fill([196, 196, 196])

    while True:
        clock.tick(2000)

        if not OPTIMIZATION_DRAWING:
            screen.fill([196, 196, 196])
            # screen.fill([0,0,0])    # black background ?
            draw_tiles(tiles, screen)
            draw_grid(screen)

        if tilesCollapsed < TilesToCollapse:
            # find lowest entropy tile
            min_e = 9999999999
            lowest_e_tile = None
            temp_tile_count = 0
            for row in tiles:
                for tile in row:
                    if not tile.is_collapsed():
                        e = tile.superposition.get_entropy()
                        if e < min_e:
                            min_e = e
                            lowest_e_tile = tile
                            temp_tile_count = 1
                        # if the entropy of a new tile is equal to the other,
                        # replace it with 1/(tiles sharing entropy) chance
                        if e == min_e:
                            temp_tile_count += 1
                            if random.random() < 1/temp_tile_count:
                                min_e = e
                                lowest_e_tile = tile

            # no tile selected, there is a problem
            if lowest_e_tile is None:
                while True:
                    print("uhhhhhhhhhhhhh")

            # select tile in superposition at random
            lowest_e_tile.set_random_superposition()
            tilesCollapsed += 1
            # update superpositions of 4 nearby tiles
            update_superpositions(lowest_e_tile)
        else:
            pg.time.wait(2000)
            break

        draw_tiles(tiles, screen)
        if DRAW_GRID:
            draw_grid(screen)

        #print(tiles[0][3].get_superposition().positions)
        #pg.time.wait(100)

        # update superpositions of 4 nearby tiles
        # when tile updates superposition, check adjacent tiles with the sum of all superpositions against nearby superpositions
        # when the lowest entropy tile has no superpositions, make a new tile :(

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
    return


def create_tiles(tileSize_, images):

    tiles = []
    for i in range(screen_height//tileSize_):
        tiles.append([])
        for j in range(screen_width//tileSize_):
            tiles[i].append(t.Tile(j*tileSize_ + side_offset, i * tileSize_ + top_offset, tileSize_, images, i, j))
    return tiles


def draw_tiles(tiles, screen):
    for x in range(len(tiles)):
        for tile in tiles[x]:
            tile.draw_tile(screen)
    return


def add_images(images):
    grey = 0
    all_grey = [grey, grey, grey]
    red = 1
    GRG = [grey, red, grey]
    blue = 2
    GBlG = [grey, blue, grey]
    green = 3
    all_green = [green, green, green]
    green_edge = 4


    #del grey, red, blue, green

    # images.add_image("Green.png", 1, [all_green, all_green, all_green, all_green])
    # images.add_image("GreenFlat.png", 4, [all_grey, [grey, green_edge, green], all_green, [green, green_edge, grey]])
    # images.add_image("GreenCorner.png", 4, [all_grey, [grey, green_edge, green], [green, green_edge, grey], all_grey])
    # images.add_image("GreenOutsideCorner.png", 4,
    #                  [all_green, [green, green_edge, grey], [grey, green_edge, green], all_green])
    # images.add_image("GreenFlatRedEnd.png", 4, [GRG, [grey, green_edge, green], all_green, [green, green_edge, grey]])
    # images.add_image("GreenFlatBlueEnd.png", 4, [GBlG, [grey, green_edge, green], all_green, [green, green_edge, grey]])

    images.add_image("Grey.png", 1, [all_grey, all_grey, all_grey, all_grey])
    images.add_image("RedT.png", 4, [all_grey, GRG, GRG, GRG])
    images.add_image("BlueT.png", 4, [all_grey, GBlG, GBlG, GBlG])
    images.add_image("RedEnd.png", 4, [all_grey, all_grey, all_grey, GRG])
    images.add_image("BlueEnd.png", 4, [all_grey, all_grey, all_grey, GBlG])
    images.add_image("RedStraight.png", 2, [all_grey, GRG, all_grey, GRG])
    images.add_image("BlueStraight.png", 2, [all_grey, GBlG, all_grey, GBlG])
    images.add_image("RedCorner.png", 4, [all_grey, GRG, GRG, all_grey])
    images.add_image("BlueCorner.png", 4, [all_grey, GBlG, GBlG, all_grey])
    images.add_image("RedOverBlue.png", 2, [GRG, GBlG, GRG, GBlG])
    images.add_image("BlueOverRed.png", 2, [GBlG, GRG, GBlG, GRG])
    images.add_image("RedStraightBlueEnd.png", 4, [all_grey, GRG, GBlG, GRG])
    images.add_image("BlueStraightRedEnd.png", 4, [all_grey, GBlG, GRG, GBlG])
    # images.add_image("RedCenter.png", 1, [GRG, GRG, GRG, GRG])
    # images.add_image("BlueCenter.png", 1, [GBlG, GBlG, GBlG, GBlG])
    # images.add_image("PurpleCenter.png", 4, [GBlG, GBlG, GRG, GRG])

    # images.add_image("Grey.png", 1, [grey, grey, grey, grey])
    # images.add_image("RedT.png", 4, [grey, red, red, red])
    # images.add_image("BlueT.png", 4, [grey, blue, blue, blue])
    # #images.add_image("RedEnd.png", 4, [grey, grey, grey, red])
    # #images.add_image("BlueEnd.png", 4, [grey, grey, grey, blue])
    # images.add_image("RedStraight.png", 2, [grey, red, grey, red])
    # images.add_image("BlueStraight.png", 2, [grey, blue, grey, blue])
    # images.add_image("RedOverBlue.png", 2, [red, blue, red, blue])
    # images.add_image("BlueOverRed.png", 2, [blue, red, blue, red])
    # images.add_image("RedStraightBlueEnd.png", 4, [grey, red, blue, red])
    # images.add_image("BlueStraightRedEnd.png", 4, [grey, blue, red, blue])
    # images.add_image("RedCenter.png", 1, [red, red, red, red])
    # images.add_image("BlueCenter.png", 1, [blue, blue, blue, blue])
    # #images.add_image("Green.png", 1, [green, green, green, green])
    # #images.add_image("GreenFlat.png", 4, [grey, green_edge, green, green_edge])
    # #images.add_image("GreenCorner.png", 4, [grey, green_edge, green_edge, grey])
    return


def draw_grid(screen):
    for i in range((screen_height // tileSize) - 1):
        pg.draw.line(screen, [0, 0, 0], (0, (i+1)*tileSize), (screen_width, (i+1)*tileSize), 2)
    for j in range((screen_width // tileSize) - 1):
        pg.draw.line(screen, [0, 0, 0], ((j+1)*tileSize, 0), ((j+1)*tileSize, screen_height), 2)
    return


def surrounding_tiles(i, j):
    surrounding = []
    if i > 0:
        surrounding.append([i-1, j, 2])
    if i < (screen_height // tileSize)-1:
        surrounding.append([i+1, j, 0])
    if j > 0:
        surrounding.append([i, j-1, 1])
    if j < (screen_width // tileSize)-1:
        surrounding.append([i, j+1, 3])
    return surrounding


if __name__ == '__main__':
    #random.seed(1)
    #print(pg.font.get_fonts())
    while True:
        collapse()
    print("Done")
