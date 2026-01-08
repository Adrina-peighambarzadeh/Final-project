#!/usr/bin/env python3
"""
Created by: Adrina Peighambarzadeh
Created on: Jan 2026
This program is the "Space Aliens" game for the PyBadge.
"""


import stage
import ugame




def game_scene() -> None:
   """
   Runs the main game scene.
   """


   # Image banks for CircuitPython
   image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
   image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")


   # Set the background to image 0 in the image bank
   background = stage.Grid(image_bank_background, 10, 8)


   # Create the player's ship sprite
   ship = stage.Sprite(image_bank_sprites, 5, 75, 66)


   # Create stage (screen)
   game = stage.Stage(ugame.display, 60)


   # Set drawing order: sprites above background
   game.layers = [ship, background]


   # Render background once
   game.render_block()


   while True:
       #  Get user input
       keys = ugame.buttons.get_pressed()


       if keys & ugame.K_X:
           print("A")
       if keys & ugame.K_O:
           print("B")
       if keys & ugame.K_START:
           print("Start")
       if keys & ugame.K_SELECT:
           print("Select")


       # Screen boundaries
       # Screen size: 160x128
       # Sprite size: 16x16 → max X = 144, max Y = 112


       if keys & ugame.K_RIGHT:
           if ship.x < 144:  # right boundary
               ship.move(ship.x + 1, ship.y)


       if keys & ugame.K_LEFT:
           if ship.x > 0:  # left boundary
               ship.move(ship.x - 1, ship.y)


       if keys & ugame.K_UP:
           if ship.y > 0:  # top boundary
               ship.move(ship.x, ship.y - 1)


       if keys & ugame.K_DOWN:
           if ship.y < 112:  # bottom boundary
               ship.move(ship.x, ship.y + 1)


       # Update game logic
       # (Aliens, lasers, collisions later)


       # Redraw sprites
       game.render_sprites([ship])
       game.tick()




if __name__ == "__main__":
   game_scene()
