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
    """This function is the splash scene game loop."""
    # get sound ready
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)
   
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_mt_background, constants.SCREEN_X, constants.SCREEN_Y)
   
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()
   
    while True:
        time.sleep(1.0)
        menu_scene()

def menu_scene():
    """This function is the menu scene."""
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
   
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
    background.tile(2, 2, 0); background.tile(3, 2, 1); background.tile(4, 2, 2); background.tile(5, 2, 3); background.tile(6, 2, 4); background.tile(7, 2, 0)
    background.tile(2, 3, 0); background.tile(3, 3, 5); background.tile(4, 3, 6); background.tile(5, 3, 7); background.tile(6, 3, 8); background.tile(7, 3, 0)
    background.tile(2, 4, 0); background.tile(3, 4, 9); background.tile(4, 4, 10); background.tile(5, 4, 11); background.tile(6, 4, 12); background.tile(7, 4, 0)
    background.tile(2, 5, 0); background.tile(3, 5, 0); background.tile(4, 5, 13); background.tile(5, 5, 14); background.tile(6, 5, 0); background.tile(7, 5, 0)
   
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()
   
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            game_scene()
        game.tick()

def game_scene():
    """This function is the main game scene."""
    
    # setup score (alien_count)
    alien_count = 0

    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # get sounds ready
    pew_sound = open("pew.wav", 'rb')
    boom_sound = open("boom.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    def show_alien():
        """Moves an alien from off screen to on screen"""
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(random.randint(0 + constants.SPRITE_SIZE, 
                                                         constants.SCREEN_X - constants.SPRITE_SIZE), 
                                          constants.OFF_TOP_SCREEN)
                break

    background = stage.Grid(image_bank_background, constants.SCREEN_X, constants.SCREEN_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)

    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # create list of lasers
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        lasers.append(a_single_laser)

    # create list of aliens
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        aliens.append(a_single_alien)
    
    # place 1 alien on the screen
    show_alien()

    game = stage.Stage(ugame.display, 60)
    # set layers in order
    game.layers = aliens + lasers + [ship] + [background]
    game.render_block()

    a_button_state = constants.button_state["button_up"]

    while True:
        keys = ugame.buttons.get_pressed()

        # fire laser logic
        if keys & ugame.K_X != 0: 
            if a_button_state == constants.button_state["button_up"]:
                a_button_state = constants.button_state["button_just_pressed"]
            else:
                a_button_state = constants.button_state["button_still_pressed"]
        else:
            a_button_state = constants.button_state["button_up"]

        if a_button_state == constants.button_state["button_just_pressed"]:
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:
                    lasers[laser_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # ship movement logic
        if keys & ugame.K_RIGHT != 0:
            if ship.x < (constants.SCREEN_X - constants.SPRITE_SIZE):
                ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
        if keys & ugame.K_LEFT != 0:
            if ship.x > 0:
                ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)

        # move lasers up
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                lasers[laser_number].move(lasers[laser_number].x, 
                                          lasers[laser_number].y - constants.LASER_SPEED)
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # move aliens down
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                aliens[alien_number].move(aliens[alien_number].x, 
                                          aliens[alien_number].y + constants.ALIEN_SPEED)
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        # collision detection
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        if stage.collide(lasers[laser_number].x + 6, lasers[laser_number].y + 2,
                                         lasers[laser_number].x + 11, lasers[laser_number].y + 12,
                                         aliens[alien_number].x + 1, aliens[alien_number].y,
                                         aliens[alien_number].x + 15, aliens[alien_number].y + 15):
                            # you hit an alien!
                            aliens[alien_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            lasers[laser_number].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            show_alien()
                            alien_count = alien_count + 1

        # redraw all sprites
        game.render_sprites(aliens + lasers + [ship])
        game.tick()

# This part must be at the very bottom!
if __name__ == "__main__":
    splash_scene()
    