#!/usr/bin/env python3

"""
Created by: Adrina Peighambarzadeh
Created on: Jan 2026
This program is the "Space Aliens" program on the PyBadge
"""

import ugame
import stage
import random
import time
import constants

def splash_scene():
    # this function is the splash scene game loop
    
    # get sound ready
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)
    
    # an image bank for CircuitPython
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    
    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y)
    
    # create a stage for the background to show up on
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()
    
    # repeat forever, game loop
    while True:
        # Wait for 1 second
        time.sleep(1.0)
        menu_scene()

def menu_scene():
    # this function is the menu scene
    
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    
    # add text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)
    
    text2 = stage.Text(width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)
    
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y)
    
    # build the logo using tiles
    background.tile(2, 2, 0)
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)
    
    background.tile(2, 3, 0)
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)
    
    background.tile(2, 4, 0)
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)
    
    background.tile(2, 5, 0)
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)
    
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()
    
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            game_scene()
        game.tick()

def game_scene():
    # this function is the main game scene
    
    # image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # set the background to images and the size (10x8 tiles)
    background = stage.Grid(image_bank_background, constants.SCREEN_X, constants.SCREEN_Y)
    
    # Randomly pick tiles for the background
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    # Setup Sprites
    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))
    alien = stage.Sprite(image_bank_sprites, 9, int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2), 16)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [ship] + [alien] + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        
        # Ship Movement logic
        if keys & ugame.K_RIGHT != 0:
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
        if keys & ugame.K_LEFT != 0:
            if ship.x > 0:
                ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)

        game.render_sprites([ship] + [alien])
        game.tick()

if __name__ == "__main__":
    splash_scene()
    